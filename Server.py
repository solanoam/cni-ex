import threading
from CardGameDealer import CardGameDealer
from Host import Host
from Logger import Logger
from ServerOptions import server_params, logging_level, server_ports


class Server(Host):
    def __init__(self, logger, **kwargs):
        super().__init__(logger, True, **kwargs)
        self.threads = [None, None]
        self.ports = server_ports

    def add_game_thread(self):
        for i, t in enumerate(self.threads):
            if not t or not t.isAlive():
                connection_params = self.build_connection_params(i)
                self.threads[i] = threading.Thread(target=self.start_game, args=(connection_params,))
                self.threads[i].start()
                msg = self.build_game_start_msg(i)
                self.transmit(msg)
                return self.close_connection()
        rejection_msg = self.build_game_rejection_msg()
        self.logger.info(f"rejected a game - server is full")
        return self.transmit(rejection_msg)

    def await_game_requests(self):
        while True:
            self.logger.debug(f"waiting for game requests")
            msg = self.init_socket()
            if self.is_start_game_request(msg):
                self.logger.debug(f"trying to find room")
                self.add_game_thread()

    def is_start_game_request(self, msg):
        return msg.get("game_start")

    def start_game(self, connection_params):
        CardGameDealer(self.logger, **connection_params).init_game()

    def build_game_start_msg(self, thread_num):
        return {
            "game_start": True,
            "ip": self.ip,
            "port": self.ports[thread_num],
            "pack_size": self.pack_size
        }

    def build_game_rejection_msg(self):
        return {"game_start": False}

    def build_connection_params(self, thread_num):
        return {
            "ip": self.ip,
            "port": self.ports[thread_num],
            "pack_size": self.pack_size
        }


Server(Logger(logging_level), **server_params).await_game_requests()
