import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from GLib.server_tools import *
from GLib.special_methods import *
from GLib.window import *
from GLib.drawing import *
from GLib.text import *
from GLib.inputs import *

host, port = input('input you host(ip) and port -> ').split(':')
name = input('input you name -> ')

client = Client(host=host, port=int(port), id=name)

rects = []
inputs = []

gp = [0,0]
my_id = client.client.getsockname()[1]

def recv_data(): # Получение данных
    global rects
    while True:
        client.start_ping()
        
        
        data = client.recv(sleep_time=0.0001) # прослушивание порта
        
        if d:= pack_name(data, 'rects'): # поиск нужного пакета
            rects = d
        client.end_ping()
        
            
            


            
new_thread_start(recv_data)

text = Text('arial',20, True)


def send_data():
    while True:
        client.send(packing(inputs, 'inputs'), 0.01)
        
        
new_thread_start(send_data)

events = Events()
events.add([
    Keyboard('up', Keyboard.press_event, '0'),
    Keyboard('left', Keyboard.press_event, '2'),
    Keyboard('right', Keyboard.press_event, '3'),
])

win = Window(size=[700,700], flags=WindowFlags.RESIZE)
win.fps = 5000
while win():
    events.update()
    
    inputs = [
        events.get('0'),
        events.get('2'),
        events.get('3'),
        client.id
    ]
    for rect in rects:
        pos = [
            rect[0][0]+gp[0],
            rect[0][1]+gp[1],
        ]
        
        if str(rect[2]) == str(client.id):
            
            gp[0]+=(win.center[0]-pos[0])*0.05*win.delta
            gp[1]+=(win.center[1]-pos[1])*0.05*win.delta
            
        Draw.draw_rect(win.surf, pos, rect[1], 'black')
        if str(rect[2]) != 'pol':
            surf = text.render_text_surf(f'id: {str(rect[2])}', 'black')
            win.surf.blit(surf, [pos[0]-surf.get_width()/2+25, pos[1]-60])
    
    surf = text.render_text_surf(f'ping: {str(round(client.ping,3)*1000)}ms', 'red')
    win.surf.blit(surf, [0,win.get_size()[1]-20])
    win.view_fps()