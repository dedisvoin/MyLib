from GLib.window import Window
from GLib.drawing import *
from GLib.special_methods import *
from GLib.mathematics import *
from GLib.inputs import *
from GLib.text import *

EVENTS = Events()
EVENTS.add(Mouse(Mouse.bt_left, Mouse.click_event, 'lclick'))
EVENTS.add(Mouse(Mouse.bt_left, Mouse.press_event, 'lpress'))

class POSITIONS:
    CENTER = 'CENTER'
    CENTER_X = 'CENTER_X'
    CENTER_Y = 'CENTER_y'
    
    CENTER_PARENT = 'CENTER_PARENT'
    CENTER_PARENT_X = 'CENTER_PARENT_X'
    CENTER_PARENT_Y = 'CENTER_PARENT_Y'
    USING_PARENT_COORD_SYSTEM = 'USING_PARENT_COORD_SYSTEM'

class CONTAINED:
    USING_CONTAINER = 'USING_CONTAINER'
    
class SPECIAL_FLAGS:
    MOUSE_MOVING = 'MOUSE_MOVING'
    USING_FATHER_WIDTH = 'USING_FATHER_WIDTH'
    USING_FATHER_HEIGHT = 'USING_FATHER_HEIGHT'

class CONTAINED_TYPES:
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'

class Box:
    def __init__(self, 
                pos: list[int] = [1, 1], 
                size: list[int] = [1, 1], 
                color: list | str = 'gray',
                objects = [],
                radius = -1,
                flags: list = [],
                window: Window = None,
                contained_padding = 0,
                container_dy = 5,
                container_dx = 5,
                contained: bool = False,
                contained_type: CONTAINED_TYPES = CONTAINED_TYPES.VERTICAL,
                rendered: bool = True) -> None:
        
        self.__start_pos = pos
        self.__start_size = size
        self.__objects = objects
        self.__color = color
        self.__radius = radius
        self.__flags = flags
        self.__window = window
        
        self.__contained = contained
        self.__contained_type = contained_type
        
        self.__rendered = rendered
        
        self.__contained_padding = contained_padding
        self.__container_dy = container_dy
        self.__container_dx = container_dx
        
        self.__id = generate_id(self)
        self.__parent_object = None
        
        self.__clicked = False
        
        
        self.__at_size = [0, 0]
        self.__at_pos = [0, 0]
        
        self.init_start_values()
        self.set_all_objects_parent_id()
        print(self)
        
    def __str__(self) -> str:
        return f'''
{self.__class__.__name__} {self.__id=}
{self.__color=}
{self.__flags=}
{self.__start_pos=}
{self.__start_size=}
{self.__radius=}
{self.__at_pos=}
{self.__at_size=}
contained: {[obj.__class__.__name__ for obj in self.__objects]}

'''
        
    def set_parent(self, parent: Any):
        self.__parent_object = parent
    
    @property
    def center(self):
        return [self.__at_pos[0]+self.__at_size[0]/2,self.__at_pos[1]+self.__at_size[1]/2]
        
    @property
    def size(self):
        return self.__at_size
    
    @size.setter
    def size(self, size):
        self.__at_size = size
    
    @property
    def contained(self):
        return self.__contained
        
    @property
    def pos(self):
        return self.__at_pos
    
    @pos.setter
    def pos(self, pos):
        self.__at_pos = pos
    
    @property
    def color(self):
        return self.__color
    
    @property
    def radius(self):
        return self.__radius
        
    def init_start_values(self):
        self.__at_pos = copy(self.__start_pos)
        self.__at_size = copy(self.__start_size)
        
        self.__basik_pos = copy(self.__start_pos)
        self.__basik_size = copy(self.__start_size)
        
    def set_all_objects_parent_id(self):
        for obj in self.__objects:
            obj.set_parent(self)
        
    def update(self):
        
        mouse_speed = Mouse.speed
        
        if self.__parent_object is None:
            self.__at_pos = copy(self.__basik_pos)
            self.__at_size = copy(self.__basik_size)
        
        if POSITIONS.USING_PARENT_COORD_SYSTEM in self.__flags:
            parent_pos = self.__parent_object.pos
            self.__at_pos[0]=parent_pos[0]+self.__basik_pos[0]
            self.__at_pos[1]=parent_pos[1]+self.__basik_pos[1]
            
        
        if POSITIONS.CENTER in self.__flags:
            win_center = self.__window.center
            pos = [win_center[0]-self.__at_size[0]/2, win_center[1]-self.__at_size[1]/2]
            self.__at_pos = pos
        if POSITIONS.CENTER_X in self.__flags:
            win_center = self.__window.center
            self.__at_pos[0] = win_center[0]-self.__at_size[0]/2
        if POSITIONS.CENTER_Y in self.__flags:
            win_center = self.__window.center
            self.__at_pos[1] = win_center[1]-self.__at_size[1]/2
        
        
            
            
        if POSITIONS.CENTER_PARENT in self.__flags:
            parent_center = self.__parent_object.center
            pos = [parent_center[0]-self.__at_size[0]/2, parent_center[1]-self.__at_size[1]/2]
            self.__at_pos = pos
        if POSITIONS.CENTER_PARENT_X in self.__flags:
            parent_center = self.__parent_object.center
            self.__at_pos[0] = parent_center[0]-self.__at_size[0]/2
        if POSITIONS.CENTER_PARENT_Y in self.__flags:
            parent_center = self.__parent_object.center
            self.__at_pos[1] = parent_center[1]-self.__at_size[1]/2
        
        if CONTAINED.USING_CONTAINER in self.__flags:
            obj_count = 0
            for obj in self.__objects:
                if type(obj) != String:
                    obj_count+=1
            if self.__contained_type == CONTAINED_TYPES.VERTICAL:
                object_height = self.__at_size[1]/obj_count-self.__container_dy*2/obj_count+self.__contained_padding/obj_count
                for i, obj in enumerate(self.__objects):
                    if obj.contained and type(obj) != String:
                        self.__objects[i].size[1] = object_height-self.__contained_padding
                        self.__objects[i].pos[1] = self.__container_dy+self.__at_pos[1]+object_height*i
            elif self.__contained_type == CONTAINED_TYPES.HORIZONTAL:
                object_width = self.__at_size[0]/obj_count-self.__container_dx*2/obj_count+self.__contained_padding/obj_count
                for i, obj in enumerate(self.__objects):
                    if obj.contained and type(obj) != String:
                        self.__objects[i].size[0] = object_width-self.__contained_padding
                        self.__objects[i].pos[0] = self.__container_dx+self.__at_pos[0]+object_width*i
                
                
        if SPECIAL_FLAGS.MOUSE_MOVING in self.__flags:
            self.__at_pos = copy(self.__basik_pos)
            self.__at_size = copy(self.__basik_size)
            
            if in_rect(self.__at_pos, self.__at_size, Mouse.pos):
                if EVENTS.get('lclick'):
                    self.__clicked = True
            if not EVENTS.get('lpress'):
                self.__clicked = False
            
            if self.__clicked:
                self.__basik_pos[0]+=mouse_speed[0]
                self.__basik_pos[1]+=mouse_speed[1]
        
    def render(self, surf):
        if self.__rendered:
            Draw.draw_rect(surf, self.pos, self.size, self.color, radius=self.radius)

class String:
    def __init__(self, 
                pos: list[int] = [1, 1], 
                color: list | str = 'black',
                flags: list = [],
                window: Window = None,
                text: str = 'basik',
                font: str = 'arial',
                font_size: int = 10,
                font_bold: bool = False)-> None:
        
        self.__text = text
        self.__font = font
        self.__font_size = font_size
        self.__font_bold = font_bold
        
        self.__start_pos = pos
        self.__color = color
        self.__flags = flags
        self.__window = window
        
        self.__id = generate_id(self)
        self.__parent_object = None

        self.__clicked = False
        self.__contained = False
        
        
        self.__at_size = [0, 0]
        self.__at_pos = [0, 0]
        
        self.__text_obj = Text(self.__font, self.__font_size, self.__font_bold, False)
        self.__text_surf = self.__text_obj.render_text_surf(self.__text, self.__color)
        
        self.init_start_values()
        #self.set_all_objects_parent_id()
        print(self)
        
    def __str__(self) -> str:
        return f'''
{self.__class__.__name__} {self.__id=}
{self.__color=}
{self.__flags=}
{self.__start_pos=}
{self.__at_pos=}
{self.__at_size=}
{self.__font=}
{self.__font_size=}
{self.__text=}


'''
        
    def set_parent(self, parent: Any):
        self.__parent_object = parent
    
    @property
    def center(self):
        return [self.__at_pos[0]+self.__at_size[0]/2,self.__at_pos[1]+self.__at_size[1]/2]
        
    @property
    def size(self):
        return [*self.__text_surf.get_size()]
    
    @property
    def contained(self):
        return self.__contained
    
    @property
    def pos(self):
        return self.__at_pos
    
    @pos.setter
    def pos(self, pos):
        self.__at_pos = pos
        
    @property
    def at_size(self):
        return self.__at_size
    
    @at_size.setter
    def at_size(self, size):
        self.__at_size = size
    
    @property
    def color(self):
        return self.__color
    
    def init_start_values(self):
        self.__at_pos = copy(self.__start_pos)
        self.__at_size = copy(self.size)
        
        self.__basik_pos = copy(self.__start_pos)
        self.__basik_size = copy(self.size)
        
    def set_all_objects_parent_id(self):
        for obj in self.__objects:
            obj.set_parent(self)
        
    def update(self):
        
        mouse_speed = Mouse.speed
        
        if self.__parent_object is None:
            self.__at_pos = copy(self.__basik_pos)
            self.__at_size = copy(self.__basik_size)
        
        if POSITIONS.USING_PARENT_COORD_SYSTEM in self.__flags:
            parent_pos = self.__parent_object.pos
            self.__at_pos[0]=parent_pos[0]+self.__basik_pos[0]
            self.__at_pos[1]=parent_pos[1]+self.__basik_pos[1]
            
        
        if POSITIONS.CENTER in self.__flags:
            win_center = self.__window.center
            pos = [win_center[0]-self.__at_size[0]/2, win_center[1]-self.__at_size[1]/2]
            self.__at_pos = pos
        if POSITIONS.CENTER_X in self.__flags:
            win_center = self.__window.center
            self.__at_pos[0] = win_center[0]-self.__at_size[0]/2
        if POSITIONS.CENTER_Y in self.__flags:
            win_center = self.__window.center
            self.__at_pos[1] = win_center[1]-self.__at_size[1]/2
        
        
            
            
        if POSITIONS.CENTER_PARENT in self.__flags:
            parent_center = self.__parent_object.center
            pos = [parent_center[0]-self.__at_size[0]/2, parent_center[1]-self.__at_size[1]/2]
            self.__at_pos = pos
        if POSITIONS.CENTER_PARENT_X in self.__flags:
            parent_center = self.__parent_object.center
            self.__at_pos[0] = parent_center[0]-self.__at_size[0]/2
        if POSITIONS.CENTER_PARENT_Y in self.__flags:
            parent_center = self.__parent_object.center
            self.__at_pos[1] = parent_center[1]-self.__at_size[1]/2
                
        if SPECIAL_FLAGS.MOUSE_MOVING in self.__flags:
            self.__at_pos = copy(self.__basik_pos)
            self.__at_size = copy(self.__basik_size)
            
            if in_rect(self.__at_pos, self.__at_size, Mouse.pos):
                if EVENTS.get('lclick'):
                    self.__clicked = True
            if not EVENTS.get('lpress'):
                self.__clicked = False
            
            if self.__clicked:
                self.__basik_pos[0]+=mouse_speed[0]
                self.__basik_pos[1]+=mouse_speed[1]
        
    def render(self, surf):
        surf.blit(self.__text_surf, self.pos)
        
class TextButton:
    def __init__(self, 
                pos: list[int] = [1, 1], 
                size: list[int] = [1, 1], 
                color: list | str = 'green',
                color_hover: list | str = 'darkgreen',
                color_press: list | str = 'white',
                radius = -1,
                flags: list = [],
                window: Window = None,
                contained: bool = False,
                rendered: bool = True,
                text_obj: String = None) -> None:
        
        self.__start_pos = pos
        self.__start_size = size
        
        self.__color = color
        self.__hover_color = color_hover
        self.__press_color = color_press
        
        self.__radius = radius
        self.__flags = flags
        self.__window = window
        self.__contained = contained
        self.__text_obj = text_obj
        self.__text_obj.set_parent(self)
        self.__rendered = rendered
        
        
        self.__id = generate_id(self)
        self.__parent_object = None
        
        self.__clicked = False
        
        
        self.__at_size = [0, 0]
        self.__at_pos = [0, 0]
        
        self.init_start_values()
        #self.set_all_objects_parent_id()
        print(self)
        
    def __str__(self) -> str:
        return f'''
{self.__class__.__name__} {self.__id=}
{self.__color=}
{self.__flags=}
{self.__start_pos=}
{self.__start_size=}
{self.__radius=}
{self.__at_pos=}
{self.__at_size=}


'''
    
    def set_parent(self, parent: Any):
        self.__parent_object = parent
    
    @property
    def center(self):
        return [self.__at_pos[0]+self.__at_size[0]/2,self.__at_pos[1]+self.__at_size[1]/2]
    
    @property
    def size(self):
        return self.__at_size
    
    @size.setter
    def size(self, size):
        self.__at_size = size
    
    @property
    def contained(self):
        return self.__contained
        
    @property
    def pos(self):
        return self.__at_pos
    
    @pos.setter
    def pos(self, pos):
        self.__at_pos = pos
    
    @property
    def color(self):
        return self.__color
    
    @property
    def radius(self):
        return self.__radius
        
    def init_start_values(self):
        self.__at_pos = copy(self.__start_pos)
        self.__at_size = copy(self.__start_size)
        
        self.__basik_pos = copy(self.__start_pos)
        self.__basik_size = copy(self.__start_size)
        
    def update(self):
        
        mouse_speed = Mouse.speed
        
        if self.__parent_object is None:
            self.__at_pos = copy(self.__basik_pos)
            self.__at_size = copy(self.__basik_size)
        
        if POSITIONS.USING_PARENT_COORD_SYSTEM in self.__flags:
            parent_pos = self.__parent_object.pos
            self.__at_pos[0]=parent_pos[0]+self.__basik_pos[0]
            self.__at_pos[1]=parent_pos[1]+self.__basik_pos[1]
            
        
        if POSITIONS.CENTER in self.__flags:
            win_center = self.__window.center
            pos = [win_center[0]-self.__at_size[0]/2, win_center[1]-self.__at_size[1]/2]
            self.__at_pos = pos
        if POSITIONS.CENTER_X in self.__flags:
            win_center = self.__window.center
            self.__at_pos[0] = win_center[0]-self.__at_size[0]/2
        if POSITIONS.CENTER_Y in self.__flags:
            win_center = self.__window.center
            self.__at_pos[1] = win_center[1]-self.__at_size[1]/2
        
        
            
            
        if POSITIONS.CENTER_PARENT in self.__flags:
            parent_center = self.__parent_object.center
            pos = [parent_center[0]-self.__at_size[0]/2, parent_center[1]-self.__at_size[1]/2]
            self.__at_pos = pos
        if POSITIONS.CENTER_PARENT_X in self.__flags:
            parent_center = self.__parent_object.center
            self.__at_pos[0] = parent_center[0]-self.__at_size[0]/2
        if POSITIONS.CENTER_PARENT_Y in self.__flags:
            parent_center = self.__parent_object.center
            self.__at_pos[1] = parent_center[1]-self.__at_size[1]/2
        
        
                
                
        if SPECIAL_FLAGS.MOUSE_MOVING in self.__flags:
            self.__at_pos = copy(self.__basik_pos)
            self.__at_size = copy(self.__basik_size)
            
            if in_rect(self.__at_pos, self.__at_size, Mouse.pos):
                if EVENTS.get('lclick'):
                    self.__clicked = True
            if not EVENTS.get('lpress'):
                self.__clicked = False
            
            if self.__clicked:
                self.__basik_pos[0]+=mouse_speed[0]
                self.__basik_pos[1]+=mouse_speed[1]
                
            
        
    def render(self, surf):
        if self.__rendered:
            color = self.__color
            if in_rect(self.__at_pos, self.__at_size, Mouse.pos):
                color = self.__hover_color
                if EVENTS.get('lpress'):
                    color = self.__press_color
            Draw.draw_rect(surf, self.pos, self.size, color, radius=self.radius)
            