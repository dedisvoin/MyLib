import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from GLib.server_tools import *
from GLib.special_methods import *
from GLib.window import *
from GLib.drawing import *
from GLib.text import *
from GLib.inputs import *


# создается обьект клиента который подключается к локалбному хосту
client = Client(host='0.tcp.eu.ngrok.io', port=13808)

balls = []
server_info = []
inputs = []



def recv_data(): # Получение данных
    global balls, server_info
    while True:
        data = client.recv(sleep_time=0.001) # прослушивание порта

        if d:= pack_name(data, 'nums'): # поиск нужного пакета
            balls = d
        if d:= pack_name(data, 'sinfo'): # поиск нужного пакета
            server_info = d
            
new_thread_start(recv_data) # запуск процесса прослушки            

def send_data():
    while True:
        client.send(packing(inputs, 'inputs'), 0.05)

new_thread_start(send_data)

events = Events()
events.add([
    Keyboard('up', Keyboard.press_event, '0'),
    Keyboard('down', Keyboard.press_event, '1'),
    Keyboard('left', Keyboard.press_event, '2'),
    Keyboard('right', Keyboard.press_event, '3'),
])



win = Window(size=[800,800])  # создание окна
text = Text('arial',10, True)

while win():
    events.update()
    
    inputs = [
        events.get('0'),
        events.get('1'),
        events.get('2'),
        events.get('3'),
    ]
    
    
    # отрисовка полученных мячей
    for ball in balls:
        Draw.draw_circle(win.surf, ball[0], ball[1], ball[2])
        
    win.surf.blit(text.render_text_surf(str(server_info), 'black'), [5,5])
        
    
        
    win.view_fps()
            




