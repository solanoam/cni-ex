import socket
import json


class Host:

    def __inti__(self, logger, sock=None, **kwargs):
        self.target_ip = kwargs["target_ip"]
        self.target_port = kwargs["target_port"]
        self.pack_size = kwargs["pack_size"]
        self.logger = logger
        self.socket = self.init_socket() if not sock else sock

    def init_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
            return sock
        except Exception as e:
            self.logger.exception(e)

    def transmit(self, msg):
        try:
            self.socket.connect(self.target_ip, self.target_port)  # connect to server
            self.socket.sendall(json.dumps(msg).encode())  # send message to server
        except Exception as e:
            self.logger.exception(e)

    def receive(self):
        try:
            self.socket.bind((self.target_ip, self.target_port))
            self.socket.listen()  # wait for connection
            conn, addr = self.socket.accept()
            self.logger.info(f"connected. connection info - {conn} {addr} ")
            msg = conn.recv(self.pack_size)
            self.logger.info(f"got message {msg}")
            return msg
        except Exception as e:
            self.logger.exception(e)
