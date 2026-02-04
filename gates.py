import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGraphicsView, QGraphicsScene,QGraphicsRectItem,QGraphicsLineItem,QGraphicsItem,QGraphicsTextItem,QGraphicsEllipseItem,
    QGraphicsPathItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor,QPen,QPainter, QPainterPath


# ==================== PROFESSIONAL GATE SHAPES ====================

class GateShape(QGraphicsPathItem):
    """Base class for professional IEEE-style gate shapes"""
    def __init__(self, w=100, h=50):
        super().__init__()
        self.w = w
        self.h = h
        # No flags - shape should move with parent, not independently
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setPen(QPen(QColor(40, 40, 40), 2))
        self.setBrush(QBrush(QColor(240, 245, 250)))
        
    def create_path(self):
        """Override in subclasses to create specific gate shapes"""
        pass


class ANDGateShape(GateShape):
    """Professional AND gate shape (D-shaped)"""
    def __init__(self, w=100, h=50):
        super().__init__(w, h)
        self.create_path()
        
    def create_path(self):
        path = QPainterPath()
        # Left side (straight line)
        path.moveTo(0, 0)
        path.lineTo(self.w * 0.5, 0)
        # Right side (curved arc)
        path.arcTo(self.w * 0.5 - self.h/2, 0, self.h, self.h, 90, -180)
        # Bottom
        path.lineTo(0, self.h)
        path.closeSubpath()
        self.setPath(path)


class ORGateShape(GateShape):
    """Professional OR gate shape (curved input, pointed output)"""
    def __init__(self, w=100, h=50):
        super().__init__(w, h)
        self.create_path()
        
    def create_path(self):
        path = QPainterPath()
        # Start at top-left
        path.moveTo(0, 0)
        # Top curve to output point
        path.quadTo(self.w * 0.6, 0, self.w, self.h / 2)
        # Bottom curve from output point
        path.quadTo(self.w * 0.6, self.h, 0, self.h)
        # Left curved indent (input side)
        path.quadTo(self.w * 0.2, self.h / 2, 0, 0)
        self.setPath(path)


class NOTGateShape(GateShape):
    """Professional NOT gate shape (triangle with bubble)"""
    def __init__(self, w=100, h=50):
        super().__init__(w, h)
        self.bubble_radius = 6
        self.create_path()
        
    def create_path(self):
        path = QPainterPath()
        # Triangle
        path.moveTo(0, 0)
        path.lineTo(self.w - self.bubble_radius * 2, self.h / 2)
        path.lineTo(0, self.h)
        path.closeSubpath()
        # Bubble (inversion circle)
        bubble_x = self.w - self.bubble_radius * 2
        bubble_y = self.h / 2 - self.bubble_radius
        path.addEllipse(bubble_x, bubble_y, self.bubble_radius * 2, self.bubble_radius * 2)
        self.setPath(path)


class NANDGateShape(GateShape):
    """Professional NAND gate shape (AND with bubble)"""
    def __init__(self, w=100, h=50):
        super().__init__(w, h)
        self.bubble_radius = 6
        self.create_path()
        
    def create_path(self):
        path = QPainterPath()
        # AND body (shortened to accommodate bubble)
        body_width = self.w - self.bubble_radius * 2
        path.moveTo(0, 0)
        path.lineTo(body_width * 0.5, 0)
        path.arcTo(body_width * 0.5 - self.h/2, 0, self.h, self.h, 90, -180)
        path.lineTo(0, self.h)
        path.closeSubpath()
        # Bubble
        bubble_x = body_width + self.h/2 - self.bubble_radius
        bubble_y = self.h / 2 - self.bubble_radius
        path.addEllipse(bubble_x, bubble_y, self.bubble_radius * 2, self.bubble_radius * 2)
        self.setPath(path)


class NORGateShape(GateShape):
    """Professional NOR gate shape (OR with bubble)"""
    def __init__(self, w=100, h=50):
        super().__init__(w, h)
        self.bubble_radius = 6
        self.create_path()
        
    def create_path(self):
        path = QPainterPath()
        body_width = self.w - self.bubble_radius * 2
        # Start at top-left
        path.moveTo(0, 0)
        # Top curve to output point
        path.quadTo(body_width * 0.6, 0, body_width, self.h / 2)
        # Bottom curve from output point
        path.quadTo(body_width * 0.6, self.h, 0, self.h)
        # Left curved indent
        path.quadTo(body_width * 0.2, self.h / 2, 0, 0)
        # Bubble
        bubble_x = body_width
        bubble_y = self.h / 2 - self.bubble_radius
        path.addEllipse(bubble_x, bubble_y, self.bubble_radius * 2, self.bubble_radius * 2)
        self.setPath(path)


class XORGateShape(GateShape):
    """Professional XOR gate shape (OR with extra curve)"""
    def __init__(self, w=100, h=50):
        super().__init__(w, h)
        self.create_path()
        
    def create_path(self):
        path = QPainterPath()
        offset = 8  # Distance for the extra curve
        # Main OR shape
        path.moveTo(offset, 0)
        path.quadTo(self.w * 0.6, 0, self.w, self.h / 2)
        path.quadTo(self.w * 0.6, self.h, offset, self.h)
        path.quadTo(offset + self.w * 0.2, self.h / 2, offset, 0)
        # Extra curve on the left (XOR identifier)
        path.moveTo(0, 0)
        path.quadTo(self.w * 0.2, self.h / 2, 0, self.h)
        self.setPath(path)


class XNORGateShape(GateShape):
    """Professional XNOR gate shape (XOR with bubble)"""
    def __init__(self, w=100, h=50):
        super().__init__(w, h)
        self.bubble_radius = 6
        self.create_path()
        
    def create_path(self):
        path = QPainterPath()
        offset = 8
        body_width = self.w - self.bubble_radius * 2
        # Main OR shape (shortened)
        path.moveTo(offset, 0)
        path.quadTo(body_width * 0.6, 0, body_width, self.h / 2)
        path.quadTo(body_width * 0.6, self.h, offset, self.h)
        path.quadTo(offset + body_width * 0.2, self.h / 2, offset, 0)
        # Extra curve on the left (XOR identifier)
        path.moveTo(0, 0)
        path.quadTo(body_width * 0.2, self.h / 2, 0, self.h)
        # Bubble
        bubble_x = body_width
        bubble_y = self.h / 2 - self.bubble_radius
        path.addEllipse(bubble_x, bubble_y, self.bubble_radius * 2, self.bubble_radius * 2)
        self.setPath(path)


class BufferGateShape(GateShape):
    """Professional Buffer gate shape (triangle without bubble)"""
    def __init__(self, w=100, h=50):
        super().__init__(w, h)
        self.create_path()
        
    def create_path(self):
        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(self.w, self.h / 2)
        path.lineTo(0, self.h)
        path.closeSubpath()
        self.setPath(path)

class cable(QGraphicsLineItem):
    """Professional wire/cable connection"""
    def __init__(self,x1 = 0,y1= 0,x2= 0,y2= 0):
        super().__init__(x1,y1,x2,y2)
        self.joints = []
        self.input_source = None
        self.logic_value = False
        self._update_cable_style()

    def _update_cable_style(self):
        """Update cable appearance based on logic value"""
        if self.logic_value:
            # Active HIGH - bright green with thicker line
            pen = QPen(QColor(50, 205, 50), 3)  # Lime green
        else:
            # LOW - darker muted color
            pen = QPen(QColor(80, 80, 80), 2)  # Dark gray
        self.setPen(pen)

    def set_logic_value(self,value,trigerred_pin,feed_back_control_set2):
        self.logic_value = value
        self._update_cable_style()
        i:cable
        for i in self.joints:
            if i == self.input_source:
                continue
            if i == trigerred_pin:
                continue
            i.set_logic_value(value,feed_back_control_set2.copy())

    def set_logic_value2(self,value,trigerred_pin,topological_queue:list,feed_back_control_set2):
        self.logic_value = value
        self._update_cable_style()
        i:cable
        for i in self.joints:
            if i == self.input_source:
                continue
            if i == trigerred_pin:
                continue

            topological_queue.append([i,value,feed_back_control_set2.copy()])
        
    
    def connect_two_pins(self,pin1:'pin',pin2:'pin'):
        self.joints.append(pin1)
        self.joints.append(pin2)
        pin1.lines.append([self,'start'])
        pin2.lines.append([self,'end'])
        
        

    
    
    
    
class logic_gate(QGraphicsRectItem):
    
    def __init__(self,  x = 0, y = 0, w = 50, h = 50, use_professional_shape=True):
        super().__init__(x, y, w, h)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges 
        )
        self.state = 0
        self.my_name = "gate"
        self.w = w
        self.h = h
        self.use_professional_shape = use_professional_shape
        self.gate_shape = None
        
        # Text label - positioned inside the gate
        self.text = QGraphicsTextItem(self.my_name)
        self.text.setParentItem(self)
        self.text.setScale(1)
        self.text.setDefaultTextColor(QColor(40, 40, 40))
        self.text.setPos(w/2 - 15, h/2 - 10)  # Inside the gate, centered
        
        # Default brush (hidden when using professional shape)
        self.setBrush(QBrush(QColor(0, 0, 0, 0)))  # Transparent
        self.setPen(QPen(QColor(0, 0, 0, 0)))  # Transparent
    
    def setup_professional_shape(self, shape_class):
        """Setup professional gate shape"""
        if self.use_professional_shape:
            self.gate_shape = shape_class(self.w, self.h)
            self.gate_shape.setParentItem(self)
            self.gate_shape.setPos(0, 0)
            # Keep text visible inside the gate
            self.text.setVisible(True)
            self.text.setZValue(1)  # Ensure text is above the shape
    
    def set_logic_value(self):
        pass

    def set_my_name(self,name):
        self.my_name = name
        self.text.setPlainText(self.my_name)
        # Center the text inside the gate
        text_width = self.text.boundingRect().width()
        text_height = self.text.boundingRect().height()
        self.text.setPos(self.w/2 - text_width/2, self.h/2 - text_height/2)
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
    """Professional input switch component"""
    def __init__(self,  x = 0, y = 0, w = 40, h = 40):
        super().__init__(x, y, w, h)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges 
        )
        self.state = False
        
        # Professional styling
        self.setBrush(QBrush(QColor(50, 50, 60)))
        self.setPen(QPen(QColor(30, 30, 40), 2))
        
        # Inner indicator circle
        self.indicator = QGraphicsEllipseItem(w*0.2, h*0.2, w*0.6, h*0.6, self)
        self.indicator.setBrush(QBrush(QColor(100, 100, 100)))
        self.indicator.setPen(QPen(QColor(60, 60, 60), 1))
        
        # Text label
        self.text = QGraphicsTextItem("0")
        self.text.setParentItem(self)
        self.text.setDefaultTextColor(QColor(255, 255, 255))
        self.text.setScale(1.5)
        self.text.setPos(w*0.3, h*0.15)
        
        # Output pin
        self.output_pin = pin(w+3, h//2-3, 6, 6, is_input_pin=False)
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
            self.state = self.state == False
            self.text.setPlainText(str(int(self.state)))
            # Professional color change for indicator
            if self.state:
                self.indicator.setBrush(QBrush(QColor(0, 220, 0)))  # Bright green when ON
            else:
                self.indicator.setBrush(QBrush(QColor(100, 100, 100)))  # Gray when OFF
            pin.feed_back_control_set.clear()
            topological_queue = []
            topological_queue.append([self.output_pin,self.state,set()])

            while len(topological_queue) > 0:
                component,value,feed_back_control_set2 = topological_queue.pop()
                component.set_logic_value2(value,topological_queue,feed_back_control_set2.copy())
                print(component)
        
        if event.button() == Qt.RightButton:
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

   



class pin(QGraphicsEllipseItem):
    """Professional circular pin connector"""
    is_clicked = False
    is_drawing = False
    start_pos = [0,0]
    line = cable(start_pos[0],start_pos[1],start_pos[0],start_pos[1])
    pen = QPen(QColor(80, 80, 80), 2)  # Professional gray for inactive wires
    line.setPen(pen)

    feed_back_control_set = set()
    id_number = 0

    
    
    

    def __init__(self,  x = 0, y = 0, w = 6, h = 6,is_input_pin = True):
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
        # Professional pin colors
        if is_input_pin:
            self.setBrush(QBrush(QColor(70, 130, 180)))  # Steel blue for input
        else:
            self.setBrush(QBrush(QColor(220, 20, 60)))   # Crimson for output
        self.setPen(QPen(QColor(40, 40, 40), 1))
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
    """Professional LED-style output indicator"""
    def __init__(self,  x = 0, y = 0, w = 40, h = 40):
        super().__init__(x, y, w, h)
        
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges 
        )
        self.out_line = None
        self.state = False
        
        # Professional LED styling
        self.setBrush(QBrush(QColor(60, 60, 60)))  # Dark when off
        self.setPen(QPen(QColor(30, 30, 40), 3))
        
        # Inner glow effect
        self.inner_glow = QGraphicsEllipseItem(w*0.15, h*0.15, w*0.7, h*0.7, self)
        self.inner_glow.setBrush(QBrush(QColor(80, 80, 80)))
        self.inner_glow.setPen(QPen(Qt.NoPen))
        
        # Text label
        self.text = QGraphicsTextItem("0")
        self.text.setParentItem(self)
        self.text.setDefaultTextColor(QColor(200, 200, 200))
        self.text.setScale(1.5)
        self.text.setPos(w*0.3, h*0.15)
        
        # Input pin
        self.input_pin = pin(-8, h//2-3, 6, 6, is_input_pin=True)
        self.input_pin.setParentItem(self)
            

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
        # Professional LED glow effect
        if self.state:
            self.setBrush(QBrush(QColor(0, 200, 0)))  # Bright green outer
            self.inner_glow.setBrush(QBrush(QColor(100, 255, 100)))  # Light green glow
            self.text.setDefaultTextColor(QColor(255, 255, 255))
        else:
            self.setBrush(QBrush(QColor(60, 60, 60)))  # Dark outer
            self.inner_glow.setBrush(QBrush(QColor(80, 80, 80)))  # Dark inner
            self.text.setDefaultTextColor(QColor(200, 200, 200))

    def set_logic_value2(self,value,topological_queue:list,feed_back_control_set2):
        self.state = value
        self.text.setPlainText(str(int(self.state)))
        # Professional LED glow effect
        if self.state:
            self.setBrush(QBrush(QColor(0, 200, 0)))
            self.inner_glow.setBrush(QBrush(QColor(100, 255, 100)))
            self.text.setDefaultTextColor(QColor(255, 255, 255))
        else:
            self.setBrush(QBrush(QColor(60, 60, 60)))
            self.inner_glow.setBrush(QBrush(QColor(80, 80, 80)))
            self.text.setDefaultTextColor(QColor(200, 200, 200))
    

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pass  # Output only shows state, no toggle
            
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
        self.setup_professional_shape(ANDGateShape)
        # Pin positions adjusted for professional shape
        self.input_pin1 = pin(-10, h*0.25, is_input_pin=True)
        self.input_pin2 = pin(-10, h*0.75, is_input_pin=True)
        self.output_pin = pin(w+5, h//2, is_input_pin=False)
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
        self.setup_professional_shape(ORGateShape)
        # Pin positions adjusted for OR gate curved input
        self.input_pin1 = pin(-5, h*0.25, is_input_pin=True)
        self.input_pin2 = pin(-5, h*0.75, is_input_pin=True)
        self.output_pin = pin(w+5, h//2, is_input_pin=False)
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
    def __init__(self, x=0, y=0, w=80, h=50):
        super().__init__(x, y, w, h)
        self.set_my_name("NOT")
        self.setup_professional_shape(NOTGateShape)
        # Pin positions for triangle shape with bubble
        self.input_pin1 = pin(-10, h//2, is_input_pin=True)
        self.output_pin = pin(w+5, h//2, is_input_pin=False)
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
        self.setup_professional_shape(NANDGateShape)
        # Pin positions for NAND (AND with bubble)
        self.input_pin1 = pin(-10, h*0.25, is_input_pin=True)
        self.input_pin2 = pin(-10, h*0.75, is_input_pin=True)
        self.output_pin = pin(w+5, h//2, is_input_pin=False)
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
        self.setup_professional_shape(NORGateShape)
        # Pin positions for NOR (OR with bubble)
        self.input_pin1 = pin(-5, h*0.25, is_input_pin=True)
        self.input_pin2 = pin(-5, h*0.75, is_input_pin=True)
        self.output_pin = pin(w+5, h//2, is_input_pin=False)
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
        self.setup_professional_shape(XORGateShape)
        # Pin positions for XOR (OR with extra curve)
        self.input_pin1 = pin(-5, h*0.25, is_input_pin=True)
        self.input_pin2 = pin(-5, h*0.75, is_input_pin=True)
        self.output_pin = pin(w+5, h//2, is_input_pin=False)
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





class seven_segment_display(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=150):
        super().__init__(x, y, w, h)
        self.set_my_name("")
        self.setBrush(QBrush(QColor(0, 0, 0)))
        self.segments = []
        self.input_pins = []
        self.create_segments(w, h)
        self.create_input_pins(w, h)


    def create_segments(self, w, h):
        segment_positions = [
            (10, 5, w - 20, 10),  # Top
            (w - 15, 15, 10, h // 2 - 20),  # Top-right
            (w - 15, h // 2 + 10, 10, h // 2 - 20),  # Bottom-right
            (10, h - 15, w - 20, 10),  # Bottom
            (5, h // 2 + 10, 10, h // 2 - 20),  # Bottom-left
            (5, 15, 10, h // 2 - 20),  # Top-left
            (10, h // 2 - 5, w - 20, 10),  # Middle
        ]
        for x, y, w, h in segment_positions:
            segment = QGraphicsRectItem(x, y, w, h, self)
            segment.setBrush(QBrush(QColor(50, 50, 50)))
            self.segments.append(segment)
            segment.setParentItem(self)

    def create_input_pins(self, w, h):
        for i in range(7):
            input_pin = pin(-15, 10 + i * 20, 5, 5, is_input_pin=True)
            input_pin.setParentItem(self)
            self.input_pins.append(input_pin)

    def get_pins(self):
        return self.input_pins

    def set_logic_value(self, value, feed_back_control_set2):
        for i, segment in enumerate(self.segments):
            if i < len(self.input_pins):
                segment.setBrush(
                    QBrush(QColor(255, 0, 0) if self.input_pins[i].logic_value else QColor(50, 50, 50))
                )

    def set_logic_value2(self, value, topological_queue: list, feed_back_control_set2):
        for i, segment in enumerate(self.segments):
            if i < len(self.input_pins):
                segment.setBrush(
                    QBrush(QColor(255, 0, 0) if self.input_pins[i].logic_value else QColor(50, 50, 50))
                )
               
    def to_json(self):
        my_json = {}
        my_json["type"] = "seven_segment_display"
        my_json["position_x"] = self.pos().x()
        my_json["position_y"] = self.pos().y()
        pin_values = [pin.to_json() for pin in self.input_pins]
        my_json["pins"] = pin_values
        return my_json

    def __repr__(self):
        return "component"

    def __str__(self):
        return "7-Segment Display"
    



class decoder_7_segment(logic_gate):
    def __init__(self, x=0, y=0, w=150, h=200):
        super().__init__(x, y, w, h, use_professional_shape=False)
        self.set_my_name("Decoder")
        self.input_pins = []
        self.output_pins = []
        self.create_input_pins(w, h)
        self.create_output_pins(w, h)
    
    def paint(self, painter, option, widget):
        # Draw gray filled rounded rectangle like custom components
        painter.setBrush(QBrush(QColor(180, 180, 180)))
        painter.setPen(QPen(QColor(60, 60, 60), 2))
        painter.drawRoundedRect(0, 0, int(self.w), int(self.h), 8, 8)
        
        # Draw pin labels
        painter.setPen(QPen(QColor(40, 40, 40)))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        
        # Input pin labels (D3, D2, D1, D0)
        input_labels = ['D3', 'D2', 'D1', 'D0']
        for i, label in enumerate(input_labels):
            painter.drawText(5, 15 + i * 20, label)
        
        # Output pin labels (a-g)
        output_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        for i, label in enumerate(output_labels):
            painter.drawText(int(self.w) - 20, 15 + i * 20, label)

    def create_input_pins(self, w, h):
        for i in range(4):  # 4 input pins for binary input
            input_pin = pin(-15, 10 + i * 20, 5, 5, is_input_pin=True)
            input_pin.setParentItem(self)
            self.input_pins.append(input_pin)

    def create_output_pins(self, w, h):
        for i in range(7):  # 7 output pins for 7-segment display
            output_pin = pin(w + 10, 10 + i * 20, 5, 5, is_input_pin=False)
            output_pin.setParentItem(self)
            self.output_pins.append(output_pin)

    def get_pins(self):
        return self.input_pins + self.output_pins

    def set_logic_value(self, value, feed_back_control_set2):
        binary_value = (
            self.input_pins[0].logic_value << 3 |
            self.input_pins[1].logic_value << 2 |
            self.input_pins[2].logic_value << 1 |
            self.input_pins[3].logic_value
        )
        segment_values = self.get_segment_values(binary_value)
        for i, output_pin in enumerate(self.output_pins):
            output_pin.set_logic_value(segment_values[i], feed_back_control_set2.copy())

    def set_logic_value2(self, value, topological_queue: list, feed_back_control_set2):
        binary_value = (
            self.input_pins[0].logic_value << 3 |
            self.input_pins[1].logic_value << 2 |
            self.input_pins[2].logic_value << 1 |
            self.input_pins[3].logic_value
        )
        segment_values = self.get_segment_values(binary_value)
        for i, output_pin in enumerate(self.output_pins):
            topological_queue.append([output_pin, segment_values[i], feed_back_control_set2.copy()])

    def get_segment_values(self, binary_value):
        # Segment values for 0-9 in 7-segment display
        segment_map = [
            [1, 1, 1, 1, 1, 1, 0],  # 0
            [0, 1, 1, 0, 0, 0, 0],  # 1
            [1, 1, 0, 1, 1, 0, 1],  # 2
            [1, 1, 1, 1, 0, 0, 1],  # 3
            [0, 1, 1, 0, 0, 1, 1],  # 4
            [1, 0, 1, 1, 0, 1, 1],  # 5
            [1, 0, 1, 1, 1, 1, 1],  # 6
            [1, 1, 1, 0, 0, 0, 0],  # 7
            [1, 1, 1, 1, 1, 1, 1],  # 8
            [1, 1, 1, 1, 0, 1, 1],  # 9
            [1, 1, 1, 0, 1, 1, 1],  # A
            [0, 0, 1, 1, 1, 1, 1],  # B
            [1, 0, 0, 1, 1, 1, 0],  # C
            [0, 1, 1, 1, 1, 0, 1],  # D
            [1, 0, 0, 1, 1, 1, 1],  # E
            [1, 0, 0, 0, 1, 1, 1],  # F
        ]
        return segment_map[binary_value]

    def to_json(self):
        my_json = {}
        my_json["type"] = "decoder_7_segment"
        my_json["position_x"] = self.pos().x()
        my_json["position_y"] = self.pos().y()
        pin_values = [pin.to_json() for pin in self.input_pins + self.output_pins]
        my_json["pins"] = pin_values
        return my_json

    def __repr__(self):
        return "component"

    def __str__(self):
        return "Decoder for 7-Segment Display"



class t_latch(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=60):
        super().__init__(x, y, w, h, use_professional_shape=False)
        self.set_my_name("T Latch")
        self.input_t = pin(-10, 15, is_input_pin=True)
        self.input_enable = pin(-10, h - 15, is_input_pin=True)
        self.output_q = pin(w + 10, h // 2, is_input_pin=False)
        self.input_t.setParentItem(self)
        self.input_enable.setParentItem(self)
        self.output_q.setParentItem(self)
        self.q_state = False  # Internal state to hold the Q value
    
    def paint(self, painter, option, widget):
        # Draw gray filled rounded rectangle
        painter.setBrush(QBrush(QColor(180, 180, 180)))
        painter.setPen(QPen(QColor(60, 60, 60), 2))
        painter.drawRoundedRect(0, 0, int(self.w), int(self.h), 8, 8)
        
        # Draw pin labels
        painter.setPen(QPen(QColor(40, 40, 40)))
        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        
        # Input labels
        painter.drawText(5, 20, 'T')
        painter.drawText(5, int(self.h) - 10, 'EN')
        
        # Output label
        painter.drawText(int(self.w) - 18, int(self.h) // 2 + 5, 'Q')

    def get_pins(self):
        return [self.input_t, self.input_enable, self.output_q]

    def set_logic_value(self, value, feed_back_control_set2):
        if self.input_enable.logic_value:  # Only update state if Enable is True
            if self.input_t.logic_value:
                self.q_state = not self.q_state  # Toggle Q state
        self.output_q.set_logic_value(self.q_state, feed_back_control_set2.copy())

    def set_logic_value2(self, value, topological_queue: list, feed_back_control_set2):
        if self.input_enable.logic_value:  # Only update state if Enable is True
            if self.input_t.logic_value:
                self.q_state = not self.q_state  # Toggle Q state
        topological_queue.append([self.output_q, self.q_state, feed_back_control_set2.copy()])

    def to_json(self):
        my_json = {}
        my_json["type"] = "t_latch"
        my_json["position_x"] = self.pos().x()
        my_json["position_y"] = self.pos().y()
        pin_values = [pin.to_json() for pin in [self.input_t, self.input_enable, self.output_q]]
        my_json["pins"] = pin_values
        return my_json

    def __repr__(self):
        return "component"

    def __str__(self):
        return "T Latch"


class d_flip_flop(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=70):
        super().__init__(x, y, w, h, use_professional_shape=False)
        self.set_my_name("D FF")
        self.input_d = pin(-10, 20, is_input_pin=True)
        self.input_clk = pin(-10, h - 20, is_input_pin=True)
        self.output_q = pin(w + 10, 20, is_input_pin=False)
        self.output_q_bar = pin(w + 10, h - 20, is_input_pin=False)
        self.input_d.setParentItem(self)
        self.input_clk.setParentItem(self)
        self.output_q.setParentItem(self)
        self.output_q_bar.setParentItem(self)
        self.q_state = False
        self.prev_clk = False
    
    def paint(self, painter, option, widget):
        # Draw gray filled rounded rectangle
        painter.setBrush(QBrush(QColor(180, 180, 180)))
        painter.setPen(QPen(QColor(60, 60, 60), 2))
        painter.drawRoundedRect(0, 0, int(self.w), int(self.h), 8, 8)
        
        # Draw pin labels
        painter.setPen(QPen(QColor(40, 40, 40)))
        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        
        # Input labels
        painter.drawText(5, 25, 'D')
        painter.drawText(5, int(self.h) - 15, 'CLK')
        
        # Output labels
        painter.drawText(int(self.w) - 18, 25, 'Q')
        painter.drawText(int(self.w) - 18, int(self.h) - 15, "Q̄")

    def get_pins(self):
        return [self.input_d, self.input_clk, self.output_q, self.output_q_bar]

    def set_logic_value(self, value, feed_back_control_set2):
        # Rising edge detection
        if self.input_clk.logic_value and not self.prev_clk:
            self.q_state = self.input_d.logic_value
        self.prev_clk = self.input_clk.logic_value
        self.output_q.set_logic_value(self.q_state, feed_back_control_set2.copy())
        self.output_q_bar.set_logic_value(not self.q_state, feed_back_control_set2.copy())

    def set_logic_value2(self, value, topological_queue: list, feed_back_control_set2):
        if self.input_clk.logic_value and not self.prev_clk:
            self.q_state = self.input_d.logic_value
        self.prev_clk = self.input_clk.logic_value
        topological_queue.append([self.output_q, self.q_state, feed_back_control_set2.copy()])
        topological_queue.append([self.output_q_bar, not self.q_state, feed_back_control_set2.copy()])

    def to_json(self):
        my_json = {}
        my_json["type"] = "d_flip_flop"
        my_json["position_x"] = self.pos().x()
        my_json["position_y"] = self.pos().y()
        pin_values = [pin.to_json() for pin in self.get_pins()]
        my_json["pins"] = pin_values
        return my_json

    def __repr__(self):
        return "component"

    def __str__(self):
        return "D Flip-Flop"


class jk_flip_flop(logic_gate):
    def __init__(self, x=0, y=0, w=100, h=90):
        super().__init__(x, y, w, h, use_professional_shape=False)
        self.set_my_name("JK FF")
        self.input_j = pin(-10, 20, is_input_pin=True)
        self.input_clk = pin(-10, h // 2, is_input_pin=True)
        self.input_k = pin(-10, h - 20, is_input_pin=True)
        self.output_q = pin(w + 10, 25, is_input_pin=False)
        self.output_q_bar = pin(w + 10, h - 25, is_input_pin=False)
        self.input_j.setParentItem(self)
        self.input_clk.setParentItem(self)
        self.input_k.setParentItem(self)
        self.output_q.setParentItem(self)
        self.output_q_bar.setParentItem(self)
        self.q_state = False
        self.prev_clk = False
    
    def paint(self, painter, option, widget):
        # Draw gray filled rounded rectangle
        painter.setBrush(QBrush(QColor(180, 180, 180)))
        painter.setPen(QPen(QColor(60, 60, 60), 2))
        painter.drawRoundedRect(0, 0, int(self.w), int(self.h), 8, 8)
        
        # Draw pin labels
        painter.setPen(QPen(QColor(40, 40, 40)))
        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        
        # Input labels
        painter.drawText(5, 25, 'J')
        painter.drawText(5, int(self.h) // 2 + 5, 'CLK')
        painter.drawText(5, int(self.h) - 15, 'K')
        
        # Output labels
        painter.drawText(int(self.w) - 18, 30, 'Q')
        painter.drawText(int(self.w) - 18, int(self.h) - 20, "Q̄")

    def get_pins(self):
        return [self.input_j, self.input_clk, self.input_k, self.output_q, self.output_q_bar]

    def set_logic_value(self, value, feed_back_control_set2):
        # Rising edge detection
        if self.input_clk.logic_value and not self.prev_clk:
            j = self.input_j.logic_value
            k = self.input_k.logic_value
            if j and k:
                self.q_state = not self.q_state  # Toggle
            elif j:
                self.q_state = True  # Set
            elif k:
                self.q_state = False  # Reset
            # else: Hold (no change)
        self.prev_clk = self.input_clk.logic_value
        self.output_q.set_logic_value(self.q_state, feed_back_control_set2.copy())
        self.output_q_bar.set_logic_value(not self.q_state, feed_back_control_set2.copy())

    def set_logic_value2(self, value, topological_queue: list, feed_back_control_set2):
        if self.input_clk.logic_value and not self.prev_clk:
            j = self.input_j.logic_value
            k = self.input_k.logic_value
            if j and k:
                self.q_state = not self.q_state
            elif j:
                self.q_state = True
            elif k:
                self.q_state = False
        self.prev_clk = self.input_clk.logic_value
        topological_queue.append([self.output_q, self.q_state, feed_back_control_set2.copy()])
        topological_queue.append([self.output_q_bar, not self.q_state, feed_back_control_set2.copy()])

    def to_json(self):
        my_json = {}
        my_json["type"] = "jk_flip_flop"
        my_json["position_x"] = self.pos().x()
        my_json["position_y"] = self.pos().y()
        pin_values = [pin.to_json() for pin in self.get_pins()]
        my_json["pins"] = pin_values
        return my_json

    def __repr__(self):
        return "component"

    def __str__(self):
        return "JK Flip-Flop"
    

class four_bit_counter(logic_gate):
    def __init__(self, x=0, y=0, w=150, h=200):
        super().__init__(x, y, w, h, use_professional_shape=False)
        self.set_my_name("4-Bit Counter")
        self.input_increment = pin(-10, 10, 5, 5, is_input_pin=True)
        self.input_decrement = pin(-10, 40, 5, 5, is_input_pin=True)
        self.input_reset = pin(-10, 70, 5, 5, is_input_pin=True)
        self.output_pins = [pin(w + 10, 10 + i * 20, 5, 5, is_input_pin=False) for i in range(4)]
        self.input_increment.setParentItem(self)
        self.input_decrement.setParentItem(self)
        self.input_reset.setParentItem(self)
        for output_pin in self.output_pins:
            output_pin.setParentItem(self)
        self.counter_value = 0  # Internal counter state
    
    def paint(self, painter, option, widget):
        # Draw gray filled rounded rectangle like custom components
        painter.setBrush(QBrush(QColor(180, 180, 180)))
        painter.setPen(QPen(QColor(60, 60, 60), 2))
        painter.drawRoundedRect(0, 0, int(self.w), int(self.h), 8, 8)
        
        # Draw pin labels
        painter.setPen(QPen(QColor(40, 40, 40)))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        
        # Input pin labels
        painter.drawText(5, 15, 'INC')
        painter.drawText(5, 45, 'DEC')
        painter.drawText(5, 75, 'RST')
        
        # Output pin labels (Q0-Q3)
        for i in range(4):
            painter.drawText(int(self.w) - 25, 15 + i * 20, f'Q{i}')

    def get_pins(self):
        return [self.input_increment, self.input_decrement, self.input_reset] + self.output_pins

    def set_logic_value(self, value, feed_back_control_set2):
        if self.input_reset.logic_value:
            self.counter_value = 0
        elif self.input_increment.logic_value:
            self.counter_value = (self.counter_value + 1) % 16  # Increment and wrap around at 16
        elif self.input_decrement.logic_value:
            self.counter_value = (self.counter_value - 1) % 16  # Decrement and wrap around at 16

        # Update output pins
        for i, output_pin in enumerate(self.output_pins):
            output_pin.set_logic_value((self.counter_value >> i) & 1, feed_back_control_set2.copy())

    def set_logic_value2(self, value, topological_queue: list, feed_back_control_set2):
        if self.input_reset.logic_value:
            self.counter_value = 0
        elif self.input_increment.logic_value:
            self.counter_value = (self.counter_value + 1) % 16  # Increment and wrap around at 16
        elif self.input_decrement.logic_value:
            self.counter_value = (self.counter_value - 1) % 16  # Decrement and wrap around at 16

        # Update output pins
        for i, output_pin in enumerate(self.output_pins):
            topological_queue.append([output_pin, (self.counter_value >> i) & 1, feed_back_control_set2.copy()])

    def to_json(self):
        my_json = {}
        my_json["type"] = "four_bit_counter"
        my_json["position_x"] = self.pos().x()
        my_json["position_y"] = self.pos().y()
        pin_values = [pin.to_json() for pin in [self.input_increment, self.input_decrement, self.input_reset] + self.output_pins]
        my_json["pins"] = pin_values
        return my_json

    def __repr__(self):
        return "component"

    def __str__(self):
        return "4-Bit Counter"
    




class component_input_pin(QGraphicsRectItem):
    counter = 0

    def __init__(self,  x = 0, y = 0, w = 100, h = 50):
        super().__init__(x, y, w, h)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges 
        )
        self.id = component_input_pin.counter
        component_input_pin.counter +=1
        self.state = 0
        self.my_name = "in"+str(self.id)
        self.text = QGraphicsTextItem(self.my_name)
        self.text.setParentItem(self)
        self.text.setScale(2)
        self.text.setPos(10,0)
        self.setBrush(QBrush(QColor(0,100,0)))
        self.pin1 = pin(w+10,h//2,is_input_pin=True)
        self.pin1.setParentItem(self)
    
    

    def get_pins(self):
        return [self.pin1]


    def set_my_name(self,name):
        self.my_name = name
        self.text.setPlainText(self.my_name)



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


    
class component_output_pin(QGraphicsRectItem):
    counter = 0
    def __init__(self,  x = 0, y = 0, w = 100, h = 50):
        super().__init__(x, y, w, h)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges 
        )

        self.id = component_output_pin.counter
        component_output_pin.counter +=1
        self.state = 0
        self.my_name = "out"+str(self.id)
        self.text = QGraphicsTextItem(self.my_name)
        self.text.setParentItem(self)
        self.text.setScale(2)
        self.text.setPos(10,0)
        self.setBrush(QBrush(QColor(0,100,0)))
        self.pin1 = pin(-10,h//2,is_input_pin=False)
        self.pin1.setParentItem(self)
    
    

    def get_pins(self):
        return [self.pin1]

    def set_my_name(self,name):
        self.my_name = name
        self.text.setPlainText(self.my_name)



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
    





class compound_component(logic_gate):
    def __init__(self, x=0, y=0, w=150, h=150):
        super().__init__(x, y, w, h)
    


# ==================== CUSTOM COMPONENT SYSTEM ====================

class ComponentInputPin(QGraphicsRectItem):
    """Input pin for custom component design - represents an external input to the component"""
    def __init__(self, x=0, y=0, w=60, h=30):
        super().__init__(x, y, w, h)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.pin_name = "IN"
        self.w = w
        self.h = h
        
        # Professional styling - blue theme for input
        self.setBrush(QBrush(QColor(70, 130, 180)))
        self.setPen(QPen(QColor(40, 40, 40), 2))
        
        # Pin name label
        self.text = QGraphicsTextItem(self.pin_name)
        self.text.setParentItem(self)
        self.text.setDefaultTextColor(QColor(255, 255, 255))
        self.text.setPos(5, 5)
        
        # Output pin (connects to internal circuit)
        self.output_pin = pin(w + 5, h//2 - 3, 6, 6, is_input_pin=False)
        self.output_pin.setParentItem(self)
        
        # Logic state
        self.state = False

    def set_pin_name(self, name):
        self.pin_name = name
        self.text.setPlainText(name)

    def get_pins(self):
        return [self.output_pin]

    def to_json(self):
        return {
            "type": "component_input",
            "pin_name": self.pin_name,
            "position_x": self.pos().x(),
            "position_y": self.pos().y(),
            "output_pin": self.output_pin.to_json()
        }

    def __repr__(self):
        return "component"
    
    def __str__(self):
        return f"ComponentInput({self.pin_name})"


class ComponentOutputPin(QGraphicsRectItem):
    """Output pin for custom component design - represents an external output from the component"""
    def __init__(self, x=0, y=0, w=60, h=30):
        super().__init__(x, y, w, h)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.pin_name = "OUT"
        self.w = w
        self.h = h
        
        # Professional styling - red theme for output
        self.setBrush(QBrush(QColor(180, 70, 70)))
        self.setPen(QPen(QColor(40, 40, 40), 2))
        
        # Pin name label
        self.text = QGraphicsTextItem(self.pin_name)
        self.text.setParentItem(self)
        self.text.setDefaultTextColor(QColor(255, 255, 255))
        self.text.setPos(5, 5)
        
        # Input pin (connects from internal circuit)
        self.input_pin = pin(-8, h//2 - 3, 6, 6, is_input_pin=True)
        self.input_pin.setParentItem(self)
        
        # Logic state
        self.state = False

    def set_pin_name(self, name):
        self.pin_name = name
        self.text.setPlainText(name)

    def get_pins(self):
        return [self.input_pin]

    def set_logic_value(self, value, feed_back_control_set2):
        self.state = value
        if self.state:
            self.setBrush(QBrush(QColor(255, 100, 100)))
        else:
            self.setBrush(QBrush(QColor(180, 70, 70)))

    def set_logic_value2(self, value, topological_queue, feed_back_control_set2):
        self.state = value
        if self.state:
            self.setBrush(QBrush(QColor(255, 100, 100)))
        else:
            self.setBrush(QBrush(QColor(180, 70, 70)))

    def to_json(self):
        return {
            "type": "component_output",
            "pin_name": self.pin_name,
            "position_x": self.pos().x(),
            "position_y": self.pos().y(),
            "input_pin": self.input_pin.to_json()
        }

    def __repr__(self):
        return "component"
    
    def __str__(self):
        return f"ComponentOutput({self.pin_name})"


class CustomComponent(QGraphicsRectItem):
    """A custom component created by the user, displayed as a rectangle with pins"""
    def __init__(self, component_data, x=0, y=0):
        self.component_name = component_data.get('name', 'Custom')
        self.input_pins_data = component_data.get('input_pins', [])
        self.output_pins_data = component_data.get('output_pins', [])
        self.internal_circuit = component_data.get('circuit', {})
        
        # Calculate size based on pins
        num_inputs = len(self.input_pins_data)
        num_outputs = len(self.output_pins_data)
        max_pins = max(num_inputs, num_outputs, 1)
        
        w = 120
        h = max(60, max_pins * 25 + 20)
        
        super().__init__(x, y, w, h)
        self.w = w
        self.h = h
        
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsScenePositionChanges
        )
        
        # Professional styling
        self.setBrush(QBrush(QColor(200, 200, 220)))
        self.setPen(QPen(QColor(40, 40, 40), 2))
        
        # Component name label
        self.text = QGraphicsTextItem(self.component_name)
        self.text.setParentItem(self)
        self.text.setDefaultTextColor(QColor(40, 40, 40))
        text_width = self.text.boundingRect().width()
        self.text.setPos(w/2 - text_width/2, h/2 - 10)
        
        # Create input pins
        self.input_pins = []
        self.input_pin_names = []
        for i, pin_data in enumerate(self.input_pins_data):
            y_pos = 15 + i * 25
            p = pin(-8, y_pos, 6, 6, is_input_pin=True)
            p.setParentItem(self)
            self.input_pins.append(p)
            self.input_pin_names.append(pin_data.get('name', f'IN{i}'))
            
            # Pin label
            label = QGraphicsTextItem(pin_data.get('name', f'IN{i}'))
            label.setParentItem(self)
            label.setDefaultTextColor(QColor(60, 60, 60))
            label.setScale(0.8)
            label.setPos(5, y_pos - 5)
        
        # Create output pins
        self.output_pins = []
        self.output_pin_names = []
        for i, pin_data in enumerate(self.output_pins_data):
            y_pos = 15 + i * 25
            p = pin(w + 2, y_pos, 6, 6, is_input_pin=False)
            p.setParentItem(self)
            self.output_pins.append(p)
            self.output_pin_names.append(pin_data.get('name', f'OUT{i}'))
            
            # Pin label
            label = QGraphicsTextItem(pin_data.get('name', f'OUT{i}'))
            label.setParentItem(self)
            label.setDefaultTextColor(QColor(60, 60, 60))
            label.setScale(0.8)
            label_width = label.boundingRect().width() * 0.8
            label.setPos(w - label_width - 5, y_pos - 5)
        
        # Internal circuit components and connections
        self.internal_components = {}  # pin_id -> component
        self.internal_input_pins = {}  # name -> internal ComponentInputPin
        self.internal_output_pins = {}  # name -> internal ComponentOutputPin
        self.internal_gates = []
        self.internal_cables = []
        
        # Build internal circuit
        self._build_internal_circuit()

    def _build_internal_circuit(self):
        """Build the internal circuit from saved data"""
        if not self.internal_circuit:
            return
            
        components = self.internal_circuit.get('components', [])
        all_pins = {}
        line_list = set()
        
        for comp_data in components:
            comp_type = comp_data.get('type')
            
            if comp_type == 'component_input':
                # Create internal input handler
                pin_name = comp_data.get('pin_name', 'IN')
                output_pin_id = comp_data.get('output_pin', {}).get('id')
                self.internal_input_pins[pin_name] = {
                    'output_pin_id': output_pin_id,
                    'logic_value': False
                }
                out_pin_data = comp_data.get('output_pin', {})
                if out_pin_data.get('id') is not None:
                    all_pins[out_pin_data['id']] = {'type': 'component_input', 'name': pin_name, 'is_output': True}
                    for conn in out_pin_data.get('connections', []):
                        pid = out_pin_data['id']
                        line_list.add((pid, conn) if pid > conn else (conn, pid))
                        
            elif comp_type == 'component_output':
                # Create internal output handler
                pin_name = comp_data.get('pin_name', 'OUT')
                input_pin_id = comp_data.get('input_pin', {}).get('id')
                self.internal_output_pins[pin_name] = {
                    'input_pin_id': input_pin_id,
                    'logic_value': False
                }
                in_pin_data = comp_data.get('input_pin', {})
                if in_pin_data.get('id') is not None:
                    all_pins[in_pin_data['id']] = {'type': 'component_output', 'name': pin_name, 'is_output': False}
                    for conn in in_pin_data.get('connections', []):
                        pid = in_pin_data['id']
                        line_list.add((pid, conn) if pid > conn else (conn, pid))
                        
            elif comp_type in ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR']:
                # Create internal gate
                gate_info = {
                    'type': comp_type,
                    'pins': comp_data.get('pins', []),
                    'input_values': [False, False] if comp_type != 'NOT' else [False],
                    'output_value': False
                }
                self.internal_gates.append(gate_info)
                
                pins = comp_data.get('pins', [])
                for i, pin_data in enumerate(pins):
                    pin_id = pin_data.get('id')
                    if pin_id is not None:
                        all_pins[pin_id] = {
                            'type': 'gate',
                            'gate_index': len(self.internal_gates) - 1,
                            'pin_index': i,
                            'is_output': (i == len(pins) - 1)  # Last pin is output
                        }
                        for conn in pin_data.get('connections', []):
                            line_list.add((pin_id, conn) if pin_id > conn else (conn, pin_id))
            
            elif comp_type == 'custom_component':
                # Handle nested custom components
                import copy
                nested_circuit = comp_data.get('circuit', {})
                nested_input_info = []
                nested_output_info = []
                
                # Extract pin names and positions from nested circuit
                for cc in nested_circuit.get('components', []):
                    if cc.get('type') == 'component_input':
                        nested_input_info.append({
                            'name': cc.get('pin_name', 'IN'),
                            'position_y': cc.get('position_y', 0)
                        })
                    elif cc.get('type') == 'component_output':
                        nested_output_info.append({
                            'name': cc.get('pin_name', 'OUT'),
                            'position_y': cc.get('position_y', 0)
                        })
                
                # Sort by Y position (top to bottom)
                nested_input_info.sort(key=lambda x: x['position_y'])
                nested_output_info.sort(key=lambda x: x['position_y'])
                
                nested_input_pins = [{'name': p['name']} for p in nested_input_info]
                nested_output_pins = [{'name': p['name']} for p in nested_output_info]
                
                # Create name-to-id mapping from external pins
                # External input_pins and output_pins are in file order, need to match by index
                external_input_pins = comp_data.get('input_pins', [])
                external_output_pins = comp_data.get('output_pins', [])
                
                # The external pins should be in the same order as nested pins (sorted by Y)
                # So we can directly use them
                input_pin_ids = [p.get('id') for p in external_input_pins]
                output_pin_ids = [p.get('id') for p in external_output_pins]
                
                nested_data = {
                    'name': comp_data.get('component_name', 'Nested'),
                    'input_pins': nested_input_pins,
                    'output_pins': nested_output_pins,
                    'circuit': nested_circuit
                }
                
                # Store nested component info
                nested_comp_info = {
                    'type': 'nested_component',
                    'data': nested_data,
                    'input_pin_ids': input_pin_ids,
                    'output_pin_ids': output_pin_ids,
                    'input_pin_names': [p['name'] for p in nested_input_pins],
                    'output_pin_names': [p['name'] for p in nested_output_pins]
                }
                self.internal_gates.append(nested_comp_info)
                
                # Register input pins
                for pin_data in comp_data.get('input_pins', []):
                    pin_id = pin_data.get('id')
                    if pin_id is not None:
                        all_pins[pin_id] = {
                            'type': 'nested_input',
                            'gate_index': len(self.internal_gates) - 1,
                            'pin_id': pin_id
                        }
                        for conn in pin_data.get('connections', []):
                            line_list.add((pin_id, conn) if pin_id > conn else (conn, pin_id))
                
                # Register output pins
                for pin_data in comp_data.get('output_pins', []):
                    pin_id = pin_data.get('id')
                    if pin_id is not None:
                        all_pins[pin_id] = {
                            'type': 'nested_output',
                            'gate_index': len(self.internal_gates) - 1,
                            'pin_id': pin_id
                        }
                        for conn in pin_data.get('connections', []):
                            line_list.add((pin_id, conn) if pin_id > conn else (conn, pin_id))
        
        # Store connection info
        self.internal_connections = list(line_list)
        self.internal_pins = all_pins

    def get_pins(self):
        return self.input_pins + self.output_pins

    def set_logic_value(self, value, feed_back_control_set2):
        # Simulate internal circuit
        self._simulate_internal()

    def set_logic_value2(self, value, topological_queue, feed_back_control_set2):
        # Simulate internal circuit
        self._simulate_internal()
        # Propagate to output pins
        for i, out_pin in enumerate(self.output_pins):
            topological_queue.append([out_pin, out_pin.logic_value, feed_back_control_set2.copy()])

    def _simulate_internal(self):
        """Simulate the internal circuit based on input values"""
        if not self.internal_circuit:
            return
        
        # Step 1: Set input values from external input pins to internal input pins
        # Match by pin name (external pin name -> internal pin with same name)
        for i, ext_pin in enumerate(self.input_pins):
            if i < len(self.input_pin_names):
                pin_name = self.input_pin_names[i]
                if pin_name in self.internal_input_pins:
                    self.internal_input_pins[pin_name]['logic_value'] = ext_pin.logic_value
        
        # Step 2: Build a complete value propagation system
        pin_values = {}
        
        # Initialize with input values
        for name, data in self.internal_input_pins.items():
            pin_id = data.get('output_pin_id')
            if pin_id is not None:
                pin_values[pin_id] = data['logic_value']
        
        # Iteratively propagate until stable
        max_iterations = 100
        for iteration in range(max_iterations):
            changed = False
            
            # Propagate through all connections (before gate calculation)
            for conn in self.internal_connections:
                pin1, pin2 = conn
                
                # Get pin info to determine direction
                pin1_info = self.internal_pins.get(pin1, {})
                pin2_info = self.internal_pins.get(pin2, {})
                
                pin1_is_output = pin1_info.get('is_output', False) or pin1_info.get('type') == 'component_input' or pin1_info.get('type') == 'nested_output'
                pin2_is_output = pin2_info.get('is_output', False) or pin2_info.get('type') == 'component_input' or pin2_info.get('type') == 'nested_output'
                
                # Propagate from output pin to input pin
                if pin1_is_output and pin1 in pin_values:
                    if pin_values.get(pin2) != pin_values[pin1]:
                        pin_values[pin2] = pin_values[pin1]
                        changed = True
                elif pin2_is_output and pin2 in pin_values:
                    if pin_values.get(pin1) != pin_values[pin2]:
                        pin_values[pin1] = pin_values[pin2]
                        changed = True
                elif pin1 in pin_values and pin2 not in pin_values:
                    pin_values[pin2] = pin_values[pin1]
                    changed = True
                elif pin2 in pin_values and pin1 not in pin_values:
                    pin_values[pin1] = pin_values[pin2]
                    changed = True
            
            # Calculate gate outputs
            for gate_idx, gate in enumerate(self.internal_gates):
                gate_type = gate.get('type')
                
                # Handle nested custom components
                if gate_type == 'nested_component':
                    nested_data = gate.get('data', {})
                    input_pin_ids = gate.get('input_pin_ids', [])
                    output_pin_ids = gate.get('output_pin_ids', [])
                    input_pin_names = gate.get('input_pin_names', [])
                    output_pin_names = gate.get('output_pin_names', [])
                    
                    # Create temporary nested component for simulation
                    import copy
                    temp_data = copy.deepcopy(nested_data)
                    temp_comp = CustomComponent(temp_data)
                    
                    # Create name-to-index mapping for temp_comp pins
                    temp_input_name_to_idx = {name: idx for idx, name in enumerate(temp_comp.input_pin_names)}
                    temp_output_name_to_idx = {name: idx for idx, name in enumerate(temp_comp.output_pin_names)}
                    
                    # Set input values on nested component using name matching
                    for idx, pin_id in enumerate(input_pin_ids):
                        if idx < len(input_pin_names) and pin_id is not None:
                            pin_name = input_pin_names[idx]
                            temp_idx = temp_input_name_to_idx.get(pin_name)
                            if temp_idx is not None and temp_idx < len(temp_comp.input_pins):
                                temp_comp.input_pins[temp_idx].logic_value = pin_values.get(pin_id, False)
                    
                    # Simulate nested component
                    temp_comp._simulate_internal()
                    
                    # Get output values from nested component using name matching
                    for idx, pin_id in enumerate(output_pin_ids):
                        if idx < len(output_pin_names) and pin_id is not None:
                            pin_name = output_pin_names[idx]
                            temp_idx = temp_output_name_to_idx.get(pin_name)
                            if temp_idx is not None and temp_idx < len(temp_comp.output_pins):
                                new_output = temp_comp.output_pins[temp_idx].logic_value
                                if pin_values.get(pin_id) != new_output:
                                    pin_values[pin_id] = new_output
                                    changed = True
                    
                    continue
                
                pins = gate.get('pins', [])
                
                # Get input values for gate
                if gate_type == 'NOT':
                    if len(pins) >= 2:
                        in1_id = pins[0].get('id')
                        in1 = pin_values.get(in1_id, False)
                        new_output = not in1
                        output_pin_id = pins[1].get('id')
                else:
                    if len(pins) >= 3:
                        in1_id = pins[0].get('id')
                        in2_id = pins[1].get('id')
                        in1 = pin_values.get(in1_id, False)
                        in2 = pin_values.get(in2_id, False)
                        
                        if gate_type == 'AND':
                            new_output = in1 and in2
                        elif gate_type == 'OR':
                            new_output = in1 or in2
                        elif gate_type == 'NAND':
                            new_output = not (in1 and in2)
                        elif gate_type == 'NOR':
                            new_output = not (in1 or in2)
                        elif gate_type == 'XOR':
                            new_output = in1 != in2
                        else:
                            new_output = False
                        output_pin_id = pins[2].get('id')
                    else:
                        continue
                
                # Update gate output
                if gate['output_value'] != new_output:
                    gate['output_value'] = new_output
                    changed = True
                
                # Set output pin value
                if output_pin_id is not None:
                    if pin_values.get(output_pin_id) != new_output:
                        pin_values[output_pin_id] = new_output
                        changed = True
            
            # Propagate through all connections AGAIN (after gate calculation)
            for conn in self.internal_connections:
                pin1, pin2 = conn
                
                # Check which pin is an output pin (source) and propagate from it
                pin1_info = self.internal_pins.get(pin1, {})
                pin2_info = self.internal_pins.get(pin2, {})
                
                pin1_is_output = pin1_info.get('is_output', False) or pin1_info.get('type') == 'component_input'
                pin2_is_output = pin2_info.get('is_output', False) or pin2_info.get('type') == 'component_input'
                
                if pin1_is_output and pin1 in pin_values:
                    # pin1 is source, propagate to pin2
                    if pin_values.get(pin2) != pin_values[pin1]:
                        pin_values[pin2] = pin_values[pin1]
                        changed = True
                elif pin2_is_output and pin2 in pin_values:
                    # pin2 is source, propagate to pin1
                    if pin_values.get(pin1) != pin_values[pin2]:
                        pin_values[pin1] = pin_values[pin2]
                        changed = True
                elif pin1 in pin_values and pin2 not in pin_values:
                    pin_values[pin2] = pin_values[pin1]
                    changed = True
                elif pin2 in pin_values and pin1 not in pin_values:
                    pin_values[pin1] = pin_values[pin2]
                    changed = True
            
            if not changed:
                break
        
        # Step 3: Set external output pin values from internal output pins
        # Match by pin name (external pin name -> internal pin with same name)
        for i, ext_pin in enumerate(self.output_pins):
            if i < len(self.output_pin_names):
                pin_name = self.output_pin_names[i]
                if pin_name in self.internal_output_pins:
                    in_pin_id = self.internal_output_pins[pin_name].get('input_pin_id')
                    if in_pin_id is not None:
                        output_value = pin_values.get(in_pin_id, False)
                        ext_pin.logic_value = output_value
                        self.internal_output_pins[pin_name]['logic_value'] = output_value

    def to_json(self):
        return {
            "type": "custom_component",
            "component_name": self.component_name,
            "position_x": self.pos().x(),
            "position_y": self.pos().y(),
            "input_pins": [p.to_json() for p in self.input_pins],
            "output_pins": [p.to_json() for p in self.output_pins],
            "circuit": self.internal_circuit
        }

    def __repr__(self):
        return "component"
    
    def __str__(self):
        return f"CustomComponent({self.component_name})"
