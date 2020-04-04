import socket
import random
import json
import time
import sys
import os

sys.path.append(os.path.abspath('../'))
from defs import *

user_name = 'hoenza'
password = '8585'
RECV_SIZE = 1024

def read_configs():
    configs = open(CONFIG_PATH).read()
    configs_dict = json.loads(configs)
    return configs_dict
    

class Client:
    def __init__(self):
        self.user_name = user_name
        self.password = password
        self.is_signed_in = False
        
    def connectToServer(self):
        self.command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_sock.connect((HOST_IP, commandChannelPort))

    def log_in(self):
        if self.is_signed_in:
            print("already singed in")
            return
        self.command_sock.sendall('USER {}'.format(self.user_name).encode('utf-8'))
        res = self.command_sock.recv(RECV_SIZE).decode('utf-8').split(' ')
        print(res)
        if res[0] == NAME_OKAY_CODE:
            self.command_sock.sendall('PASS {}'.format(self.password).encode('utf-8'))
            res = self.command_sock.recv(RECV_SIZE).decode('utf-8').split(' ')
            print(res)
            if res[0] == LOG_IN_OKAY_CODE:
                print('logged in successfully')



if __name__ == "__main__":
    # READ CONFIGS
    configs = read_configs()
    commandChannelPort = configs['commandChannelPort']

    #CREATE CLIENT
    client = Client()

    client.connectToServer()
    client.log_in()
    #COMMANDS
    # while(True):
        # command = input('ENTER COMMAND: ')

