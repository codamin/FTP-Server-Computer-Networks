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