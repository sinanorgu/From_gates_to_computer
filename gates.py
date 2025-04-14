import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGraphicsView, QGraphicsScene,QGraphicsRectItem,QGraphicsLineItem,QGraphicsItem,QGraphicsTextItem,QGraphicsEllipseItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor,QPen,QPainter

class cable(QGraphicsLineItem):
    def __init__(self,x1,y1,x2,y2):
        super().__init__(x1,y1,x2,y2)
        self.joints = []
        self.input_source = None
        self.logic_value = False
        self.setPen(QPen(QColor(0,255 if self.logic_value else 100,0),2))


        #self.setFlags( QGraphicsItem.ItemIsSelectable)

    def set_logic_value(self,value,trigerred_pin,feed_back_control_set2):
        self.logic_value = value
        self.setPen(QPen(QColor(0,255 if self.logic_value else 100,0),2))
        i:cable
        for i in self.joints:
            if i == self.input_source:
                continue
            if i == trigerred_pin:
                continue
            i.set_logic_value(value,feed_back_control_set2.copy())

    def set_logic_value2(self,value,trigerred_pin,topological_queue:list,feed_back_control_set2):
        self.logic_value = value
        self.setPen(QPen(QColor(0,255 if self.logic_value else 100,0),2))
        i:cable
        for i in self.joints:
            if i == self.input_source:
                continue
            if i == trigerred_pin:
                continue

            topological_queue.append([i,value,feed_back_control_set2.copy()])
        
    
    
    
    
    
    
class logic_gate(QGraphicsRectItem):
    def __init__(self,  x = 0, y = 0, w = 50, h = 50):
        super().__init__(x, y, w, h)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges 
        )
        self.state = 0
        self.my_name = "gate"
        self.text = QGraphicsTextItem(self.my_name)
        self.text.setParentItem(self)
        self.text.setScale(2)
        self.text.setPos(10,0)
        self.setBrush(QBrush(QColor(0,100,0)))
    
    
    def set_logic_value(self):
        pass

    def set_my_name(self,name):
        self.my_name = name
        self.text.setPlainText(self.my_name)
    def get_pins(self):
        pass

    def to_json(self):
        pins = self.get_pins()
        my_json = {}
        my_json["type"] = self.my_name

        my_json['position_x'] = self.pos().x()
        my_json['position_y'] = self.pos().y()
        
        pin_values = []
        for i in pins:
            pin_values.append(i.to_json())
        my_json["pins"] = pin_values
        return my_json

    def __repr__(self):
        return "component"
    def __str__(self):
        return self.my_name
    
 




class logic_input(QGraphicsRectItem):
    def __init__(self,  x = 0, y = 0, w = 50, h = 50):
        super().__init__(x, y, w, h)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges 
        )
        self.state = False
        self.text = QGraphicsTextItem(str(int(self.state)))
        self.text.setParentItem(self)
        self.text.setScale(2)
        self.text.setPos(10,0)
        self.setBrush(QBrush(QColor(0,100,0)))
        self.output_pin = pin(w+5,h//2,5,5,is_input_pin=False)
        self.output_pin.setBrush(QBrush(QColor(255,0,0)))
        self.output_pin.setParentItem(self)

    


    """ def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange:
            #print(f"Yeni konum: {value.x()}, {value.y()}")
            # Buraya senin istediğin fonksiyonu çağırabilirsin
            
                
                
        return super().itemChange(change, value)
     """


    def get_pins(self):
        return [self.output_pin]
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            #print("sol tik")
            self.state = self.state == False
            self.text.setPlainText(str(int(self.state)))
            #print(self.state)
            self.setBrush(QBrush(QColor(0,255 if self.state else 100 ,0)))
            pin.feed_back_control_set.clear()
            #self.output_pin.set_logic_value(self.state)
            topological_queue = []
            topological_queue.append([self.output_pin,self.state,set()])

            while len(topological_queue) > 0:
                component,value,feed_back_control_set2 = topological_queue.pop()
                component.set_logic_value2(value,topological_queue,feed_back_control_set2.copy())
                print(component)
        
        if event.button() == Qt.RightButton:
            #print("sagtik")
            #print(self.pos().x(),self.pos().y())
            #self.setPos(100,100)
            pass
        return super().mousePressEvent(event)
    
    def to_json(self):
        my_json = {}
        my_json["type"] = "input"
        my_json['position_x'] = self.pos().x()
        my_json['position_y'] = self.pos().y()

        my_json["output_pin"] = self.output_pin.to_json()
        return my_json

    def __repr__(self):
        return "component"
    
    def __str__(self):
        return "Input source"

   



class pin(QGraphicsRectItem):
    is_clicked = False
    is_drawing = False
    start_pos = [0,0]
    line = cable(start_pos[0],start_pos[1],start_pos[0],start_pos[1])
    pen = QPen(QColor(0,100,0),2)
    line.setPen( pen)

    feed_back_control_set = set()
    id_number = 0

    
    
    

    def __init__(self,  x = 0, y = 0, w = 5, h = 5,is_input_pin = True):
        super().__init__(x, y, w, h)
        self.connection = None
        self.is_input_pin = is_input_pin    
        self.logic_value = 0
        self.lines = []
        self.setFlags(
            QGraphicsItem.ItemSendsScenePositionChanges 
        )
        self.x = x
        self.y = y
        self.setBrush(QBrush(QColor(255,0,0)))
        self.id = pin.id_number
        pin.id_number+=1
        

    def to_json(self):
        my_json = {}
        my_json["is_input_pin"] = self.is_input_pin
        my_json['id'] = self.id
        connections = []
        
        for i in self.lines:
            
            other_id = i[0].joints[0].id if i[0].joints[1] == self else i[0].joints[1].id
            connections.append(other_id)

        my_json["connections"] = connections
        return my_json


    def set_logic_value(self,value,feed_back_control_set2=None):
        if feed_back_control_set2 is None:
            feed_back_control_set2 = set()

        if self not in feed_back_control_set2:

            feed_back_control_set2.add(self)
            self.logic_value = value
            if self.is_input_pin:
                self.parentItem().set_logic_value(value,feed_back_control_set2.copy())
            else:
                for i in self.lines:
                    i[0].set_logic_value(value,self,feed_back_control_set2.copy())
        else:
            pin.feed_back_control_set.clear()
            feed_back_control_set2.clear()


    def set_logic_value2(self,value,topological_queue:list,feed_back_control_set2=None):
        
        if feed_back_control_set2 is None:
            feed_back_control_set2 = set()

        if self not in feed_back_control_set2:
        
            self.logic_value = value
            feed_back_control_set2.add(self)
            
            if self.is_input_pin:
                topological_queue.append([self.parentItem(),value,feed_back_control_set2.copy()])
            else:
                for i in self.lines:
                    i[0].set_logic_value2(value,self,topological_queue,feed_back_control_set2.copy())
        else:
            pin.feed_back_control_set.clear()
            feed_back_control_set2.clear()
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            #print("bu pine tik")
            
            pin.is_clicked = True
            if pin.is_drawing == False:
                pin.is_drawing = True
                #print("position:",event.scenePos().x())
                pin.start_pos = [event.scenePos().x(),event.scenePos().y()]
                self.lines.append([pin.line,'start'])
                pin.line.joints.append(self)

            else:
                pin.is_drawing = False
                pin.is_clicked = False

                self.lines.append([pin.line,'end'])
                pin.line.joints.append(self)
                pin.start_pos = [0,0]
                pin.line = cable(pin.start_pos[0],pin.start_pos[1],pin.start_pos[0],pin.start_pos[1])
                pin.line.setPen(pin.pen)

            #print(pin.is_clicked)
        
        if event.button() == Qt.RightButton:
            print(self.pos().x(),self.pos().y(),self.x,self.y)


            
        return super().mousePressEvent(event)
    
    
    
    def itemChange(self, change, value):

        for i in self.lines:
            try:
                if i[1] == 'start':
                    i[0].setLine(value.x()+self.x+2,value.y()+self.y +2,i[0].line().x2(),i[0].line().y2())
                if i[1] == 'end':
                    i[0].setLine(i[0].line().x1(),i[0].line().y1(),value.x()+self.x+2,value.y()+self.y +2)
            except:
                pass
                #self.lines.remove(i)



        return super().itemChange(change, value)

    


class logic_output(QGraphicsEllipseItem):
    def __init__(self,  x = 0, y = 0, w = 50, h = 50):
        super().__init__(x, y, w, h)
        
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges 
        )
        self.out_line = None
        self.state = False
        self.text = QGraphicsTextItem(str(int(self.state)))
        self.input_pin = pin(-10,h//2,5,5,is_input_pin=True)
        
        self.input_pin.setParentItem(self)
        
        self.text.setParentItem(self)
        self.text.setScale(2)
        self.text.setPos(10,0)
        self.setBrush(QBrush(QColor(0,100,0)))
            

    def to_json(self):
        my_json = {}
        my_json["type"] = "output"
        my_json['position_x'] = self.pos().x()
        my_json['position_y'] = self.pos().y()

        my_json["input_pin"] = self.input_pin.to_json()
        return my_json
    def __repr__(self):
        return "component"
    
    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange:
            #print(f"Yeni konum: {value.x()}, {value.y()}")
            # Buraya senin istediğin fonksiyonu çağırabilirsin
            if self.out_line != None:
                x = self.line.line().p1().x()
                y = self.line.line().p1().y()
                self.out_line.setLine(x,y,value.x(),value.y())
                
                
        return super().itemChange(change, value)
    
    def set_logic_value(self,value,feed_back_control_set2):
        self.state = value
        self.text.setPlainText(str(int(self.state)))
        #print(self.state)
        self.setBrush(QBrush(QColor(0,255 if self.state else 100 ,0)))

    def set_logic_value2(self,value,topological_queue:list,feed_back_control_set2):
        self.state = value
        self.text.setPlainText(str(int(self.state)))
        #print(self.state)
        self.setBrush(QBrush(QColor(0,255 if self.state else 100 ,0)))
    

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            #print("sol tik")
            #self.state = False ==  self.state
            self.text.setPlainText(str(int(self.state)))
            #print(self.state)
            self.setBrush(QBrush(QColor(0,255 if self.state else 100 ,0)))
            
        return super().mousePressEvent(event)

    def get_pins(self):
        return [self.input_pin]

    

    
    """ def mouseMoveEvent(self, event):
        #print("mouse move calisiyor",event.pos().x(),event.pos().y())
        return super().mouseMoveEvent(event) """



class and_gate(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=50):
        super().__init__(x, y, w, h)
        self.set_my_name("AND")
        self.input_pin1 = pin(-10,0,is_input_pin=True)
        self.input_pin2 = pin(-10,h,is_input_pin=True)
        self.output_pin = pin(w+10,h//2,is_input_pin=False)
        self.input_pin1.setParentItem(self)
        self.input_pin2.setParentItem(self)
        self.output_pin.setParentItem(self)
        
    def get_pins(self):
        return [self.input_pin1,self.input_pin2,self.output_pin]


    def set_logic_value(self,value,feed_back_control_set2):
        output_value = self.input_pin1.logic_value and self.input_pin2.logic_value
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()   
    
    def set_logic_value2(self,value,topological_queue:list,feed_back_control_set2):
        output_value = self.input_pin1.logic_value and self.input_pin2.logic_value
        
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        topological_queue.append([self.output_pin,output_value,feed_back_control_set2.copy()])
        #self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()   
         
    



class or_gate(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=50):
        super().__init__(x, y, w, h)
        self.set_my_name("OR")
        self.input_pin1 = pin(-10,0,is_input_pin=True)
        self.input_pin2 = pin(-10,h,is_input_pin=True)
        self.output_pin = pin(w+10,h//2,is_input_pin=False)
        self.input_pin1.setParentItem(self)
        self.input_pin2.setParentItem(self)
        self.output_pin.setParentItem(self)
    
    def get_pins(self):
        return [self.input_pin1,self.input_pin2,self.output_pin]


    def set_logic_value(self,value,feed_back_control_set2):
        output_value = self.input_pin1.logic_value | self.input_pin2.logic_value
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()      
    
    def set_logic_value2(self,value,topological_queue:list,feed_back_control_set2):
        output_value = (self.input_pin1.logic_value or self.input_pin2.logic_value)
        
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        topological_queue.append([self.output_pin,output_value,feed_back_control_set2.copy()])
        #self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()    



class not_gate(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=50):
        super().__init__(x, y, w, h)
        self.set_my_name("NOT")
        self.input_pin1 = pin(-10,h//2,is_input_pin=True)
        self.output_pin = pin(w+10,h//2,is_input_pin=False)
        self.input_pin1.setParentItem(self)
        self.output_pin.setParentItem(self)
    
    def get_pins(self):
        return [self.input_pin1,self.output_pin]

    def set_logic_value(self,value,feed_back_control_set2):
        output_value = self.input_pin1.logic_value 
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        self.output_pin.set_logic_value(output_value == False,feed_back_control_set2.copy())
        return super().set_logic_value()  

    def set_logic_value2(self,value,topological_queue:list,feed_back_control_set2):
        output_value = self.input_pin1.logic_value == False
        
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        topological_queue.append([self.output_pin,output_value,feed_back_control_set2.copy()])
        #self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()    
    



class nand_gate(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=50):
        super().__init__(x, y, w, h)
        self.set_my_name("NAND")
        self.input_pin1 = pin(-10,0,is_input_pin=True)
        self.input_pin2 = pin(-10,h,is_input_pin=True)
        self.output_pin = pin(w+10,h//2,is_input_pin=False)
        self.input_pin1.setParentItem(self)
        self.input_pin2.setParentItem(self)
        self.output_pin.setParentItem(self)
        
    def get_pins(self):
        return [self.input_pin1,self.input_pin2,self.output_pin]


    def set_logic_value(self,value,feed_back_control_set2):
        output_value = (self.input_pin1.logic_value and self.input_pin2.logic_value) == False
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()    
    
    def set_logic_value2(self,value,topological_queue:list,feed_back_control_set2):
        output_value = (self.input_pin1.logic_value and self.input_pin2.logic_value) == False
        
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        topological_queue.append([self.output_pin,output_value,feed_back_control_set2.copy()])
        #self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()    
    
    


class nor_gate(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=50):
        super().__init__(x, y, w, h)
        self.set_my_name("NOR")
        self.input_pin1 = pin(-10,0,is_input_pin=True)
        self.input_pin2 = pin(-10,h,is_input_pin=True)
        self.output_pin = pin(w+10,h//2,is_input_pin=False)
        self.input_pin1.setParentItem(self)
        self.input_pin2.setParentItem(self)
        self.output_pin.setParentItem(self)
        
    def get_pins(self):
        return [self.input_pin1,self.input_pin2,self.output_pin]


    def set_logic_value(self,value,feed_back_control_set2):
        output_value = (self.input_pin1.logic_value or self.input_pin2.logic_value) == False
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()    
      
    def set_logic_value2(self,value,topological_queue:list,feed_back_control_set2):
        output_value = (self.input_pin1.logic_value or self.input_pin2.logic_value) == False
        
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        topological_queue.append([self.output_pin,output_value,feed_back_control_set2.copy()])
        #self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()    

class xor_gate(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=50):
        super().__init__(x, y, w, h)
        self.set_my_name("XOR")
        self.input_pin1 = pin(-10,0,is_input_pin=True)
        self.input_pin2 = pin(-10,h,is_input_pin=True)
        self.output_pin = pin(w+10,h//2,is_input_pin=False)
        self.input_pin1.setParentItem(self)
        self.input_pin2.setParentItem(self)
        self.output_pin.setParentItem(self)
        
    def get_pins(self):
        return [self.input_pin1,self.input_pin2,self.output_pin]


    def set_logic_value(self,value,feed_back_control_set2):
        output_value = (self.input_pin1.logic_value != self.input_pin2.logic_value)
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()     
       
    def set_logic_value2(self,value,topological_queue:list,feed_back_control_set2):
        output_value = (self.input_pin1.logic_value != self.input_pin2.logic_value) 
        
        
        #print("output value for and",self.input_pin1.logic_value,self.input_pin2.logic_value,output_value)
        topological_queue.append([self.output_pin,output_value,feed_back_control_set2.copy()])
        #self.output_pin.set_logic_value(output_value,feed_back_control_set2.copy())
        return super().set_logic_value()    

