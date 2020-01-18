import socket
import json


class Host:

    def __inti__(self, logger, server=None, **kwargs):
        self.logger = logger
        self.is_server = server
        self.ip = kwargs["ip"]
        self.port = kwargs["port"]
        self.pack_size = kwargs["pack_size"]
        self.socket = self.init_socket()

    def init_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
            if self.is_server:
                self.init_server_connection()
            return sock
        except Exception as e:
            self.logger.exception(e)

    def transmit(self, msg):
        try:
            self.socket.connect(self.ip, self.port)  # connect to server
            self.socket.sendall(json.dumps(msg).encode())  # send message to server
        except Exception as e:
            self.logger.exception(e)

    def receive(self):
        try:

            msg = self.socket.recv(self.pack_size)
            self.logger.info(f"got message {msg}")
            return msg
        except Exception as e:
            self.logger.exception(e)

    def init_server_connection(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen()  # wait for connection
        conn, addr = self.socket.accept()
        self.logger.info(f"connected. connection info - {conn} {addr} ")
