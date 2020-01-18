import threading
from CardGameDealer import CardGameDealer
from Host import Host
from Logger import Logger
from ServerOptions import server_params, logging_level


class Server(Host):
    def __init__(self, logger, sock=None, **kwargs):
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


Server(Logger(logging_level), **server_params).await_game_requests()
