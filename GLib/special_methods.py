import random
import subprocess
from threading import Thread
import json

def generate_id(obj: any, id = None):
    name = type(obj).__name__
    if id is None:
        id = f'{name}:({random.randint(0,9999999999999999)})'
    else:
        id = f'{name}:({id})'
    return id

def get_type_from_id(id: str):
    args = id.split(':')
    return args[0]

def compare_id_and_number(id: str, compare_id: str | int):
    args = id.split(':')
    numbers = args[1][1:-1]
    return numbers == str(compare_id)

def sub_process():
    def NewProcessInner(func):
        def wrapper(*args, **kvargs):
            Thread(target=func, args=args, kwargs=kvargs).start()
        return wrapper
    return NewProcessInner

def new_thread_start(target):
    Thread(target=target, daemon=True).start()
    
def new_process_start(file_name: str):
    subprocess.Popen(f'python {file_name}', shell=True)

class JSON:
    @staticmethod
    def save(file_name: str, data: any):
        file = open(file_name, 'w')
        json.dump(data, file, allow_nan=False, indent=3)

    @staticmethod
    def load(file_name: str):
        file = open(file_name, 'r')
        data = json.load(file)
        return data