    def handle_list(self):
        dir_list = os.listdir(self.session_user.dir)
        dir_str = '\n'.join(dir_list)
        data_sock.send(dir_str)
        data_sock.send('')


    def recv_data(self, fileName):
        os.remove(os.path.join('./', fileName))
        file = open(os.path.join('./', fileName), 'w+')

        recv_data = self.data_sock.recv(RECV_SIZE)
        while recv_data:
            file.write(recv_data)
            recv_data = self.data_sock.recv(RECV_SIZE)
        file.close()


    listen_command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("listen command on ", HOST_IP, self.command_port)
        listen_command_socket.bind((HOST_IP, self.command_port))
        listen_command_socket.listen()

        print("listen data on ", HOST_IP, self.data_port)
        listen_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_data_socket.bind((HOST_IP, self.data_port))
        listen_data_socket.listen()

        # listen_command_socket.setblocking(0)
        # listen_data_socket.setblocking(0)
        TIMEOUT = 1
        listen_sockets = [listen_command_socket, listen_data_socket]
        while True:
            sock_command, addr1 = listen_command_socket.accept()
            sock_data, addr2 = listen_data_socket.accept()
            newThread = ClientThread(client_command_addr, client_command_socket)
            newThread.start()