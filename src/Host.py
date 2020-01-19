"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
repo - https://github.com/solanoam/cni-ex
"""

import socket
import json

class Host:
    """
    logic of host management that support both server and client instantiations
    """
    def __init__(self, logger, server=None, **kwargs):
        """
        constructor
        :param logger: logger
        :param server: is this is a server instance
        :param kwargs: ip - port - packet size
        """
        self.logger = logger
        self.is_server = server
        self.ip = kwargs["ip"]
        self.port = kwargs["port"]
        self.pack_size = kwargs["pack_size"]
        self.socket = None

    def init_socket(self):
        """
        init a socket
        :return: socket
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.is_server:
            return self.init_server_connection()
        else:
            return self.init_client_connection()

    def transmit(self, msg):
        """
        transmit a message to the target port
        :param msg: a dictionary
        """
        try:
            self.logger.debug(f"sending message: {msg}")
            self.socket.sendall(json.dumps(msg).encode())  # send message to server
        except Exception as e:
            self.logger.exception(e)

    def receive(self):
        """
        recive a message from the connected target
        :return: a dictionary parsed for the json string
        """
        try:
            msg = self.socket.recv(self.pack_size)
            self.logger.debug(f"got message: {msg}")
            return json.loads(msg)
        except Exception as e:
            self.logger.exception(e)

    def init_server_connection(self):
        """
        initialize a listening server
        :return:
        """
        self.socket.bind((self.ip, self.port))
        self.logger.info(f"waiting for connection on {self.ip}:{self.port}")
        self.socket.listen()  # wait for connection
        self.socket, addr = self.socket.accept()
        self.logger.info(f"connected. connection info - {self.socket} {addr} ")
        return self.receive()

    def init_client_connection(self):
        """
        initialize a client
        :return:
        """
        try:
            self.socket.connect((self.ip, self.port))  # connect to server
        except Exception as e:
            self.logger.exception(e)

    def close_connection(self):
        """
        close a socket
        """
        self.logger.debug(f"closing socket {self.socket}")
        self.socket.close()

