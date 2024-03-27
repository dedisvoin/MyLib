import pygame
import random
from GLib.drawing import *
from GLib.mathematics import *
from GLib.sprites import *

from typing import Tuple


class P_SHAPES:
    CIRCLE = 'S_CIRCLE'
    RECT = 'S_RECT'
    SPRITE = 'S_SPRITE'
    
class P_EMMITERS:
    RECT = 'E_RECT'
    CIRCLE = 'E_CIRCLE'
    LINE = 'E_LINE'
    
class _particle:
    def __init__(self) -> None:
        
        # basic
        self.POS = [0,0]
        self.POS_GLOBAL = [0,0]
        self.SHAPE = P_SHAPES.CIRCLE
        self.COLOR = [100,100,100]
        self.COLOR_FROM_LIST = False
        self.COLOR_LIST = [[100,100,100]]
        self.TIMER = 0
        self.SHAPE_RENDERE = True
        self.SIZE_RESIZE_TIMER = 0

        # sprite
        self.SPRITE_ANGLE_ADD = 0
        self.SPRITE_ANGLE = 0
        self.SPRITE_ANGLE_BY_SPEED = True
        self.SPRITE_NAME = None
        self.SPRITE_FROM_LIST = False
        self.SPRITE_LIST = []
        self.SPRITE_START_SCALE = 1
        self.SPRITE_SCALE_RESIZE = -0.1
        self.SPRITE_RANDOM_SCALE = 0
        self.SPRITE_START_START_SCALE = 1

        # shadow
        self.SHADOWING = False
        self.SHADOW_DX = 0
        self.SHADOW_DY = 1
        self.SHADOW_COLOR = (0,0,0)
        
        # circle 
        self.RADIUS = 10
        self.START_RADIUS = 10
        self.RANDOM_RADIUS = 0
        self.RADIUS_RESIZE = -0.1
        
        # speed
        self.SPEED = Vector2([0, 0])
        self.RANDOM_SPEED = 0
        self.SPEED_ANGLE = 0
        self.SPEED_DURATION = 0
        self.SPEED_FRICTION = 1
        self.GRAVITY_VECTOR = Vector2([0, 0])
        self.SPEED_ROTATE_ANGLE = 0

        # tile
        self.TILE_USE = False
        self.TILE_POINTS = []
        self.TILE_POINT_SETUP_SPEED = 10
        self.TILE_POINT_RADIUS_RESIZE = -0.1

        # lightning
        self.LIGHT_USE = False
        self.LIGHT_COLOR = [255,255,255]
        self.LIGHT_COLOR_FROM_PARTICLE_COLOR = False
        self.LIGHT_RADIUS = 20
        self.LIGHT_STRANGE = 1
        self.LIGHT_STRANGE_BY_SIZE = False
        
    def set(self, arg_name: str, value_: any):
        arg_name = arg_name.upper()
        if arg_name in self.__dict__.keys():
            self.__dict__[arg_name] = value_
        else:
            print(f'Do not found {arg_name}!')
            
    def set_all(self, args):
        for name in args:
            self.set(name, args[name])
        
class Particle(_particle):
    def __init__(self) -> None:
        super().__init__()
        
class Emmiter:
    def __init__(self, type = P_EMMITERS.RECT, r_pos = [0,0], r_size = [1,1]) -> None:
        self.r_pos = r_pos
        self.r_size = r_size
        self.type = type
        
class ParticleSpace:
    def __init__(self) -> None:
        self._space:Tuple = []
        self.timer = 0
        self.sprites:dict[Sprite] = {}
        

    def load_sprites(self, file_paths: list[str]):
        for name in file_paths:
            sprite = Sprite(name[0], True, 90)
            self.sprites[name[1]] = sprite

        
    def get_particles(self):
        p = []
        
        for particle in self._space:
            pd = {}
            for name in particle:
                data = particle[name]
                if type(data) != Vector2:
                    pd[name] = data
            p.append(pd)
        return p
        
    def __construct_particle__(self, particle: Particle, emmiter: Emmiter):
        p_dict = {}
        
       
        

        for i in particle.__dict__:
            p_dict[i] = copy(particle.__dict__[i])
        
        
        if emmiter.type == P_EMMITERS.RECT:
            
            p_dict['POS'][0] = emmiter.r_pos[0]+random.randint(0, emmiter.r_size[0])
            p_dict['POS'][1] = emmiter.r_pos[1]+random.randint(0, emmiter.r_size[1])
            
        p_dict['RADIUS'] += random.randint(0, p_dict['RANDOM_RADIUS'])
        p_dict['START_RADIUS'] = copy(p_dict['RADIUS'])
        
        p_dict['SPEED']+=Vector2([0,random.randint(0, p_dict['RANDOM_SPEED']*1000)/1000])
        p_dict['SPEED'].set_angle(p_dict['SPEED_ANGLE']+random.randint(-p_dict['SPEED_DURATION'],p_dict['SPEED_DURATION']))

        if p_dict['COLOR_FROM_LIST']:
            p_dict['COLOR'] = random.choice(p_dict['COLOR_LIST'])

        p_dict['SPRITE_START_SCALE']+=random.randint(0, p_dict['SPRITE_RANDOM_SCALE']*1000)/1000
        p_dict['SPRITE_START_START_SCALE'] = copy(p_dict['SPRITE_START_SCALE'])
        
        return copy(p_dict)
    
    def timer_update(self):
        self.timer+=1
    
    def add(self, particle, emmiter, count, time):
        
        if self.timer%time==0:
            for i in range(count):
                p = self.__construct_particle__(particle, emmiter)

                self._space.append(p)
            
            
    def update(self):
        for i, particle in enumerate(self._space):
            self._space[i]['SPEED']+=self._space[i]['GRAVITY_VECTOR']
            if self._space[i]['SIZE_RESIZE_TIMER']>0:
                self._space[i]['SIZE_RESIZE_TIMER']-=1

            self._space[i]['SPEED'].rotate(self._space[i]['SPEED_ROTATE_ANGLE'])

            self._space[i]['POS'][0]+=self._space[i]['SPEED'].x
            self._space[i]['POS'][1]+=self._space[i]['SPEED'].y
            
            if self._space[i]['SIZE_RESIZE_TIMER']==0:
                self._space[i]['RADIUS']+=self._space[i]["RADIUS_RESIZE"]

            self._space[i]['SPEED']*=self._space[i]['SPEED_FRICTION']

            self._space[i]['TIMER']+=1

            if self._space[i]['TILE_USE']:
                if self._space[i]['TIMER']%self._space[i]['TILE_POINT_SETUP_SPEED']==0:
                    self._space[i]['TILE_POINTS'].append([copy(self._space[i]['POS']), self._space[i]['RADIUS']*2])

            for tile_point in self._space[i]['TILE_POINTS']:
                tile_point[1]+=self._space[i]['TILE_POINT_RADIUS_RESIZE']
                

                if tile_point[1]<=0:
                    self._space[i]['TILE_POINTS'].remove(tile_point)
                    break

            if self._space[i]['SPRITE_ANGLE_BY_SPEED']:
                self._space[i]['SPRITE_ANGLE'] = self._space[i]['SPEED'].get_angle()+self._space[i]['SPRITE_ANGLE_ADD']

            self._space[i]['SPRITE_START_SCALE']+=self._space[i]['SPRITE_SCALE_RESIZE']

            
        self._space = list(filter(lambda elem: elem['RADIUS']>0, self._space))
        self._space = list(filter(lambda elem: elem['SPRITE_START_SCALE']>0, self._space))
    
    def create_light_surf(self, particle):
        LIGHT_STRANGE = particle['LIGHT_STRANGE']
        if particle['LIGHT_STRANGE_BY_SIZE']:
            
            LIGHT_STRANGE = (particle['RADIUS']/particle['START_RADIUS'])*particle['LIGHT_STRANGE']
            if particle['SHAPE'] == P_SHAPES.SPRITE:
                LIGHT_STRANGE = (particle['SPRITE_START_SCALE']/particle['SPRITE_START_START_SCALE'])*particle['LIGHT_STRANGE']
                        
        LIGHT_STRANGE = max(0,LIGHT_STRANGE)
        light_color = particle['LIGHT_COLOR']
        if particle['LIGHT_COLOR_FROM_PARTICLE_COLOR']:
            light_color = particle['COLOR']

        light_color = [
            min(light_color[0]*LIGHT_STRANGE,255),
            min(light_color[1]*LIGHT_STRANGE,255),
            min(light_color[2]*LIGHT_STRANGE,255),
        ]
                        
        surf = pygame.Surface([(particle['RADIUS']+particle['LIGHT_RADIUS'])*2, (particle['RADIUS']+particle['LIGHT_RADIUS'])*2],flags=pygame.SRCCOLORKEY).convert_alpha()
                        
        
                            
        Draw.draw_circle(surf, [particle['RADIUS']+particle['LIGHT_RADIUS'],particle['RADIUS']+particle['LIGHT_RADIUS']],particle['RADIUS']+particle['LIGHT_RADIUS'], light_color)
        return surf

    
    def render(self, win, global_pos, particles):

        for i, particle in enumerate(particles):
            particle['POS_GLOBAL'][0] = round(particle['POS'][0]+global_pos[0])
            particle['POS_GLOBAL'][1] = round(particle['POS'][1]+global_pos[1])
            if particle['SHADOWING']:
                if particle['SHAPE'] == P_SHAPES.CIRCLE:
                    Draw.draw_circle(win.surf, [particle['POS_GLOBAL'][0]+particle['SHADOW_DX'],particle['POS_GLOBAL'][1]+particle['SHADOW_DY']], particle['RADIUS'], particle['SHADOW_COLOR'] )
        
        for i, particle in enumerate( particles ):
            
            
            
            #particle['TILE_POINTS'].append([particle['POS'], particle['RADIUS']])
            if particle['TILE_USE']:
                if particle['SHADOWING']:
                    for i in range(len(particle['TILE_POINTS'])):
                        if i+1<len(particle['TILE_POINTS']):
                            point_1 = particle['TILE_POINTS'][i]
                            point_2 = particle['TILE_POINTS'][i+1]
                            
                            Draw.draw_line(win.surf, [point_1[0][0]+global_pos[0]+particle['SHADOW_DX'],point_1[0][1]+global_pos[1]+particle['SHADOW_DY']], 
                                            [point_2[0][0]+global_pos[0]+particle['SHADOW_DX'],point_2[0][1]+global_pos[1]+particle['SHADOW_DY']], 
                                            particle['SHADOW_COLOR'], int(point_1[1]))

                for i in range(len(particle['TILE_POINTS'])):
                    if i+1<len(particle['TILE_POINTS']):
                        point_1 = particle['TILE_POINTS'][i]
                        point_2 = particle['TILE_POINTS'][i+1]
                        
                        Draw.draw_line(win.surf, [point_1[0][0]+global_pos[0],point_1[0][1]+global_pos[1]], 
                                        [point_2[0][0]+global_pos[0],point_2[0][1]+global_pos[1]], 
                                        particle['COLOR'], int(point_1[1]))
            
            
            if particle['SHAPE'] == P_SHAPES.CIRCLE:
                Draw.draw_circle(win.surf, particle['POS_GLOBAL'], particle['RADIUS'], particle['COLOR'] )
            elif particle['SHAPE'] == P_SHAPES.SPRITE:
                
                self.sprites[particle['SPRITE_NAME']].angle = particle['SPRITE_ANGLE']
                self.sprites[particle['SPRITE_NAME']].scale = particle['SPRITE_START_SCALE']
                self.sprites[particle['SPRITE_NAME']].render(win.surf, particle['POS_GLOBAL'])
            
            if particle['LIGHT_USE']:
                surf = self.create_light_surf(particle)
                win.surf.blit(surf, center_rect( particle['POS_GLOBAL'], surf.get_size(), True), special_flags=pygame.BLEND_RGB_ADD) 

class CircleEffectSpace:
    def __init__(self) -> None:
        self.circles = []

    def add(self, circle):
        self.circles.append(copy(circle))

    def update(self):
        for circle in self.circles:
            circle.radius+=circle.radius_summing
            circle.start_width-=circle.width_minus
            if circle.start_width<=0:

                self.circles.remove(circle)

    def draw(self, win, camera=None):

        for circle in self.circles:

            pos = copy(circle.pos)
            if camera is not None:
                pos[0]+=camera.pos[0]
                pos[1]+=camera.pos[1]
            if int(circle.start_width)!=0:
                Draw.draw_circle(win.surf, pos, circle.radius, circle.color, int(circle.start_width))
        
class CircleEffect:       
    def __init__(self,pos, color, start_width=10, width_minus = 1, radius_suming = 0.1) -> None:
        self.color = color
        self.start_width = start_width
        self.width_minus = width_minus
        self.radius_summing = radius_suming
        self.radius = 1
        self.pos = pos

