import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGraphicsView, QGraphicsScene,QGraphicsRectItem,QGraphicsLineItem,QGraphicsItem,
    QGroupBox,QScrollArea, QToolBox , QAction, QFileDialog,
    QTabWidget , QLineEdit,QComboBox,QGridLayout, QDialog, QDialogButtonBox,
    QFormLayout, QListWidget, QListWidgetItem, QSplitter, QMessageBox)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor,QPen,QPainter , QIntValidator

from gates import *
from additional_component import *
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
        self.imported_components = {}  # name -> component_data
        self.initUI()
        self.initMenuBar()

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

        # Save file action
        panel_ac = QAction("alt paneli ac", self)
        panel_ac.triggered.connect(lambda: self.show_footer_panel(True))
        file_menu.addAction(panel_ac)

        panel_kapat = QAction("alt paneli kapat", self)
        panel_kapat.triggered.connect(lambda: self.show_footer_panel(False))
        file_menu.addAction(panel_kapat)
        
        
        
        



        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create menüsü
        create_menu = menubar.addMenu("Create")
        
        # Create Component action
        create_component_action = QAction("Create Component", self)
        create_component_action.triggered.connect(self.open_component_designer)
        create_menu.addAction(create_component_action)
        
        # Import Component action
        import_component_action = QAction("Import Component", self)
        import_component_action.triggered.connect(self.import_component)
        create_menu.addAction(import_component_action)

    def open_component_designer(self):
        """Open the component designer window"""
        designer = ComponentDesigner(self)
        designer.exec_()
    
    def import_component(self):
        """Import a saved component into the library"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Component",
            "",
            "Component Files (*.comp);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    component_data = json.load(f)
                
                if component_data.get('type') == 'custom_component_definition':
                    comp_name = component_data.get('name', 'Custom')
                    
                    # Store component data
                    self.imported_components[comp_name] = component_data
                    
                    # Add button to imported components panel
                    self.add_imported_component_button(comp_name, component_data)
                    
                    QMessageBox.information(self, "Success", f"Component '{comp_name}' imported successfully!\nYou can now add it from the 'Imported Components' panel.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to import component: {str(e)}")
    
    def add_imported_component_button(self, name, component_data):
        """Add a button for the imported component to the panel"""
        btn = QPushButton(name)
        btn.setStyleSheet("background-color: #6B8E23; color: white;")
        # Use lambda with default argument to capture the current component_data
        btn.clicked.connect(lambda checked, data=component_data: self.add_custom_component_to_scene(data))
        self.imported_components_layout.addWidget(btn)
    
    def add_custom_component_to_scene(self, component_data):
        """Add a custom component to the current scene"""
        import copy
        # Deep copy to avoid sharing the same data between instances
        data_copy = copy.deepcopy(component_data)
        custom_comp = CustomComponent(data_copy)
        custom_comp.setPos(200, 200)
        self.get_current_scene().addItem(custom_comp)

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

                    # Custom Component yükleme
                    if i['type'] == "custom_component":
                        circuit_data = i.get('circuit', {})
                        circuit_components = circuit_data.get('components', [])
                        
                        # İç devreden pin isimlerini ve pozisyonlarını topla (sıralama için)
                        input_pin_info = []
                        output_pin_info = []
                        for cc in circuit_components:
                            if cc.get('type') == 'component_input':
                                input_pin_info.append({
                                    'name': cc.get('pin_name', 'IN'),
                                    'position_y': cc.get('position_y', 0)
                                })
                            elif cc.get('type') == 'component_output':
                                output_pin_info.append({
                                    'name': cc.get('pin_name', 'OUT'),
                                    'position_y': cc.get('position_y', 0)
                                })
                        
                        # Pinleri Y pozisyonuna göre sırala (yukarıdan aşağıya)
                        input_pin_info.sort(key=lambda x: x['position_y'])
                        output_pin_info.sort(key=lambda x: x['position_y'])
                        
                        # Sadece isim listesi oluştur
                        input_pin_names = [{'name': p['name']} for p in input_pin_info]
                        output_pin_names = [{'name': p['name']} for p in output_pin_info]
                        
                        # Eğer iç devreden isim bulunamazsa, varsayılan isimler kullan
                        if not input_pin_names:
                            input_pin_names = [{'name': f'IN{idx+1}'} for idx in range(len(i.get('input_pins', [])))]
                        if not output_pin_names:
                            output_pin_names = [{'name': f'OUT{idx+1}'} for idx in range(len(i.get('output_pins', [])))]
                        
                        component_data = {
                            'name': i.get('component_name', 'Custom'),
                            'input_pins': input_pin_names,
                            'output_pins': output_pin_names,
                            'circuit': circuit_data
                        }
                        comp = CustomComponent(component_data)
                        comp.setPos(i['position_x'], i['position_y'])
                        
                        # Input pinlerini yükle
                        input_pins_data = i.get('input_pins', [])
                        for idx, pin_data in enumerate(input_pins_data):
                            if idx < len(comp.input_pins):
                                pin_id = pin_data.get('id')
                                comp.input_pins[idx].id = pin_id
                                all_pins[pin_id] = comp.input_pins[idx]
                                connections = pin_data.get('connections', [])
                                for j in connections:
                                    line_list.add((pin_id, j) if pin_id > j else (j, pin_id))
                        
                        # Output pinlerini yükle
                        output_pins_data = i.get('output_pins', [])
                        for idx, pin_data in enumerate(output_pins_data):
                            if idx < len(comp.output_pins):
                                pin_id = pin_data.get('id')
                                comp.output_pins[idx].id = pin_id
                                all_pins[pin_id] = comp.output_pins[idx]
                                connections = pin_data.get('connections', [])
                                for j in connections:
                                    line_list.add((pin_id, j) if pin_id > j else (j, pin_id))
                        
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


    def show_footer_panel(self,visible = True):
        self.bottom_panel.setVisible(visible)


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
        for name in ["Button", "Input", "Output","7-segment-display","decoder-7","counter"]:
            btn = QPushButton(name)
            if name == "Button":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(logic_input()) )
            if name == "Input":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(logic_input()) )
            if name == "Output":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(logic_output()) )
            if name == "7-segment-display":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(seven_segment_display()) )
            if name == "decoder-7":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(decoder_7_segment()) )
            if name == "counter":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(four_bit_counter()) )
            
            

            
           

            io_layout.addWidget(btn)
        io_layout.addStretch()
        io_section = CollapsibleSection("Input / Output", io_content)

        # Memory Section
        mem_content = QWidget()
        mem_layout = QVBoxLayout(mem_content)
        for name in ["D Flip-Flop", "T Latch", "JK Flip-Flop"]:
            btn = QPushButton(name)
            
            if name == "D Flip-Flop":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(d_flip_flop()) )
            if name == "T Latch":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(t_latch()) )
            if name == "JK Flip-Flop":
                btn.clicked.connect( lambda x: self.get_current_scene().addItem(jk_flip_flop()) )
            
            

            mem_layout.addWidget(btn)

        mem_layout.addStretch()
        mem_section = CollapsibleSection("Memory", mem_content)

        # Imported Components Section
        imported_content = QWidget()
        self.imported_components_layout = QVBoxLayout(imported_content)
        self.imported_components_layout.addStretch()
        imported_section = CollapsibleSection("Imported Components", imported_content)

        # Add all to layout
        container_layout.addWidget(logic_section)
        container_layout.addWidget(io_section)
        container_layout.addWidget(mem_section)
        container_layout.addWidget(imported_section)
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


        # component panel (gizli başlangıçta)
        self.bottom_panel = QFrame()
        self.bottom_panel.setFixedWidth(300)
        self.bottom_panel.setFrameShape(QFrame.StyledPanel)
        self.bottom_panel.setVisible(False)


        #self.footer_dropdown = QComboBox()
        #self.footer_dropdown.addItems(["Seçenek 1", "Seçenek 2", "Seçenek 3"])

        #bottom_layout = QVBoxLayout(self.bottom_panel)
        bottom_layout = QGridLayout(self.bottom_panel)

        first_row = QVBoxLayout()
        layout = QVBoxLayout()
        



        

        #first_row.addWidget(self.footer_dropdown)

        selection = QComboBox()
        orientations = QComboBox()
        orientations.addItems(['left','right','top','bottom'])
        def load_from_scene():
            input_pin_list = [pin_with_label(label = i.my_name) for i in self.get_current_scene().items() if i.__str__().startswith('in') ]
            component_template.set_my_pin_list('left',input_pin_list)
            output_pin_list = [pin_with_label(label = i.my_name) for i in self.get_current_scene().items() if i.__str__().startswith('out') ]
            component_template.set_my_pin_list('right',output_pin_list)

            ([i.label for i in input_pin_list])
            selection.clear()
            selection.addItems([i.label for i in input_pin_list])
            selection.addItems([i.label for i in output_pin_list])
            
            

            

            component_template.locate_pins()


        load_from_scene_btn =  QPushButton("Reset/Load from scene")
        load_from_scene_btn.clicked.connect(load_from_scene)


        bottom_layout.addWidget(load_from_scene_btn,0,0,1,2)
        

        self.add_input_btn = QPushButton("component input pin")
        self.add_input_btn.clicked.connect( lambda x: self.get_current_scene().addItem(component_input_pin()) )
        self.add_output_btn = QPushButton("component output pin")
        self.add_output_btn.clicked.connect( lambda x: self.get_current_scene().addItem(component_output_pin()) )
        
        
        
        bottom_layout.addWidget( self.add_input_btn,1,0,1,2)
        bottom_layout.addWidget( self.add_output_btn,2,0,1,2)

        

        #self.number_of_pins_on_left = QLineEdit()
        #self.number_of_pins_on_left.setText(str(0))
        #self.number_of_pins_on_left.setValidator(QIntValidator(0,component_input_pin.counter))
        #bottom_layout.addWidget(QLabel("Seçim:"), 2, 0)
        #bottom_layout.addWidget(self.number_of_pins_on_left,2,1,1,1)
        bottom_layout.addWidget(QLabel("isim:"), 4, 0)
        isim = QLineEdit()
        bottom_layout.addWidget(isim,4,1)        

       

        #bottom_layout.addWidget(QLabel("____________"), 30, 0)
        


        aa_scene = CustomScene()
        component_template = general_component_template()
        
        submit_btn = QPushButton("apply")


        

        input_pins = {}
        output_pins = {}
        
        def apply():
            component_template.set_my_name(isim.text() if isim.text() is not None else '')
            #pin_name = selection.currentText()
            #location = orientations.currentText()
            #component_template.change_pin_position_and_name(pin_name,location,new_name= '')

            
            
            #print(component_template.left_pins)
            

        submit_btn.clicked.connect(apply)
        


        aa_scene.addItem(component_template)
        view = QGraphicsView(aa_scene)
        
        layout.addWidget(view)

        #bottom_layout.addWidget(selection,5,0)     
        #bottom_layout.addWidget(orientations,5,1)     
           
        bottom_layout.addWidget(submit_btn,6,0)        

        bottom_layout.addLayout(layout,31,0,1,2)







        


        
        main_layout.addWidget(self.bottom_panel)

        ####
            
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


class ComponentDesignerScene(QGraphicsScene):
    """Custom scene for component designer"""
    def __init__(self):
        super().__init__()
        self.start_point = None

    def mouseMoveEvent(self, event):
        if pin.is_clicked == True:
            self.addItem(pin.line)
            pin.is_clicked = False
        
        pin.line.setLine(pin.start_pos[0], pin.start_pos[1], event.scenePos().x(), event.scenePos().y())
        return super().mouseMoveEvent(event)


class ComponentDesigner(QDialog):
    """Dialog window for designing custom components"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent  # Reference to main window for imported components
        self.setWindowTitle("Component Designer")
        self.setGeometry(150, 150, 1200, 700)
        self.setModal(True)
        
        self.component_name = "MyComponent"
        self.input_pin_counter = 0
        self.output_pin_counter = 0
        
        self.initUI()
    
    def initUI(self):
        main_layout = QHBoxLayout(self)
        
        # Left panel - component palette
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(200)
        
        # Component name input
        name_group = QGroupBox("Component Name")
        name_layout = QVBoxLayout(name_group)
        self.name_input = QLineEdit(self.component_name)
        self.name_input.textChanged.connect(self.update_component_name)
        name_layout.addWidget(self.name_input)
        left_layout.addWidget(name_group)
        
        # Component pins group
        pins_group = QGroupBox("Component Pins")
        pins_layout = QVBoxLayout(pins_group)
        
        add_input_btn = QPushButton("+ Add Input Pin")
        add_input_btn.clicked.connect(self.add_input_pin)
        add_input_btn.setStyleSheet("background-color: #4682B4; color: white;")
        pins_layout.addWidget(add_input_btn)
        
        add_output_btn = QPushButton("+ Add Output Pin")
        add_output_btn.clicked.connect(self.add_output_pin)
        add_output_btn.setStyleSheet("background-color: #B44646; color: white;")
        pins_layout.addWidget(add_output_btn)
        
        left_layout.addWidget(pins_group)
        
        # Logic gates group
        gates_group = QGroupBox("Logic Gates")
        gates_layout = QVBoxLayout(gates_group)
        
        gate_buttons = [
            ("AND Gate", self.add_and_gate),
            ("OR Gate", self.add_or_gate),
            ("NOT Gate", self.add_not_gate),
            ("NAND Gate", self.add_nand_gate),
            ("NOR Gate", self.add_nor_gate),
            ("XOR Gate", self.add_xor_gate),
        ]
        
        for name, callback in gate_buttons:
            btn = QPushButton(name)
            btn.clicked.connect(callback)
            gates_layout.addWidget(btn)
        
        left_layout.addWidget(gates_group)
        
        # Imported Components group (from main window)
        imported_group = QGroupBox("Imported Components")
        imported_layout = QVBoxLayout(imported_group)
        
        # Import button for designer
        import_btn = QPushButton("+ Import Component")
        import_btn.setStyleSheet("background-color: #6B8E23; color: white;")
        import_btn.clicked.connect(self.import_component_for_designer)
        imported_layout.addWidget(import_btn)
        
        # Add buttons for already imported components
        if self.parent_window and hasattr(self.parent_window, 'imported_components'):
            for comp_name, comp_data in self.parent_window.imported_components.items():
                btn = QPushButton(comp_name)
                btn.setStyleSheet("background-color: #556B2F; color: white;")
                btn.clicked.connect(lambda checked, data=comp_data: self.add_imported_component(data))
                imported_layout.addWidget(btn)
        
        self.imported_buttons_layout = imported_layout
        left_layout.addWidget(imported_group)
        
        left_layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Component")
        save_btn.setStyleSheet("background-color: #2E8B57; color: white; font-weight: bold; padding: 10px;")
        save_btn.clicked.connect(self.save_component)
        left_layout.addWidget(save_btn)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        left_layout.addWidget(cancel_btn)
        
        main_layout.addWidget(left_panel)
        
        # Center - design area
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        design_label = QLabel("Design Area - Create your component circuit")
        design_label.setStyleSheet("font-weight: bold; padding: 5px;")
        center_layout.addWidget(design_label)
        
        self.design_scene = ComponentDesignerScene()
        self.design_scene.setSceneRect(0, 0, 800, 1500)  # Larger vertical area
        self.design_view = QGraphicsView(self.design_scene)
        self.design_view.setRenderHint(QPainter.Antialiasing)
        self.design_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.design_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        center_layout.addWidget(self.design_view)
        
        main_layout.addWidget(center_widget, stretch=1)
        
        # Right panel - pin configuration
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_panel.setFixedWidth(250)
        
        # Input pins list
        input_group = QGroupBox("Input Pins")
        input_layout = QVBoxLayout(input_group)
        self.input_pins_list = QListWidget()
        self.input_pins_list.itemDoubleClicked.connect(self.rename_input_pin)
        input_layout.addWidget(self.input_pins_list)
        input_layout.addWidget(QLabel("Double-click to rename"))
        
        delete_input_btn = QPushButton("Delete Selected Input")
        delete_input_btn.setStyleSheet("background-color: #8B0000; color: white;")
        delete_input_btn.clicked.connect(self.delete_selected_input_pin)
        input_layout.addWidget(delete_input_btn)
        
        right_layout.addWidget(input_group)
        
        # Output pins list
        output_group = QGroupBox("Output Pins")
        output_layout = QVBoxLayout(output_group)
        self.output_pins_list = QListWidget()
        self.output_pins_list.itemDoubleClicked.connect(self.rename_output_pin)
        output_layout.addWidget(self.output_pins_list)
        output_layout.addWidget(QLabel("Double-click to rename"))
        
        delete_output_btn = QPushButton("Delete Selected Output")
        delete_output_btn.setStyleSheet("background-color: #8B0000; color: white;")
        delete_output_btn.clicked.connect(self.delete_selected_output_pin)
        output_layout.addWidget(delete_output_btn)
        
        right_layout.addWidget(output_group)
        
        # Preview group
        preview_group = QGroupBox("Component Preview")
        preview_layout = QVBoxLayout(preview_group)
        self.preview_scene = QGraphicsScene()
        self.preview_view = QGraphicsView(self.preview_scene)
        self.preview_view.setFixedHeight(150)
        preview_layout.addWidget(self.preview_view)
        right_layout.addWidget(preview_group)
        
        right_layout.addStretch()
        main_layout.addWidget(right_panel)
        
        self.update_preview()
    
    def update_component_name(self, text):
        self.component_name = text
        self.update_preview()
    
    def add_input_pin(self):
        self.input_pin_counter += 1
        pin_name = f"IN{self.input_pin_counter}"
        
        comp_input = ComponentInputPin()
        comp_input.set_pin_name(pin_name)
        # All input pins spawn at the same position
        comp_input.setPos(50, 50)
        self.design_scene.addItem(comp_input)
        
        item = QListWidgetItem(pin_name)
        item.setData(Qt.UserRole, comp_input)
        self.input_pins_list.addItem(item)
        
        self.update_preview()
    
    def add_output_pin(self):
        self.output_pin_counter += 1
        pin_name = f"OUT{self.output_pin_counter}"
        
        comp_output = ComponentOutputPin()
        comp_output.set_pin_name(pin_name)
        # All output pins spawn at the same position
        comp_output.setPos(600, 50)
        self.design_scene.addItem(comp_output)
        
        item = QListWidgetItem(pin_name)
        item.setData(Qt.UserRole, comp_output)
        self.output_pins_list.addItem(item)
        
        self.update_preview()
    
    def rename_input_pin(self, item):
        from PyQt5.QtWidgets import QInputDialog
        new_name, ok = QInputDialog.getText(self, "Rename Pin", "Enter new pin name:", text=item.text())
        if ok and new_name:
            item.setText(new_name)
            comp = item.data(Qt.UserRole)
            if comp:
                comp.set_pin_name(new_name)
            self.update_preview()
    
    def rename_output_pin(self, item):
        from PyQt5.QtWidgets import QInputDialog
        new_name, ok = QInputDialog.getText(self, "Rename Pin", "Enter new pin name:", text=item.text())
        if ok and new_name:
            item.setText(new_name)
            comp = item.data(Qt.UserRole)
            if comp:
                comp.set_pin_name(new_name)
            self.update_preview()
    
    def add_and_gate(self):
        gate = and_gate()
        gate.setPos(300, 200)
        self.design_scene.addItem(gate)
    
    def add_or_gate(self):
        gate = or_gate()
        gate.setPos(300, 200)
        self.design_scene.addItem(gate)
    
    def add_not_gate(self):
        gate = not_gate()
        gate.setPos(300, 200)
        self.design_scene.addItem(gate)
    
    def add_nand_gate(self):
        gate = nand_gate()
        gate.setPos(300, 200)
        self.design_scene.addItem(gate)
    
    def add_nor_gate(self):
        gate = nor_gate()
        gate.setPos(300, 200)
        self.design_scene.addItem(gate)
    
    def add_xor_gate(self):
        gate = xor_gate()
        gate.setPos(300, 200)
        self.design_scene.addItem(gate)
    
    def import_component_for_designer(self):
        """Import a component to use in the designer"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Component",
            "",
            "Component Files (*.comp);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    component_data = json.load(f)
                
                if component_data.get('type') == 'custom_component_definition':
                    comp_name = component_data.get('name', 'Custom')
                    
                    # Also add to main window's imported components
                    if self.parent_window and hasattr(self.parent_window, 'imported_components'):
                        if comp_name not in self.parent_window.imported_components:
                            self.parent_window.imported_components[comp_name] = component_data
                            self.parent_window.add_imported_component_button(comp_name, component_data)
                    
                    # Add button to designer's imported components panel
                    btn = QPushButton(comp_name)
                    btn.setStyleSheet("background-color: #556B2F; color: white;")
                    btn.clicked.connect(lambda checked, data=component_data: self.add_imported_component(data))
                    self.imported_buttons_layout.addWidget(btn)
                    
                    QMessageBox.information(self, "Success", f"Component '{comp_name}' imported!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to import component: {str(e)}")
    
    def add_imported_component(self, component_data):
        """Add an imported custom component to the design scene"""
        import copy
        data_copy = copy.deepcopy(component_data)
        custom_comp = CustomComponent(data_copy)
        custom_comp.setPos(300, 200)
        self.design_scene.addItem(custom_comp)
    
    def delete_selected_input_pin(self):
        """Delete the selected input pin from list and scene"""
        current_item = self.input_pins_list.currentItem()
        if current_item:
            comp = current_item.data(Qt.UserRole)
            if comp:
                # Remove connected cables
                if hasattr(comp, 'output_pin'):
                    for line_info in comp.output_pin.lines[:]:
                        cable_obj = line_info[0]
                        # Remove from other pin's lines
                        for joint in cable_obj.joints:
                            if joint != comp.output_pin:
                                joint.lines = [l for l in joint.lines if l[0] != cable_obj]
                        self.design_scene.removeItem(cable_obj)
                self.design_scene.removeItem(comp)
            row = self.input_pins_list.row(current_item)
            self.input_pins_list.takeItem(row)
            self.update_preview()
    
    def delete_selected_output_pin(self):
        """Delete the selected output pin from list and scene"""
        current_item = self.output_pins_list.currentItem()
        if current_item:
            comp = current_item.data(Qt.UserRole)
            if comp:
                # Remove connected cables
                if hasattr(comp, 'input_pin'):
                    for line_info in comp.input_pin.lines[:]:
                        cable_obj = line_info[0]
                        # Remove from other pin's lines
                        for joint in cable_obj.joints:
                            if joint != comp.input_pin:
                                joint.lines = [l for l in joint.lines if l[0] != cable_obj]
                        self.design_scene.removeItem(cable_obj)
                self.design_scene.removeItem(comp)
            row = self.output_pins_list.row(current_item)
            self.output_pins_list.takeItem(row)
            self.update_preview()
    
    def keyPressEvent(self, event):
        """Handle key press events for deletion"""
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            self.delete_selected_items()
        else:
            super().keyPressEvent(event)
    
    def delete_selected_items(self):
        """Delete selected items from the design scene"""
        selected_items = self.design_scene.selectedItems()
        for item in selected_items:
            # Check if it's a component with pins
            if hasattr(item, 'get_pins'):
                for p in item.get_pins():
                    for line_info in p.lines[:]:
                        cable_obj = line_info[0]
                        # Remove from other pin's lines
                        for joint in cable_obj.joints:
                            if joint != p:
                                joint.lines = [l for l in joint.lines if l[0] != cable_obj]
                        self.design_scene.removeItem(cable_obj)
            
            # Remove from input pins list if it's a ComponentInputPin
            if item.__class__.__name__ == 'ComponentInputPin':
                for i in range(self.input_pins_list.count()):
                    list_item = self.input_pins_list.item(i)
                    if list_item.data(Qt.UserRole) == item:
                        self.input_pins_list.takeItem(i)
                        break
            
            # Remove from output pins list if it's a ComponentOutputPin
            if item.__class__.__name__ == 'ComponentOutputPin':
                for i in range(self.output_pins_list.count()):
                    list_item = self.output_pins_list.item(i)
                    if list_item.data(Qt.UserRole) == item:
                        self.output_pins_list.takeItem(i)
                        break
            
            self.design_scene.removeItem(item)
        
        self.update_preview()
    
    def update_preview(self):
        """Update the component preview"""
        self.preview_scene.clear()
        
        # Collect pin info
        input_pins = []
        for i in range(self.input_pins_list.count()):
            item = self.input_pins_list.item(i)
            input_pins.append({"name": item.text()})
        
        output_pins = []
        for i in range(self.output_pins_list.count()):
            item = self.output_pins_list.item(i)
            output_pins.append({"name": item.text()})
        
        # Create preview component
        component_data = {
            "name": self.component_name,
            "input_pins": input_pins,
            "output_pins": output_pins
        }
        
        if input_pins or output_pins:
            preview_comp = CustomComponent(component_data)
            preview_comp.setPos(20, 10)
            # Disable movement in preview
            preview_comp.setFlag(QGraphicsItem.ItemIsMovable, False)
            preview_comp.setFlag(QGraphicsItem.ItemIsSelectable, False)
            self.preview_scene.addItem(preview_comp)
    
    def save_component(self):
        """Save the component to a file"""
        if not self.component_name:
            QMessageBox.warning(self, "Error", "Please enter a component name.")
            return
        
        if self.input_pins_list.count() == 0 and self.output_pins_list.count() == 0:
            QMessageBox.warning(self, "Error", "Please add at least one input or output pin.")
            return
        
        # Collect component data
        component_data = {
            "type": "custom_component_definition",
            "name": self.component_name,
            "input_pins": [],
            "output_pins": [],
            "circuit": {"components": []}
        }
        
        # Collect input pins - sort by Y position for consistent ordering
        input_pins_with_pos = []
        for i in range(self.input_pins_list.count()):
            item = self.input_pins_list.item(i)
            comp = item.data(Qt.UserRole)
            input_pins_with_pos.append({
                "name": item.text(),
                "position_x": comp.pos().x() if comp else 0,
                "position_y": comp.pos().y() if comp else 0
            })
        # Sort by Y position (top to bottom)
        input_pins_with_pos.sort(key=lambda x: x['position_y'])
        component_data["input_pins"] = input_pins_with_pos
        
        # Collect output pins - sort by Y position for consistent ordering
        output_pins_with_pos = []
        for i in range(self.output_pins_list.count()):
            item = self.output_pins_list.item(i)
            comp = item.data(Qt.UserRole)
            output_pins_with_pos.append({
                "name": item.text(),
                "position_x": comp.pos().x() if comp else 0,
                "position_y": comp.pos().y() if comp else 0
            })
        # Sort by Y position (top to bottom)
        output_pins_with_pos.sort(key=lambda x: x['position_y'])
        component_data["output_pins"] = output_pins_with_pos
        
        # Collect circuit components
        for item in self.design_scene.items():
            if hasattr(item, 'to_json') and item.__repr__() == "component":
                component_data["circuit"]["components"].append(item.to_json())
        
        # Save to file
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Component",
            f"{self.component_name}.comp",
            "Component Files (*.comp);;All Files (*)"
        )
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(component_data, f, indent=4)
            QMessageBox.information(self, "Success", f"Component '{self.component_name}' saved successfully!")
            self.accept()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogicSimulator()
    
    window.show()


    sys.exit(app.exec_())

