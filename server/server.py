import json
import socket
import select
import os
import sys
from user import User
from threading import Thread, currentThread
import threading
import datetime

sys.path.append(os.path.abspath('../'))
from defs import *

def read_configs():
    configs = open(CONFIG_PATH).read()
    configs_dict = json.loads(configs)
    return configs_dict

class ClientThread(Thread):
    def __init__(self, socket_command, socket_data):
        Thread.__init__(self)
        self.socket_command = socket_command
        self.socket_data = socket_data
        self.user_name = ""
        self.session_user = None
        self.mail_server_user_name = 'YW1pbmFzYWRpMzI5\r\n'.encode()
        self.mail_server_password = 'VXRhbWluMzI5'.encode()

    def send(self, msg):
        message = " ".join(msg)
        print('response ', message)
        self.socket_command.sendall(message.encode('utf-8'))

    def send_file(self, msg):
        self.socket_data.sendall(msg.encode('utf-8'))

    def run(self):
        while True:
            data = self.socket_command.recv(1024).decode('utf-8')
            if not data:
                break
            command = ''
            param = []
            tmp = data.split(' ')

            if len(tmp) > 0:
                command = tmp[0]
            if len(tmp) > 1:
                param = tmp[1:]

            self.handle_commands(command, param)

    def handle_commands(self, command, param):
        global server

        if command == 'USER':
            if len(param) < 1:
                return
            user = server.get_user(param[0])
            if user:
                self.user_name = user.user_name
                self.send([NAME_OKAY_MSG])
            else:
                self.send([LOG_IN_FALED_MSG])
        
        elif command == 'PASS':
            user = server.get_user(self.user_name)
            if not self.user_name:
                self.send([BAD_SEQUENCE_MSG])
            elif user.password != param[0]:
                self.send([LOG_IN_FALED_MSG])
            else:
                self.session_user = user
                self.handle_log("user " + self.session_user.user_name + " logged in successfully")
                self.send([LOG_IN_OKAY_MSG])
        
        elif command == 'PWD':
            self.handle_log('responded pwd request for user: ' + self.session_user.user_name)
            self.send([PWD_OKAY, self.session_user.dir])
        
        elif command == 'MKD':
            self.handle_mkd(param)
        
        elif command == 'RMD':
            self.handle_rmd(param)

        elif command == 'LIST':
            self.handle_list()

        elif command == 'CWD':
            self.handle_cwd(param)

        elif command == 'DL':
            self.handle_dl(param)
        
        elif command == 'HELP':
            self.handle_help()
        
        elif command == 'QUIT':
            self.handle_quit()

    def handle_log(self, msg):
        if server.logging_enable:
            file = open(server.logging_path, 'a')
            msg = str(datetime.datetime.today()) + '  ---  ' + msg + '\n'
            file.write(msg)
            file.close()

    def handle_quit(self):
        self.send([QUIT_OKAY, QUIT_OKAY_MSG])
        self.handle_log(self.session_user.user_name + "quit")
        sys.exit()
     
    def handle_help(self):
        resp = "\nUSER [name], It's argument is used to specify the user's string. It is used for user authentication.\n"
        self.send([HELP_OKAY, resp])
    
    def handle_dl(self, param):
        path = os.path.join(self.session_user.dir, param[0])

        if server.authorization_enable and server.is_admin_file(path):
            if not server.is_admin(self.session_user.user_name):
                self.handle_log('admin file was not available to user')
                self.send([NOT_AVAILABLE_CODE + " " + NOT_AVAILABLE_MSG])
                return

        if not os.path.isfile(path):
            self.handle_log('requestetd file does not exist')
            self.send(['requestetd file does not exist'])
            return

        file = open(path, 'r')
        info = file.read()
        if len(info) > int(self.session_user.size):
            self.send([OPEN_CONN_FAIL, OPEN_CONN_MSG])
        else:
            self.handle_log("file: " + path + " was sent to user")
            self.session_user.size = str(int(self.session_user.size) - len(info))
            # self.send_mail()
            self.send([LIST_OKAY, DL_OKAY_MSG])
            self.send_file(info)
    
    def send_mail(self):
        send = lambda msg: mail_socket.sendall(('msg' + '\r\n').encode())
        recv = lambda : print(mail_socket.recv(1024).decode())
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mail_socket:
            mail_socket.connect(('mail.ut.ac.ir', 25))
            recv()
            
            send('helo FtpServer')
            recv()

            send('auth login')
            recv()
            
            send('YW1pbmFzYWRpMzI5')
            recv()

            send('VXRhbWluMzI5')
            recv()

            send('mail from: <aminasadi329@ut.ac.ir>')
            recv()

            send('rcpt to: <aminasadi329@ymail.com>')
            recv()

            send('data')
            recv()

            send('subject: low capacity in ftp server')
            send('Hi! your capacity is lower than threashold')
            send('.')
            recv()
            
    def handle_cwd(self, param):
        if len(param) == 0:
            self.session_user.dir = os.getcwd()
        elif param[0] == '..':
            head, tail = os.path.split(self.session_user.dir)
            if head[-1] == '/':
                head = head[:-1]
            self.session_user.dir = head
        else:
            self.session_user.dir = os.path.join(self.session_user.dir, param[0])
        self.send([CWD_OKAY_MSG])

    def handle_list(self):
        dir_list = os.listdir(self.session_user.dir)
        dir_str = '\n'.join(dir_list)
        self.send_file(dir_str)
        self.send([LIST_OKAY, LIST_DONE])

    def handle_rmd(self, param):
        path = os.path.join(self.session_user.dir, param[0])

        if len(param) < 1:
            pass
        elif '-f' in param:
            param.remove('-f')
            path = os.path.join(self.session_user.dir, param[0])
            try:
                os.rmdir(path)
                self.handle_log(path + " folder remove")
                self.send([RMD_OKAY, path, RMD_PATH_DELETED])
            except:
                self.send("provided path is not a dir")
                self.handle_log("provided path is not a dir")
        else:
            os.remove(path)
            self.handle_log(path + " file remove")
            self.send([RMD_OKAY, path, RMD_PATH_DELETED])

    def handle_mkd(self, param):
        path = os.path.join(self.session_user.dir, param[0])
        if len(param) < 1:
            pass
        elif '-i' in param:
            param.remove('-i')
            path = os.path.join(self.session_user.dir, param[0])
            self.handle_log(path + " file create")
            open(path, 'w+').close()
            self.send([PWD_OKAY, path, MKD_PATH_CREATED])
        else:
            self.handle_log(path + " folder create")
            os.makedirs(path)
            self.send([PWD_OKAY, path, MKD_PATH_CREATED])


class Server:

    def __init__(self, configs):
        self.command_port = configs['commandChannelPort']
        self.data_port = configs['dataChannelPort']
        self.init_users(configs['users'])
        self.init_accounting(configs['accounting'])
        self.init_logging(configs['logging'])
        self.init_authorization(configs['authorization'])

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

    def init_authorization(self, authorization):
        self.admins = authorization['admins']
        self.admin_files = authorization['files']
        self.authorization_enable = ['authorization.enable']
    
    def init_logging(self, logging):
        self.logging_enable = logging['enable']
        self.logging_path = logging['path']

    def print_users(self):
        for user in self.users:
            user.print()
            print('#############')

    def is_admin_file(self, path):
        return path in self.admin_files

    def is_admin(self, user_name):
        return user_name in self.admins
            
    def run(self):
        listen_command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_command_socket.bind((HOST_IP, self.command_port))
        listen_command_socket.listen()

        listen_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_data_socket.bind((HOST_IP, self.data_port))
        listen_data_socket.listen()

        while True:
            sock_command, addr1 = listen_command_socket.accept()
            sock_data, addr2 = listen_data_socket.accept()
            newThread = ClientThread(sock_command, sock_data)
            newThread.start()

    def get_user(self, user_name):
        for user in self.users:
            if user.user_name == user_name:
                return user
        return None

configs = read_configs()
server = Server(configs)
server.run()