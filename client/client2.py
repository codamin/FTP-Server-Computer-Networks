import socket
import random
import json
import time
import sys
import os
from termcolor import colored

sys.path.append(os.path.abspath('../'))
from defs import *

def read_configs():
    configs = open(CONFIG_PATH).read()
    configs_dict = json.loads(configs)
    return configs_dict
    

class Client:        
    def connectToServer(self):
        self.command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_sock.connect((HOST_IP, commandChannelPort))

    def send(self, msg):
        self.command_sock.sendall(msg.encode('utf-8'))

    def recv(self):
        print(colored(self.command_sock.recv(RECV_SIZE).decode('utf-8'), 'red'))

    def User(self, user_name):
        self.send('USER {}'.format(user_name))
        self.recv()

    def Pass(self, password):
        self.send('PASS {}'.format(password))
        self.recv()

    def Pwd(self):
        self.send('PWD')
        self.recv()
    
    def Mkd(self, name):
        self.send('MKD {}'.format(name))
        self.recv()
    
    def Mkdi(self, name):
        self.send('MKD -i {}'.format(name))
        self.recv()
    
    def Rmd(self, name):
        self.send('RMD {}'.format(name))
        self.recv()
    
    def Rmdf(self, name):
        self.send('RMD -f {}'.format(name))
        self.recv()
    
    
    



if __name__ == "__main__":
    # READ CONFIGS
    configs = read_configs()
    commandChannelPort = configs['commandChannelPort']

    #CREATE CLIENT
    client = Client()
    client.connectToServer()
    client.User('hoenza')
    client.Pass('8585')
    
    # COMMANDS
    while(True):
        command1 = input('ENTER COMMAND: ')
        command = command1.split()
        if command[0].lower() == 'user':
            client.User(command[1])
        if command[0].lower() == 'pass':
            client.Pass(command[1])
        if command[0].lower() == 'pwd':
            client.Pwd()
        if command[0].lower() == 'mkd':
            if len(command) == 3:
                if command[1] != '-i':
                    client.Mkdi(command[1])
                else:
                    client.Mkd(command[2])
            else:
                client.Mkd(command[1])
        if command[0].lower() == 'rmd':
            if len(command) == 3:
                if command[1] != '-f':
                    client.Rmdf(command[1])
                else:
                    client.Rmdf(command[2])
            else:
                client.Rmd(command[1])
        


        else:
            # client.Mkd(command[1])
            client.send(command1)
