import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from GLib.window import *
from GLib.drawing import *
from GLib.sprites import *

import interface





# app 
class MC:
    def __init__(self) -> None:
        self.window = Window(
            pos = None,
            size = [1000, 800],
            title = 'MC',
            flags = WindowFlags.RESIZE
        )
        self.left_interface = interface.LeftInterface(self.window)
        self.map_create_interface = interface.MapCreateInterface(self.window)
        
    def run(self):
        while self.window(interface.BG_COLOR):
            self.left_interface.render()
            self.map_create_interface.render()
            
            

app = MC()

app.run()