import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from GLib.window import *
from GLib.drawing import *
from GLib.sprites import *
from GLib.inputs import *

win = Window()

class Tile:
    def __init__(self, color, edges: list, name) -> None:
        self.color = color
        self.edges = edges
        self.pos = [0,0]
        self.size = [0,0]
        self.name = name

        
    def render(self):
        Draw.draw_rect(win.surf, self.pos, self.size, self.color )


class CollapseMap:
    def __init__(self, size: list[int, int] = [50,50], tile_size = 20, tiles=[]) -> None:
        self.size = size
        self.map = self.generate()
        self.tile_size = tile_size
        self.tiles = tiles
        
    def generate(self):
        dummy = []
        for i in range(self.size[1]):
            m = []
            for j in range(self.size[0]):
                m.append(None)
            dummy.append(m)
        return dummy
    
    def generate_start_values(self, count=3):
        for i in range(count):
            self.map[random.randint(0, len(self.map)-1)][random.randint(0, len(self.map[0])-1)] = random.choice(self.tiles)
    
    def render(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                pos = [j*self.tile_size, i*self.tile_size]
                if self.map[i][j] is not None:
                    
                    self.map[i][j].pos = pos
                    self.map[i][j].size = [self.tile_size, self.tile_size]
                    self.map[i][j].render()
                    
                Draw.draw_rect(win.surf, pos, [self.tile_size, self.tile_size], 'black', 1 )
                
    def collapse(self):
        ...
                
tiles = [
    Tile('yellow', [['water','send'],['water','send'], ['water','send'], ['water','send']], 'send'),
    Tile('blue', [['water','send'],['water','send'], ['water','send'], ['water','send']], 'water'),
    Tile('brown', [['dirt','send'],['dirt','send'], ['dirt','send'], ['dirt','send']], 'dirt')
]

cm = CollapseMap([20,20],20, tiles)


cm.generate_start_values(3)


while win():
    cm.render()