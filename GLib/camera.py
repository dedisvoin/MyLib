import pygame
from GLib.window import Window
from GLib.special_methods import *
from GLib.mathematics import *

class Camera2D:
    def __init__(self, win: Window) -> None:
        self.win = win
        self.scale = 1
        self.angle = 0
        self.pos = [0,0]
        self.move_delta = 0.01
        self.scale_delta = 0.01
        self.target_scale = 1

        self.target_pos = None
        self.shake = 0
        self.shake_delta = 0.8

    def set_target_pos(self, pos):
        self.target_pos = pos

    def set_target_scale(self, scale):
        self.target_scale = scale

    def update(self):
        win_center = self.win.center
        dx = (self.target_pos[0]-win_center[0]+self.pos[0])*self.move_delta
        dy = (self.target_pos[1]-win_center[1]+self.pos[1])*self.move_delta
        self.pos[0]-=dx
        self.pos[1]-=dy

        self.shake*=self.shake_delta
        vector = Vector2([10,10])
        vector.normalyze()
        
        vector.set_angle(random.randint(0,360))
        vector*=self.shake

        self.pos[0]+=vector.x
        self.pos[1]+=vector.y


        self.scale-=(self.scale-self.target_scale)*self.scale_delta

    def render(self):
        self.scale = max(self.scale, 0.001)
        surf = self.win.surf.copy()
        
        surf = pygame.transform.scale(surf, [
            self.win.surf.get_size()[0]*self.scale, 
            self.win.surf.get_size()[1]*self.scale
        ])
        surf = pygame.transform.rotate(surf, self.angle).convert()
        
                
        win_size = self.win.get_size()
        pygame.draw.rect(self.win.surf, self.win.bg_color, [0,0, *win_size], 0)
        self.win.surf.blit(surf,[0,0],[(surf.get_width()-self.win.surf.get_width())/2,
                                            (surf.get_height()-self.win.surf.get_height())/2,
                                            self.win.surf.get_width(), 
                                            self.win.surf.get_height()])
          