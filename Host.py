import socket, sys, json
from Logger import Logger, LoggingLevel

ip = "0.0.0.0"
m_port = 7000
pack_size = 1024
log_level = LoggingLevel.DEBUG.value

if len(sys.argv) is not 4:  # check the number of arguments sent by user is correct
    print('''
          not enough variables.
          please try again and insert 3 variables.
          ''')
    exit(-1)
else:
    argv_obj = {"a_or_b": sys.argv[1], "partner_ip": sys.argv[2], "m_ip_addr": sys.argv[3]}  # initialize variables
    if argv_obj["a_or_b"] is 'a':
        local_port = 6000
    if argv_obj["a_or_b"] is 'b':
        local_port = 5000


class Server(object):

    def __inti__(self, **kwargs):
        self.ip = kwargs["ip"]
        self.m_port = kwargs["m_port"]
        self.pack_size = kwargs["pack_size"]
        self.logger = Logger(log_level)
        self.socket = self.init_socket()

    def init_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
            return sock
        except Exception as e:
            self.logger.exception(e)

    def transmit(self, ip, port, msg):
        try:
            self.socket.connect(ip, port)  # connect to server
            self.socket.sendall(json.dumps(msg).encode())  # send message to server
        except Exception as e:
            self.logger.exception(e)

    def receive(self):
        try:
            self.socket.bind((ip, local_port))
            self.socket.listen()  # wait for connection
            conn, addr = self.socket.accept()
            self.logger.info(f"connected. connection info - {conn} {addr} ")
            msg = conn.recv(self.pack_size)
            self.logger.info(f"got message {msg}")
            return msg
        except Exception as e:
            self.logger.exception(e)
