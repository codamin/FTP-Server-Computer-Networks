import json
import socket
from threading import Thread

from defs import *
from user import User

def read_configs():
    configs = open(CONFIG_PATH).read()
    configs_dict = json.loads(configs)
    return configs_dict

class ClientThread(Thread):
    def __init__(self, client_address, client_socket):
        Thread.__init__(self)
        self.sock = client_socket
    def run(self):
        while True:
            data = self.sock.recv(20)
            print(data)
            if not(data):
                break
            self.sock.sendall(data)


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
                if user.id == accounting_user['user']:
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


configs = read_configs()
server = Server(configs)
server.run()