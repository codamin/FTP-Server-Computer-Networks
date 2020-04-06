import json
import socket
import os
import sys
from user import User
from threading import Thread, currentThread
import threading

sys.path.append(os.path.abspath('../'))
from defs import *

def read_configs():
    configs = open(CONFIG_PATH).read()
    configs_dict = json.loads(configs)
    return configs_dict

class ClientThread(Thread):
    def __init__(self, client_address, client_socket):
        Thread.__init__(self)
        self.sock = client_socket
        self.session_user = None

    def send(self, msg):
        self.sock.sendall(msg.encode('utf-8'))

    def run(self):
        while True:
            data = self.sock.recv(1024).decode('utf-8')
            if not data:
                break
            try:
                command = data.split(' ')[0]
                param = data.split(' ')[1:]

            except:
                pass

            print(data, command, param)
            self.handle_commands(command, param)

    def handle_commands(self, command, param):
        global server
        if command == 'USER':
            self.session_user = server.get_user(param[0])
            if self.session_user:
                self.send(NAME_OKAY_MSG)
            else:
                self.send(LOG_IN_FALED_MSG)


        elif command == 'PASS':
            if not self.session_user:
                self.send(BAD_SEQUENCE_MSG)
            elif self.session_user.password != param[0]:
                self.send(LOG_IN_FALED_MSG)
                self.session_user = None
            else:
                self.send(LOG_IN_OKAY_MSG)
        
        elif command == 'PWD':
            self.send(self.session_user.dir)
        
        elif command == 'MKD':
            if '-i' in param:
                open(param.remove('-i')[0]).close()
            else:
                print(param)
                os.makedirs(param[0])

class Server:

    def __init__(self, configs):
        self.command_port = configs['commandChannelPort']
        self.data_port = configs['dataChannelPort']
        self.init_users(configs['users'])
        self.init_accounting(configs['accounting'])

    def init_users(self, users):
        self.users = []
        for user in users:
            self.users.append(User(user['user'], user['password']))
    
    def init_accounting(self, accounting):
        self.accounting_enable = accounting['enable']
        self.accounting_threshold = accounting['threshold']
        accounting_users = set()
        for accounting_user in accounting['users']:
            for user in self.users:
                if user.user_name == accounting_user['user']:
                    user.size = accounting_user['size']
                    user.email = accounting_user['email']
                    user.alert = accounting_user['alert']
    
    def print_users(self):
        for user in self.users:
            user.print()
            print('#############')
    
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
            listen_socket.bind((HOST_IP, self.command_port))
            listen_socket.listen()
            while True:
                client_socket, client_address = listen_socket.accept()
                newThread = ClientThread(client_address, client_socket)
                newThread.start()

    def get_user(self, user_name):
        for user in self.users:
            if user.user_name == user_name:
                return user
        return None

configs = read_configs()
server = Server(configs)
server.run()