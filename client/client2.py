import socket
import random
import json
from defs import *

id = 'hoenza'
password = '8585'

def read_configs():
    configs = open(CONFIG_PATH).read()
    configs_dict = json.loads(configs)
    return configs_dict
    

class Client:
    def configure(self):
        self.id = id
        self.password = password
        # self.command_port = random.randint(2000, 10000)
        # self.data_port = command_port + 1
        
    def run(self, configs):
        self.configure()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST_IP, configs['commandChannelPort']))
            s.sendall(b'I am client 2')
            data = s.recv(1024)
            print(data)
            

configs = read_configs()
client = Client()
client.run(configs)