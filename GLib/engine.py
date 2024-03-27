import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from GLib.server_tools import *
from GLib.inputs import *
from GLib.special_methods import *

class Field:
    def __init__(self, name) -> None:
        self.data = []
        self.name = name
        
class GameServer:
    def __init__(self, port, host, password=None, clients_count=2) -> None:
        
        self.server_object = Server(port, host, 'GameServer', clients_count, password)
        
        self.sended_fields = {}
        self.recv_fields = {}
        
        self.sleep_wait = 0.1
        self.sleep_update = 0.01
        self.sleep_send = 0.01
        self.sleep_recv = 0.0001
        self.connect_event = None
        
        self.disconnect_event = None

        
    def get(self):
        return self.recv_fields
        
    def add_send_field(self, filed: Field):
        self.sended_fields[filed.name] = filed
        
    def add_recv_field(self, field: Field):
        self.recv_fields[field.name] = field.data
        
    def start(self):
        self.client_wait()
        self.client_update()
        self.send()
        self.recv()
        
    @sub_process()
    def client_wait(self):
        '''client_connect_event(client_connect_info) '''
        while self.server_object.wait_connects(sleep_time = self.sleep_wait): 
            if self.server_object.client_connect_event():
                if self.connect_event is not None:
                    client_connect_info = self.server_object.client_connect_info()
                    self.connect_event[0](client_connect_info, *self.connect_event[1])
                    
    @sub_process()
    def client_update(self):
        while True:
            self.server_object.clients_update(self.sleep_update) # метод обновления состояния
            self.server_object.exiting()
            # ивент отключения клиента
            '''
            проверяется отправкой тестового пакета и если клиент не отвечает 
            на него несколько тиков подпряд значит он отключился
            '''
            
            if self.server_object.client_deconnect_event(): 
                if self.disconnect_event is not None:
                    client_disconnect_info = self.server_object.client_deconnect_info() # Получение информации об отключившемся клиенте
                    self.disconnect_event[0](client_disconnect_info, *self.disconnect_event[1])

    @sub_process()
    def send(self):
        
        while True:
            
            for field in self.sended_fields:
                pack = packing(self.sended_fields[field].data,field)
                
                self.server_object.add_send_packet(pack) # пакетирование и индексация информации, и добавление его в буфер отправки
            self.server_object.send(self.sleep_send) # отправка буфера всем подключенным клиентам
                
    @sub_process()
    def recv(self):
        while True:
            if len(self.recv_fields)>0:
                for field in self.recv_fields:
                    data = self.server_object.recv_all(buffer_size=1024, sleep_time=self.sleep_recv, name=field)
                    
                    self.recv_fields[field] = data
            else:
                sleep(self.sleep_recv)
        
class GameClient:
    def __init__(self, port, host, password=None, id=None) -> None:
        self.host = host
        self.port = port
        self.password = password
        self._id = id
        self.client_object = Client(port, host, id, password )
        
        self.recice_fields = {}
        self.send_fileds = {}
        
        self.sleep_recv = 0.0001
        self.sleep_send = 0.01
        self.recv_buf_size = 2048

    def reconect(self):
        self.client_object.reconect()
    
    @property
    def id(self):
        __id = self.client_object.id
        if type(__id) == int:
            return __id
        else:
            return __id[1]
    
    def start(self):
        new_thread_start(self.recv_data)
        new_thread_start(self.send_data)
        
    def add_recv_filed(self, field: Field):
        self.recice_fields[field.name] = field.data
        
    def add_send_field(self, filed: Field):
        self.send_fileds[filed.name] = filed
        
    def get(self):
        return self.recice_fields
        
    
    def recv_data(self):
        while True:
                
                self.client_object.start_ping()
                
                data = self.client_object.recv(sleep_time=self.sleep_recv, buffer_size=self.recv_buf_size) # прослушивание порта
                
                for field in self.recice_fields:
                    if d:= pack_name(data, field): # поиск нужного пакета
                        
                        self.recice_fields[field] = d
                self.client_object.end_ping()
            
        
    
    
    def send_data(self):
        while True:
            
            if len(self.send_fileds)>0:
                for field in self.send_fileds:
                    self.client_object.add_sended_data(packing(self.send_fileds[field].data, field))
                
                
                self.client_object.send(self.sleep_send)
            else:
                sleep(self.sleep_send)

