import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from GLib.server_tools import *
from GLib.special_methods import *
from GLib.color import *


ip = 'localhost'

# создается сервер на локальном хосте
server = Server(
    port=9999,
    host=ip,
    name='TestServer',
    max_clients=50
)

# размеры окна
window_size = [800, 800]

# класс мяча
class Ball:
    def __init__(self, id) -> None:
        self.color = Color.random().rgb
        self.radius = randint(50,200)
        self.pos = [
            randint(0+self.radius, window_size[0]-self.radius),
            randint(0+self.radius, window_size[1]-self.radius)
        ]
        self.id = id
        self.speed = [0,0]
    
    def data(self):
        return [self.pos, self.radius, self.color]
    
    def update(self):
        self.speed[0]*=0.9
        self.speed[1]*=0.9
        
        self.pos[0]+=self.speed[0]
        self.pos[1]+=self.speed[1]
        
        if self.pos[0]-self.radius<0: self.pos[0] = self.radius
        if self.pos[0]+self.radius>window_size[0]: self.pos[0] = window_size[0]-self.radius
        if self.pos[1]-self.radius<0: self.pos[1] = self.radius
        if self.pos[1]+self.radius>window_size[1]: self.pos[1] = window_size[1]-self.radius

balls = []


@sub_process() # декоратор для создания метода работающего в другом потоке
def client_wait():
    while server.wait_connects(sleep_time = 0.1): # ожидание подключения клиентов
        if server.client_connect_event(): # ивент сробатывающий при подключении клиента
            client_info = server.client_connect_info() # Получение информации об подключившемся клиенте
            balls.append(Ball(client_info[1][1])) # создание обьекта мяча
            
        
            
@sub_process()
def client_update(): # обновление состояния клиентов
    while True:
        server.clients_update(0.01) # метод обновления состояния
        
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
            for i, ball in enumerate(balls):
                if ball.id == client_info[1][1]:
                    del balls[i]


@sub_process()
def send_data(): # отправка состояния поля всем клиентам
    while True:
        
        data = [
            ball.data() for ball in balls
        ]
        
        server.add_send_packet(packing(data,'nums')) # пакетирование и индексация информации, и добавление его в буфер отправки
        server.send(0.01) # отправка буфера всем подключенным клиентам
        
@sub_process()
def recv_data():
    global balls
    while True:
        data = server.recv_all(buffer_size=1024, sleep_time=0.01, name='inputs')
        for d in data:
            for ball in balls:
                if ball.id == d[0][1]:
                    if d[1][0]:
                        ball.speed[1]-=5
                    if d[1][1]:
                        ball.speed[1]+=5
                    if d[1][2]:
                        ball.speed[0]-=5
                    if d[1][3]:
                        ball.speed[0]+=5


@sub_process()
def update(): # обновление состояний мячей
    while True:
        sleep(0.01)
        for ball in balls:
            ball.update()
        
'''
Запуск всех процессов
'''
client_wait()
client_update()
send_data()
recv_data()
update()