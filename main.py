import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGraphicsView, QGraphicsScene,QGraphicsRectItem,QGraphicsLineItem,QGraphicsItem,
    QGroupBox,QScrollArea, QToolBox , QAction, QFileDialog,
    QTabWidget)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor,QPen,QPainter

from gates import *
import json

class MovableRect(QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges 
        )
        self.line = None

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange:
            #print(f"Yeni konum: {value.x()}, {value.y()}")
            # Buraya senin istediğin fonksiyonu çağırabilirsin
            if self.line != None:
                self.line.setLine(value.x(),value.y(),0,0)
                
                
                
        return super().itemChange(change, value)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("sol tik")
        
        return super().mousePressEvent(event)
   


class CustomScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.start_point = None

    def mousePressEvent_______(self, event):
        if event.button() == Qt.LeftButton:
            if self.start_point is None:
                # İlk tıklama: başlangıç noktası
                self.start_point = event.scenePos()
                print(f"Başlangıç noktası: {self.start_point}")
            else:
                # İkinci tıklama: çizgi çiz ve sıfırla
                end_point = event.scenePos()
                print(f"Bitiş noktası: {end_point}")
                line = QGraphicsLineItem(
                    self.start_point.x(), self.start_point.y(),
                    end_point.x(), end_point.y()
                )
                pen = QPen(QColor("black"))
                pen.setWidth(2)
                line.setPen(pen)
                self.addItem(line)
                self.start_point = None  # yeniden çizime hazır
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        #print("position: " , event.scenePos().x(),event.scenePos().y())
        if pin.is_clicked == True:
            self.addItem(pin.line)
            pin.is_clicked = False
        
        pin.line.setLine(pin.start_pos[0],pin.start_pos[1],event.scenePos().x(),event.scenePos().y())
        

        return super().mouseMoveEvent(event)
        

class CollapsibleSection(QWidget):
    def __init__(self, title, content_widget):
        super().__init__()
        self.toggle_button = QPushButton(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.clicked.connect(self.toggle)

        self.content = content_widget
        self.content.setVisible(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.content)

    def toggle(self):
        visible = self.toggle_button.isChecked()
        self.content.setVisible(visible)


class LogicSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mantık Devresi Simülatörü")
        self.setGeometry(100, 100, 900, 600)
        self.scenes = []
        self.files_for_tabs = dict()
        self.initMenuBar()
        self.initUI()

    def initMenuBar(self):
        # Menü çubuğu
        menubar = self.menuBar()

        # File menüsü
        file_menu = menubar.addMenu("File")

        # Open file action
        open_action = QAction("Open File", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Save file action
        save_file_action = QAction("Save File", self)
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        # Save file action
        new_file_action = QAction("New File", self)
        new_file_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_file_action)
        
        



        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def get_current_scene(self):
        tab_widget = self.tabs.currentWidget()
        view = tab_widget.layout().itemAt(0).widget()
        return view.scene()

    def add_new_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        scene = CustomScene()
        self.scenes.append(scene)
        view = QGraphicsView(scene)
        layout.addWidget(view)
        self.tabs.addTab(tab, f"Circuit {self.tabs.count() + 1}")
        self.files_for_tabs[tab] = None
        self.tabs.setCurrentWidget(tab)
        


    def open_file(self):

        file_name, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "Tüm Dosyalar (*)")
        
        if file_name:

            self.add_new_tab()
            self.tabs.setTabText(self.tabs.currentIndex(),file_name.split('/')[-1])
            self.files_for_tabs[self.tabs.currentWidget()] = file_name

            print("Seçilen dosya:", file_name)

            with open(file_name, "r") as f:
                data = json.load(f)
                
            if data['type'] == 'circuit':
                components = data['components']

                line_list = set()
                all_pins = dict()

                for i in components:


                    if i['type'] ==  "input":
                        comp = logic_input()
                        comp.setPos(i['position_x'],i['position_y'])
                        out_pin = i['output_pin']
                        id = out_pin['id']
                        comp.output_pin.id = id
                        all_pins[id] = comp.output_pin
                        connections = out_pin['connections']
                        for j in connections:
                            line_list.add((id,j) if id > j else (j,id) )

                        self.get_current_scene().addItem(comp)

                    if i['type'] ==  "output":

                        comp = logic_output()
                        comp.setPos(i['position_x'],i['position_y'])
                        input_pin = i['input_pin']
                        id = input_pin['id']
                        comp.input_pin.id = id
                        all_pins[id] = comp.input_pin
                        connections = input_pin['connections']
                        for j in connections:
                            line_list.add((id,j) if id > j else (j,id) )

                        self.get_current_scene().addItem(comp)
                        self.get_current_scene()
                    
                    if i['type'] == "NOT":
                        comp = not_gate()
                        comp.setPos(i['position_x'],i['position_y'])
                        pins = i['pins']
                    
                        comp.input_pin1.id  = pins[0]['id']
                        comp.output_pin.id  = pins[1]['id']
                        all_pins[pins[0]['id']] = comp.input_pin1
                        all_pins[pins[1]['id']] = comp.output_pin

                        for my_pin in pins:
                            connections = my_pin['connections']
                            for j in connections:
                                id = my_pin['id']
                                line_list.add((id,j) if id > j else (j,id) )
                        self.get_current_scene().addItem(comp)



                    if i['type'] in  ["AND","OR","NAND","NOR","XOR"]:
                        if i['type'] == "AND":
                            comp = and_gate()
                        if i['type'] == "OR":
                            comp = or_gate()
                        if i['type'] == "NAND":
                            comp = nand_gate()
                        if i['type'] == "NOR":
                            comp = nor_gate()
                        if i['type'] == "XOR":
                            comp = xor_gate()

                        comp.setPos(i['position_x'],i['position_y'])
                        pins = i['pins']
                        comp.input_pin1.id  = pins[0]['id']
                        comp.input_pin2.id  = pins[1]['id']
                        comp.output_pin.id  = pins[2]['id']
                        all_pins[pins[0]['id']] = comp.input_pin1
                        all_pins[pins[1]['id']] = comp.input_pin2
                        all_pins[pins[2]['id']] = comp.output_pin
                        

                        for my_pin in pins:
                            connections = my_pin['connections']
                            for j in connections:
                                id = my_pin['id']
                                line_list.add((id,j) if id > j else (j,id) )
                        self.get_current_scene().addItem(comp)





                line_list = list(line_list)

                for i in line_list:
                    print(i)
                    
                    pin1:pin
                    pin2:pin
                    
                    pin1 = all_pins[i[0]]
                    pin2 = all_pins[i[1]]
                    x1 = pin1.parentItem().pos().x() + pin1.x
                    y1 = pin1.parentItem().pos().y() + pin1.y
                    x2 = pin2.parentItem().pos().x() + pin2.x
                    y2 = pin2.parentItem().pos().y() + pin2.y
                    


                    my_cable = cable(x1,y1,x2,y2)
                    print("POSITION",x1,y1,x2,y2)
                
                    
                    my_cable.joints = [all_pins[i[0]],all_pins[i[1]]]
                    if all_pins[i[0]].is_input_pin == False:
                        my_cable.input_source = all_pins[i[0]]

                    if all_pins[i[1]].is_input_pin == False:
                        my_cable.input_source = all_pins[i[1]]
                    
                    
                    all_pins[i[0]].lines.append([my_cable,"start"])
                    all_pins[i[1]].lines.append([my_cable,"end"])

                    self.get_current_scene().addItem(my_cable)
                    
                    print(all_pins[i[0]],all_pins[i[1]])

                    
    def save_file(self):
        filename = self.files_for_tabs[self.tabs.currentWidget()]
        if filename is None:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Devreyi Kaydet",              # Pencere başlığı
                "",                            # Varsayılan klasör
                "Tum dosyalar (*)"     # Dosya türü filtresi
            )
            if filename == "":
                return False
            self.files_for_tabs[self.tabs.currentWidget()] = filename


        print(self.get_current_scene().items())
        my_json = {}
        my_json['type'] = "circuit"
        components = []
        for i in self.get_current_scene().items():
            if i.__repr__() == "component":
                components.append(i.to_json())
        my_json['components'] = components
        with open(filename, "w") as f:
            json.dump(my_json, f, indent=4)




    def keyPressEvent(self, event):

        #delete 
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key.Key_0 or event.key() == Qt.Key.Key_Backspace :
            selected_items = self.get_current_scene().selectedItems()
            for item in selected_items:
                for pins in item.get_pins():
                    for a_line in pins.lines:
                        if a_line[0].joints[0] == pins:
                            a_line[0].joints[1].lines.remove([a_line[0], 'start' if a_line[1] == 'end' else 'end'])
                        if a_line[0].joints[1] == pins:
                            a_line[0].joints[0].lines.remove([a_line[0], 'start' if a_line[1] == 'end' else 'end'])
                        
                        self.get_current_scene().removeItem(a_line[0])
                        del a_line[0]

                self.get_current_scene().removeItem(item)
                del item
        else:
            super().keyPressEvent(event)

    def change_color(self):
        #self.myrect.setBrush(QBrush(QColor(255,0,0)))  # içini renklendir
        
        #self.line.setLine(0,0,139,98)
        color = QColor(0,255,0) if self.line.pen().color() == QColor(0,100,0) else QColor(0,100,0)
        #print(color.getRgb())
        self.line.setPen(QPen(color,2))
        
        
        

        


    def create_gate_panel(self):
        scroll_area = QScrollArea()
        scroll_area.setFixedWidth(220)
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Logic Section
        logic_content = QWidget()
        logic_layout = QVBoxLayout(logic_content)
        for name in ["AND", "OR", "NOT", "NAND", "NOR", "XOR"]:
            btn = QPushButton(name)
            if name == "AND":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(and_gate()) )
            if name == "OR":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(or_gate()) )
            if name == "NOT":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(not_gate()) )
            if name == "NAND":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(nand_gate()) )
            if name == "NOR":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(nor_gate()) )
            if name == "XOR":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(xor_gate()) )
            

            logic_layout.addWidget(btn)
        logic_layout.addStretch()
        logic_section = CollapsibleSection("Logic Gates", logic_content)

        # I/O Section
        io_content = QWidget()
        io_layout = QVBoxLayout(io_content)
        for name in ["Button", "Input", "Output"]:
            btn = QPushButton(name)
            if name == "Button":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(logic_input()) )
            if name == "Input":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(logic_input()) )
            if name == "Output":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(logic_output()) )
           

            io_layout.addWidget(btn)
        io_layout.addStretch()
        io_section = CollapsibleSection("Input / Output", io_content)

        # Memory Section
        mem_content = QWidget()
        mem_layout = QVBoxLayout(mem_content)
        for name in ["D Flip-Flop", "T Flip-Flop", "JK Flip-Flop"]:
            mem_layout.addWidget(QPushButton(name))
        mem_layout.addStretch()
        mem_section = CollapsibleSection("Memory", mem_content)

        # Add all to layout
        container_layout.addWidget(logic_section)
        container_layout.addWidget(io_section)
        container_layout.addWidget(mem_section)
        container_layout.addStretch()

        scroll_area.setWidget(container)
        return scroll_area


    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Sol panel (gate butonları)
        left_panel = self.create_gate_panel()
        main_layout.addWidget(left_panel)


            
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # İlk sekmeyi ekle
        self.add_new_tab() 
        
        # Sağ taraf (çizim alanı)
        """ self.scene = CustomScene()
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 680, 580)
        self.view.setSceneRect(0, 0, 680, 580)
        """

        # Ana layout'a ekle
        #main_layout.addWidget(panel)
        #main_layout.addWidget(self.view)


        
        
        

        #self.scene.addItem(self.myrect)  # sahneye ekle
        #self.scene.addItem(self.line)
        #self.scene.addItem(self.my_input)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogicSimulator()
    
    window.show()


    sys.exit(app.exec_())