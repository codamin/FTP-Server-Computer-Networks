import socket
import random
import json
from defs import *

id = 'hoenza'
password = '8585'
RECV_SIZE = 1024

def read_configs():
    configs = open(CONFIG_PATH).read()
    configs_dict = json.loads(configs)
    return configs_dict
    

class Client:
    def __init__(self):
        self.id = id
        self.password = password
        self.is_signed_in = False
        
    def connectToServer(self):
        self.command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM):
        self.command_sock.connect((HOST_IP, commandChannelPort))

    def log_in():
        if self.is_signed_in:
            print("already singed in")
            return
        self.command_sock.sendall(USER + '' + self.id)
        res = self.command_sock.recv(RECV_SIZE)
        if res == '331 User name okay, need password.':
            self.command_sock.sendall(PASS + '' + self.password)
            res = self.command_sock.recv(RECV_SIZE)
            if res == '230 User logged in, proceed.':
                print('logged in successfully')



if __name__ == "__main__":
    # READ CONFIGS
    configs = read_configs()
    commandChannelPort = configs['commandChannelPort']

    #CREATE CLIENT
    client = Client()

    #COMMANDS
    while(True):
        command = input('ENTER COMMAND: ')
        client.connectToServer()
        client.log_in()