from GLib.interface import *
from GLib.window import *


win = Window(flags=WindowFlags.RESIZE)

text_1 = String([10,10],
        'black', 
        [], 
        win, 'Button', 'arial', 20, True)

button = TextButton([0,0],[200,30], text_obj=text_1, flags=[POSITIONS.CENTER_X],contained=1,window=win)

box_1 = Box(
    pos=[20,20],
    size=[400,320],
    radius=7,
    flags=[POSITIONS.CENTER_Y],
    window=win,
    color='darkgray',
    contained=1,
    rendered=False
)


box_3 = Box(
    pos=[20,20],
    size=[400,320],
    radius=7,
    flags=[POSITIONS.CENTER_Y, CONTAINED.USING_CONTAINER,],
    window=win,
    color='darkgray',
    contained=1,
    objects=[button],
    contained_type=CONTAINED_TYPES.VERTICAL
)



box = Box(
    pos=[20,20],
    size=[500,350],
    radius=12,
    flags=[CONTAINED.USING_CONTAINER, POSITIONS.CENTER],
    window=win,
    objects=[box_1,box_3],
    contained_padding=10,
    container_dy = 10,
    contained_type=CONTAINED_TYPES.HORIZONTAL
)




while win():
    EVENTS.update()
    
    box.update()
    box.render(win.surf)
    
    box_1.update()
    box_1.render(win.surf)
    box_3.update()
    box_3.render(win.surf)
    
    button.update()
    button.render(win.surf)
    
    text_1.update()
    text_1.render(win.surf)
    
    