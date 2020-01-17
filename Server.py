import threading
import sys
from CardGameDealer import CardGameDealer
from Host import Host
from Logger import Logger, LoggingLevel

class Server(Host):
    def __inti__(self, logger, sock=None, **kwargs):
        super().__init__(self, **kwargs)
        self.threads = [None, None]

    def build_connection_params(self, client_msg):
        return {
            "target_ip": client_msg['target_ip'],
            "target_port": client_msg["target_port"],
            "pack_size": client_msg["pack_size"]
        }

    def add_game_thread(self, connection_params):
        for i, t in enumerate(self.threads):
            if not t or not t.isAlive():
                self.threads[i] = threading.Thread(target=self.start_game, args=(connection_params,))

    def await_game_requests(self):
        msg = self.receive()
        connection_params = self.build_connection_params(msg)
        self.add_game_thread(connection_params)

    def start_game(self, connection_params):
        CardGameDealer(self.logger, self.socket, **connection_params).play_game()

ip = "0.0.0.0"
port = 7000
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

server_params = {
    "target_ip": "127.0.0.1",
    "target_port": 3301,
    "pack_size": 1024
}
Server(Logger(1), **server_params).await_game_requests()