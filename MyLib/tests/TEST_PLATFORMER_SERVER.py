import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))



from GLib.drawing import *
from GLib.physick import *
from GLib.inputs import *
from GLib.server_tools import *
from GLib.special_methods import *







cs = Physics.CollidingSpace()

cs.adds([
    Physics.CollidingRect([800,100],[0,600],True, 'pol', Vector2(0,0), Vector2(1,1)),
    Physics.CollidingRect([200,400],[600,400],True, 'pol', Vector2(0,0), Vector2(1,1)),
    Physics.CollidingRect([300,100],[100,100],True, 'pol', Vector2(0,0), Vector2(1,1)),
    Physics.CollidingRect([100,100],[400,200],True, 'pol', Vector2(0,0), Vector2(1,1)),
    Physics.CollidingRect([1000,50],[400,800],True, 'pol', Vector2(0,0), Vector2(1,1)),
    Physics.CollidingRect([100,100],[800,600],True, 'pol', Vector2(0,0), Vector2(1,1)),
    Physics.CollidingRect([100,100],[1000,400],True, 'pol', Vector2(0,0), Vector2(1,1)),
    Physics.CollidingRect([100,100],[1200,200],True, 'pol', Vector2(0,0), Vector2(1,1)),
])


ip = '127.0.0.1'

server = Server(
    port=9999,
    host=ip,
    name='TestServer',
    max_clients=5
)

@sub_process() # декоратор для создания метода работающего в другом потокеeee
def client_wait():
    while server.wait_connects(sleep_time = 0.1): # ожидание подключения клиентов
        
        if server.client_connect_event(): # ивент сробатывающий при подключении клиента
            client_info = server.client_connect_info() # Получение информации об подключившемся клиенте
            cs.add(Physics.CollidingRect([50,50],[400,0],False, client_info[2], Vector2(0,0), Vector2(1,1), air_resistance=Vector2(0.8,0.99)))
            
@sub_process()
def client_update(): # обновление состояния клиентов
    while True:
        server.clients_update(0.01) # метод обновления состояния
        server.exiting()
        # ивент отключения клиента
        '''
        проверяется отправкой тестового пакета и если клиент не отвечает 
        на него несколько тиков подпряд значит он отключился
        '''
        if server.client_deconnect_event(): 
            
            client_info = server.client_deconnect_info() # Получение информации об отключившемся клиенте
            '''
            Поиск обьекта принадлежавшего данному клиенту и его удаление
            '''
            for i, ball in enumerate(cs.colliders):
                
                if ball._id == client_info[1][1]:
                    del cs.colliders[i]
                    
@sub_process()
def update(): # обновление состояний мячей
    while True:
        sleep(0.01)
        cs.update()
        for rect in cs.colliders:
            if rect.y >2000:rect.y = 0
        
        for d in data:
            
            for ball in cs.colliders:
                if str(ball._id) == str(d[1][3]):
                    if d[1][0] and ball.trigers['down']:
                        ball._speed.y-=18
                    if d[1][1]:
                        ball._speed.x-=4
                    if d[1][2]:
                        ball._speed.x+=4
        
        
        
@sub_process()
def send_data(): # отправка состояния поля всем клиентам
    while True:
        
        data = []
        for rect in cs.colliders:
            data.append([rect.xy, rect.wh, rect._id])
        
        server.add_send_packet(packing(data,'rects')) # пакетирование и индексация информации, и добавление его в буфер отправки
        server.send(0.01) # отправка буфера всем подключенным клиентам

data = []
@sub_process()
def recv_data():
    global cs, data
    while True:
        data = server.recv_all(buffer_size=1024, sleep_time=0.01, name='inputs')
        
        
        
client_wait()
client_update()
update()
send_data()
recv_data()