from GLib.window import *

from GLib.color import *

from GLib.drawing import *
win = Window()

g = Gradient.ManyColors(
    [
        [200,0,0],[0,200,0],[0,0,200]
    ],
    [200,200,200],
    [[1,1,1],[1,1,1],[1,1,1]]
)


p = 0
while win():
    p+=0.01
    if p>1:
        p = 0
    Draw.draw_circle(win.surf, [300,300], 100, g.get_percent(p))