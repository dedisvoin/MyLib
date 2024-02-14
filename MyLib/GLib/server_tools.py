from copy import copy
from typing import Iterable, Tuple
from ast import literal_eval
from time import sleep, time
import socket
import os, sys
from colorama import Fore, Style
import keyboard
import random

class LOGS:
    @classmethod    
    def LOG_SERVER_CONNECT(self, host, port, clients, max_clients):
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'server'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+'Connected '+Style.BRIGHT+Fore.CYAN+f'{host=} {port=}'+Fore.RESET+Style.RESET_ALL)
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'server -> client'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+f'Online count {clients}/{max_clients}')

    @classmethod
    def LOG_SERVER_CREATED(self, s_host, s_port):
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'server'+Style.RESET_ALL+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.GREEN+'SUCCES'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+'Server started ('+Style.BRIGHT+Fore.CYAN+f'{s_host=} {s_port=}'+Fore.RESET+Style.RESET_ALL+")")
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'server'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+'Wait connects...')

    @classmethod
    def LOG_SERVER_NOT_CREATED(self, s_host, s_port):
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'server'+Style.RESET_ALL+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.RED+'ERROR'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+'Server not started ('+Style.BRIGHT+Fore.CYAN+f'{s_host=} {s_port=}'+Fore.RESET+Style.RESET_ALL+')')
        

    @classmethod
    def LOG_CLIENT_CLOSED(self, host, port, clients, max_clients):
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'server -> client'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+'Client '+Style.BRIGHT+Fore.CYAN+f'{host=} {port=}'+Fore.RESET+Style.RESET_ALL+' closed.')
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'server'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+f'Online count {clients}/{max_clients}')
    
    @classmethod
    def LOG_CLIENT_CREATED(self, id):
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'client'+Style.RESET_ALL+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.GREEN+'SUCCES'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+'Client created ('+Style.BRIGHT+Fore.CYAN+f'{id=}'+Fore.RESET+Style.RESET_ALL+')')
    
    @classmethod
    def LOG_CLIENT_CONNECT(self, host, port):
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'client'+Style.RESET_ALL+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.GREEN+'SUCCES'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+'Connected to server ('+Style.BRIGHT+Fore.CYAN+f'{host=} {port=}'+Fore.RESET+Style.RESET_ALL+')')

    @classmethod
    def LOG_CLIENT_NOT_CONNECT(self, host, port):
        print(Fore.YELLOW+'['+Fore.WHITE+'socket'+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.MAGENTA+'client'+Style.RESET_ALL+Fore.YELLOW+']'+'['+Style.BRIGHT+Fore.RED+'ERROR'+Style.RESET_ALL+Fore.YELLOW+']: '+Fore.RESET+'Server ('+Style.BRIGHT+Fore.CYAN+f'{host=} {port=}'+Fore.RESET+Style.RESET_ALL+') not online.')

# local port and host constants
LOCALHOST = 'localhost'
LOCALPORT = 8000

# converting methods
def convert_string_to_list(string: str) -> list:
    return literal_eval(string)

def convert_list_to_string(list: list) -> str:
    return str(list)

def convert_pack_to_bytes(pack: str) -> bytes:
    return pack.encode()

# get my host method
def get_my_host() -> str:
    return socket.gethostbyname(socket.gethostname())

# packing methods
def packing(data: list, name: str) -> str:
    pack = [name, data]
    return convert_list_to_string(pack)

def unpacking(data: bytes) -> list | None:
    try:
        return convert_string_to_list(data.decode())
    except:
        return None
    
def one_pack_name(pack: bytes, name: str) -> list:
    udata = unpacking(pack)
    if udata[0] == name:
        return udata[1]
    return None

def pack_name(pack: bytes, name: str) -> list:
    udata = unpacking(pack)
    if udata is not None:
        for element in udata:

            try:
                elem = convert_string_to_list(element)
                
                if elem is not None:
                    if elem[0] == name:
                        return elem[1]
            except:
                ...
    return None

def get_online(port, host) -> bool:
    try:
        Client(port, host)
        return True
    except:
        return False

# server class
class Server:
    def __init__(self, 
                port: int = LOCALPORT,
                host: str = LOCALHOST,
                name: str = 'Server',
                max_clients: int = 1) -> None:
        
        self.__port = port
        self.__host = host
        self.__name = name
        self.__max_client = max_clients
        self.__server_started = False
        
        
        self.__clients = []
        self.__client_connect_flag = False
        self.__client_connect_data = None
        
        self.__client_deconnect_flag = False
        self.__client_deconnect_data = None
        
        self.__sended_data = []
        
        self.__send_speed = 0
        
        
        self.server_init()
        
    def clients_count(self) -> int:
        return len(self.__clients)
    
    def update_sended_data(self):
        self.__sended_data = []
    
    @property
    def max_clients_count(self):
        return self.__max_client
    
    def server_init(self):
        try:
            self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.__server.bind((self.__host, self.__port))
            self.__server.setblocking(0)
            self.__server.listen(5)
            
            self.__server_started = True
            LOGS.LOG_SERVER_CREATED(self.__host, self.__port)
            
            
        except:
            LOGS.LOG_SERVER_NOT_CREATED(self.__host, self.__port)
            sys.exit()
            
    def exiting(self):
        if keyboard.is_pressed('e'):
            
            os._exit(-1)
            
            
            
            
    def wait_connects(self, sleep_time: float):
        sleep(sleep_time)
        
        if self.clients_count()<self.__max_client:
            try:
                client, addr = self.__server.accept()
                
                
                
                client.setblocking(0)
                idstring = client.recv(1024).decode()
                id = idstring[idstring.index('-')+1: idstring.index('+')]
                
                
                self.__clients.append([client, addr, id])
                
                
                    
                
                    
                    
                self.__client_connect_flag = True
                self.__client_connect_data = [client, addr, id]
                
                
                
                LOGS.LOG_SERVER_CONNECT(addr[0], addr[1], self.clients_count(), self.__max_client )
            except:
                self.__client_connect_flag = False
                self.__client_connect_data = None
        
        else:
            self.__client_connect_flag = False
            self.__client_connect_data = None
        
        return self.__server_started
    
    def client_connect_event(self) -> bool:
        return self.__client_connect_flag

    def client_connect_info(self) -> list:
        return self.__client_connect_data
    
    def client_deconnect_event(self) -> bool:
        return self.__client_deconnect_flag

    def client_deconnect_info(self) -> list:
        return self.__client_deconnect_data
    
    def clients_update(self, sleep_time: float = 0.01):
        self.__send_pack_to_name(['you online?'], 'connected', sleep_time)
        
    def add_send_packet(self, packet: any):
        self.__sended_data.append(packet)
    
    def send(self, sleep_time: float):
        
        self.__server_info_pack()
        data = self.__sended_data
        send_start_time = time()
        try:
            sleep(sleep_time)
            
            str_data = convert_list_to_string(data)
            for index in range(len(self.__clients)):
                try:
                    self.__clients[index][0].send(str_data.encode())
                    #self.__client_deconnect_flag = False
                    #self.__client_deconnect_data = None
                except:
                    #print(f'Client {self.__clients[index][1]} closed!')
                    #self.__client_deconnect_flag = True
                    
                    #self.__clients[index][0].close()
                    #self.__client_deconnect_data = copy(self.__clients[index])
                    #del self.__clients[index]
                    #print(f'{self.clients_count()} / {self.__max_client} connected.')
                    #break
                    ...
        except:...
        self.__send_speed = round(time() - send_start_time,4)
        self.update_sended_data()
        
    def __server_info_pack(self):
        self.__sended_data.append(packing([self.clients_count(),self.__send_speed], 'sinfo'))
    
    def __send_pack_to_name(self, data, name, sleep_time: float):
        try:
            sleep(sleep_time)
            
            convert_packet = convert_pack_to_bytes( packing(data, name) )
            for index in range(len(self.__clients)):
                try:
                    self.__clients[index][0].send(convert_packet)
                    self.__client_deconnect_flag = False
                    self.__client_deconnect_data = None
                except:
                    LOGS.LOG_CLIENT_CLOSED(self.__clients[index][1][0] ,self.__clients[index][1][1], self.clients_count()-1, self.__max_client)
                    self.__client_deconnect_flag = True
                    
                    self.__clients[index][0].close()
                    self.__client_deconnect_data = copy(self.__clients[index])
                    del self.__clients[index]
                    
                    break
        except:...
        
    def recv_all(self, buffer_size: int = 2048, sleep_time: float = 0, name: str = 'None'):
        sleep(sleep_time)
        all_clients_packets = []
        
        for index in range(len(self.__clients)):
            try:
                packet = self.__clients[index][0].recv(buffer_size)
                if p := one_pack_name(packet, name):
                    pack = [self.__clients[index][1], p]
                    all_clients_packets.append(pack)
            except:
                ...
        return all_clients_packets
                    
                

# client class
class Client:
    def __init__(self,
                port: int = LOCALPORT,
                host: str = LOCALHOST, 
                id: None = None) -> None:
        self.__port = port
        self.__host = host
        self.__client:socket.socket = None
        self.__ping = 0
        self.__recv_start_time = 0
        self.__id = random.randint(0,9999999999999)
        if id is not None:
            self.__id = id
        LOGS.LOG_CLIENT_CREATED(self.__id)
        self.client_init()
        
    @property
    def client(self):
        return self.__client
    
    @property
    def id(self):
        return self.__id
    
    @property
    def ping(self):
        return self.__ping
    
    def start_ping(self):
        self.__recv_start_time = time()
        
    def end_ping(self):
        self.__ping = time()-self.__recv_start_time
    
    def client_init(self):
        try:
            self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.__client.connect((self.__host, self.__port))
            
            self.__client.send(f'-{str(self.id)}+'.encode())
            
            LOGS.LOG_CLIENT_CONNECT(self.__host, self.__port)
        except:
            LOGS.LOG_CLIENT_NOT_CONNECT(self.__host, self.__port)
            sys.exit()
            
        
    def recv(self, buffer_size: int = 2048, sleep_time: float = 0):
        sleep(sleep_time)
        try:
            data = self.__client.recv(buffer_size)
            return data
        except:
            return []
    
    def send(self, packet: bytes , sleep_time: float = 0):
        sleep(sleep_time)
        self.__client.send(convert_pack_to_bytes(packet))
        