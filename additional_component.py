import sys
from PyQt5.QtWidgets import (
    QGraphicsRectItem ,QGraphicsItem,QGraphicsTextItem
    )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor,QPen,QPainter



class pin_with_label(QGraphicsRectItem):
    def __init__(self,  x = 0, y = 0, w = 5, h = 5,label = "" ):
        super().__init__(x, y, w, h)
        
        self.x = x
        self.y = y
        self.label = label
        
        self.text = QGraphicsTextItem(self.label)
        self.text.setParentItem(self)
        #self.text.setScale()
        self.text.setPos(5,-10)
        self.setBrush(QBrush(QColor(255,0,0)))
    
    def set_text_pos(self,location:str):
        
        if location == 'left':
            x,y = 10,-10

        if location == 'right':
            x,y = -35,-10

        if location == 'top':
            x,y = -10,10

        if location == 'bottom':
            x,y = -10,-20
        
        self.text.setPos( x ,   y )


       

        
        

  
    
class general_component_template(QGraphicsRectItem):
    

    def __init__(self,  x = 0, y = 0, w = 150, h = 150):
        super().__init__(x, y, w, h)
        
        self.state = 0
        self.my_name = ""
        self.text = QGraphicsTextItem(self.my_name)
        self.text.setParentItem(self)
        self.text.setScale(2)
        self.text.setPos(10,0)
        self.setBrush(QBrush(QColor(0,100,0)))
        #self.pin1 = pin_with_label(-10,0,label= "Q")
        #self.pin1.setParentItem(self)
        self.left_pins = []
        self.right_pins = []
        self.top_pins = []
        self.bottom_pins = []

    def change_pin_position_and_name(self,pin_name,position,new_name):
        if pin_name in self.left_pins:
            self.left_pins.remove(pin_name)
        if pin_name in self.right_pins:
            self.right_pins.remove(pin_name)
        if pin_name in self.top_pins:
            self.top_pins.remove(pin_name)
        if pin_name in self.bottom_pins:
            self.bottom_pins.remove(pin_name)
        

        new_name = pin_name if new_name == '' else new_name
        if position == 'right':
            self.right_pins.append(new_name)
        
        if position == 'left':
            self.left_pins.append(new_name)
        
        if position == 'bottom':
            self.bottom_pins.append(new_name)
        
        if position == 'top':
            self.top_pins.append(new_name)
        self.locate_pins()
        
        

    

    def locate_pins(self):
        w,h = self.rect().width(),self.rect().height()
        pin_count = len(self.left_pins)
        for i in range(pin_count):
            self.left_pins[i].setPos(-10,((h//pin_count))*i)
            self.left_pins[i].set_text_pos('left')
            self.left_pins[i].setParentItem(self)

        pin_count = len(self.right_pins)
        for i in range(pin_count):
            self.right_pins[i].setPos(w + 10,((h//pin_count))*i)
            self.right_pins[i].set_text_pos('right')
            self.right_pins[i].setParentItem(self)

        pin_count = len(self.bottom_pins)
        for i in range(pin_count):
            self.bottom_pins[i].setPos(((w//pin_count))*i,h+5)
            self.bottom_pins[i].set_text_pos('bottom')
            self.bottom_pins[i].setParentItem(self)

        pin_count = len(self.top_pins)
        for i in range(pin_count):
            self.top_pins[i].setPos(((w//pin_count))*i,-5)
            self.top_pins[i].set_text_pos('top')
            self.top_pins[i].setParentItem(self)
        
    

    def set_my_pin_list(self,list_name:str,liste:list):
        if list_name == "left":
            for i in self.left_pins:
                i.setParentItem(None)
            self.left_pins = liste
        if list_name == "right":
            for i in self.right_pins:
                i.setParentItem(None)
            self.right_pins = liste
        if list_name == "top":
            for i in self.top_pins:
                i.setParentItem(None)
            self.top_pins = liste
        if list_name == "bottom":
            for i in self.bottom_pins:
                i.setParentItem(None)
            self.bottom_pins = liste
        
    

        
    
    


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
    
 
