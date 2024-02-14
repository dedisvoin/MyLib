import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from GLib.window import *
from GLib.drawing import *
from GLib.sprites import *
from GLib.color import *
from GLib.mathematics import *
from GLib.inputs import *


events = Events()
events.add(Mouse(Mouse.bt_left, Mouse.click_event, 'lclick'))
events.add(Mouse(Mouse.bt_left, Mouse.press_event, 'lpress'))

LEFT_INTERFACE_WIDTH = 300
BG_COLOR = Color.hsv('#080C25')
LEFT_INTERFACE_COLOR = Color.hsv('#161E35')
BTN_TEXT_COLOR = Color.hsv('#FFFFFF')
WINDOWS_BG_COLOR = Color.hsv('#161E35')
WINDOWS_NAME_TEXT_COLOR = Color.hsv('#161E35')
WINDOWS_BORDER_COLOR = Color.hsv('#293659')

SLIDER_BG_COLOR = Color.hsv('#A6B2EC')

tc = '#018866'

BTN_COLOR_P = Color.hsv('#15497E')
BTN_COLOR = Color.hsv('#3071E7')
BTN_COLOR_R = Color.hsv('#A6B2EC')

class Connects:
    left_up_down = 'lud'
    right_up_down = 'rud'

class TextButton:
    def __init__(self, pos, size, text, font_size, color, p_color, r_color, connect, window: Window, r) -> None:
        self.text = Text('arial', font_size, True)
        self.text_surf = self.text.render_text_surf(text, BTN_TEXT_COLOR)
        
        self.window = window
        self.color = color
        self.r_color = r_color
        self.p_color = p_color
        self.connect = connect
        self.radius = r
        
        self.pos = pos
        self.size = size
        
    def render(self):
        color = self.color
        if in_rect(self.pos, self.size, Mouse.pos):
            color = self.r_color
            if events.get('lpress'):
                color = self.p_color
                
        r = [0, 0, 0, 0]
        if self.connect == Connects.left_up_down:
            r = [0, self.radius, self.radius, 0]
        if self.connect == Connects.right_up_down:
            r = [self.radius, 0, 0, self.radius]
        Draw.draw_rect(self.window.surf, self.pos, self.size, color, radius=r)
        self.window.surf.blit(self.text_surf, [self.pos[0]+self.size[0]/2-self.text_surf.get_width()/2, 
                                                self.pos[1]+self.size[1]/2-self.text_surf.get_height()/2])

class Slider:
    def __init__(self, window: Window, pos, size, max, min, start=0) -> None:
        self.pos = pos
        self.size = size
        self.min = min
        self.max = max
        self.start = start
        
        self.window = window
        self.at_pos = copy(pos)
        self.cp = [0,0]
    
    def render(self):
        Draw.draw_rect(self.window.surf, self.at_pos, self.size, SLIDER_BG_COLOR)

class MapCreateInterface:
    def __init__(self, window: Window) -> None:
        self.start_size = [400,200]
        self.size = copy(self.start_size)
        self.window = window
        self.name_text_surf = Text('arial', 18, 1).render_text_surf('space settings', BTN_TEXT_COLOR)
        self.pos = [0, 0]
        
        self.opened = False
        
        self.tiles_w_count_slider = Slider(self.window, [10,30],[150,10], 200, 1, 1)
    
    def render_ui(self):
        self.tiles_w_count_slider.at_pos = [self.pos[0]+self.tiles_w_count_slider.pos[0],self.pos[1]+self.tiles_w_count_slider.pos[1]]
        self.tiles_w_count_slider.render()
    
    def render(self):
        if self.opened:
            self.size = self.start_size
        else:
            self.size = [self.name_text_surf.get_width()+10, 22]
            
        
        self.pos = [self.window.get_size()[0]-self.size[0]-10, self.window.get_size()[1]-self.size[1]-10]
        Draw.draw_rect(self.window.surf, self.pos, self.size, WINDOWS_BG_COLOR, radius=10)
        Draw.draw_rect(self.window.surf, self.pos, [self.size[0],22], WINDOWS_BORDER_COLOR, radius=[10,10,0,0])
        self.window.surf.blit(self.name_text_surf, [self.pos[0]+5,self.pos[1]])
        
        if in_rect(self.pos, [self.size[0],22], Mouse.pos):
            Draw.draw_rect(self.window.surf, self.pos, [self.size[0],22], BTN_TEXT_COLOR, width=1, radius=[10,10,0,0])
            if events.get('lclick'):
                self.opened = not self.opened
                
        self.render_ui()
            
        
class LeftInterface:
    def __init__(self, window: Window) -> None:
        self.window = window
        self.btn_create = TextButton(
            [10,10],[(LEFT_INTERFACE_WIDTH-20)/2, 20],'create', 18,
            BTN_COLOR, BTN_COLOR_P, BTN_COLOR_R, Connects.right_up_down, self.window, 4
        )
        self.btn_load = TextButton(
            [10+(LEFT_INTERFACE_WIDTH-20)/2,10],[(LEFT_INTERFACE_WIDTH-20)/2, 20],'load', 18, 
            BTN_COLOR, BTN_COLOR_P, BTN_COLOR_R, Connects.left_up_down, self.window, 4
        )
        
    @property
    def win_size_w(self):
        return self.window.get_size()[0]
    
    @property
    def win_size_h(self):
        return self.window.get_size()[1]
        
    def render(self):
        Draw.draw_rect(self.window.surf, [0,0], [LEFT_INTERFACE_WIDTH, self.win_size_h], LEFT_INTERFACE_COLOR)
        
        self.btn_create.render()
        self.btn_load.render()
        events.update()