import socket
import json


class Host:

    def __init__(self, logger, server=None, **kwargs):
        self.logger = logger
        self.is_server = server
        self.ip = kwargs["ip"]
        self.port = kwargs["port"]
        self.pack_size = kwargs["pack_size"]
        self.socket = None

    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.is_server:
            return self.init_server_connection()
        else:
            self.init_client_connection()

    def transmit(self, msg):
        try:
            self.logger.debug(f"sending message: {msg}")
            self.socket.sendall(json.dumps(msg).encode())  # send message to server
        except Exception as e:
            self.logger.exception(e)

    def receive(self):
        try:
            msg = self.socket.recv(self.pack_size)
            self.logger.debug(f"got message: {msg}")
            return json.loads(msg)
        except Exception as e:
            self.logger.exception(e)

    def init_server_connection(self):
        self.socket.bind((self.ip, self.port))
        self.logger.info(f"waiting for connection on {self.ip}:{self.port}")
        self.socket.listen()  # wait for connection
        self.socket, addr = self.socket.accept()
        self.logger.info(f"connected. connection info - {self.socket} {addr} ")
        return self.receive()

    def init_client_connection(self):
        try:
            self.socket.connect((self.ip, self.port))  # connect to server
        except Exception as e:
            self.logger.exception(e)

    def close_connection(self):
        self.logger.debug(f"closing socket {self.socket}")
        self.socket.close()

