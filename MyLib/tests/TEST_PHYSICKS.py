from GLib.window import *
from GLib.drawing import *
from GLib.physick import *
from GLib.inputs import *


win = Window()

cs = Physics.CollidingSpace()
cs.adds([
    Physics.CollidingRect([800,100],[0,600],True),
    Physics.CollidingRect([50,50],[300,300],False, 'player')
])

while win():
    cs.update()
    cs.view(win.surf)
    