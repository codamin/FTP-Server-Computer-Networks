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
        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_sock.connect((HOST_IP, dataChannelPort))

    def send(self, msg):
        self.command_sock.sendall(msg.encode('utf-8'))

    def recv(self):
        resp = self.command_sock.recv(RECV_SIZE).decode('utf-8')
        print(colored(resp, 'red'))
        return(resp)

    def recv_file(self, fileName):
        if os.path.isfile(os.path.join('./', fileName)):
            os.remove(os.path.join('./', fileName))
        
        file = open(os.path.join('./', fileName), 'w+')

        recv_data = self.data_sock.recv(RECV_SIZE).decode('utf-8')
        file.write(recv_data)
        file.close()

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
        print('sending MKD -i {}'.format(name))
        self.send('MKD -i {}'.format(name))
        self.recv()
    
    def Rmd(self, name):
        self.send('RMD {}'.format(name))
        self.recv()
    
    def Rmdf(self, name):
        self.send('RMD -f {}'.format(name))
        self.recv()
    
    def List(self):
        self.send('LIST')
        self.recv()
        self.recv_file('LIST')

    def Cwd(self, path):
        print('sending ', 'CWD {}'.format(path))
        self.send('CWD {}'.format(path))
        self.recv()

    def Dl(self, file):
        self.send('DL {}'.format(file))
        res = self.recv()
        if res[:3] == '226':
            self.recv_file(file)
    
    def Help(self):
        self.send('HELP')
        self.recv()
    
    def Quit(self):
        self.send('QUIT')
        self.recv()



if __name__ == "__main__":
    # READ CONFIGS
    configs = read_configs()
    commandChannelPort = configs['commandChannelPort']
    dataChannelPort = configs['dataChannelPort']

    #CREATE CLIENT
    client = Client()
    client.connectToServer()
    client.User('amin')
    client.Pass('329')
    
    # COMMANDS
    while(True):
        command1 = input('ENTER COMMAND: ')
        command = command1.split()
        if command[0].lower() == 'user':
            client.User(command[1])
        elif command[0].lower() == 'pass':
            client.Pass(command[1])
        elif command[0].lower() == 'pwd':
            client.Pwd()
        elif command[0].lower() == 'mkd':
            if len(command) == 3:
                if command[1] != '-i':
                    client.Mkdi(command[1])
                else:
                    client.Mkdi(command[2])
            else:
                client.Mkd(command[1])
        elif command[0].lower() == 'rmd':
            if len(command) == 3:
                if command[1] != '-f':
                    client.Rmdf(command[1])
                else:
                    client.Rmdf(command[2])
            else:
                client.Rmd(command[1])
        elif command[0].lower() == 'list':
            client.List()
        elif command[0].lower() == 'cwd':
            if len(command) == 1:
                client.Cwd("")
            else:
                client.Cwd(command[1])
        elif command[0].lower() == 'dl':
            if len(command) > 1:
                client.Dl(command[1])
        elif command[0].lower() == 'help':
            client.Help()
        elif command[0].lower() == 'quit':
            client.Quit()
        else:
            client.send(command1)