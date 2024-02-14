from GLib.window import *
from GLib.drawing import *
from GLib.inputs import *
from GLib.color import *
from GLib.vfx import *

win = Window(statick=0,size=[1920/4,1080/4], flags=WindowFlags.RESIZE|WindowFlags.SCALE)
win.fps = 90


events = Events()
events.add(
    Mouse(Mouse.bt_left, Mouse.press_event, 1)
)



pspace = ParticleSpace([0,0],[1000,1000], win, 1)
pspavn = ParticleSpawner(size_=[1,1])

p = Particle()
p.RADIUS = 5
p.COLOR = (150,200,255)
p.RADIUS_RESIZE = -0.05
p.RESIZE_START_TIME = 0
p.SPEED = Vector2(3,0)
p.SPEED_DURATION = 180
p.SPEED_RANDOMER = 2
p.SPEED_FRICTION = 0.999
p.TILE_USING = 10
p.TILE_POINT_SET_TIME = 1
p.TILE_POINTS_SIZE_RESIZE = -0.2
p.GRADIENT = Gradient.ManyColors([[255,100,100],[100,100,200]],[100,100],[[1,1,1],[1,1,1]])
p.GRADIENT_MAX_STEP = 200
p.LIGHTNING = 1
p.LIGHT_STRANGE = 2
p.LIGHT_SIZE = 10
p.BLEND_LIGHT_CIRCLES = 50
p.LIGHT_SHAPE = ParticleShapes.BLEND_CIRCLE
p.LIGHT_MODE = ParticleLightTypes.ADD
p.PULSING = 1
p.PULSE_AMPLITUDE = 8
p.PULSE_SPEED = 0.1
p.PULSE_RANDOM_AMPLITUDE = 1


mg = ParticleTurbulesity.MagnetCircle([0,0],400,0.99)


last_sprites = []

while win(fill_color=(0,0,0)):
    win.view_fps()
    win.view_delta()
    
    events.update()
    
    
    pspavn._pos = [0,0]
    pspavn._size = win.get_surf_size()
    
    pspace.add(p, pspavn, 1, 1)
    pspace.render([0,0])
    pspace.update(lambda x,y : ..., lambda x:...)
    pspace.tick()
    
    
    
    
    
    
    
    
    
    