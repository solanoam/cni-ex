import threading
from CardGameDealer import CardGameDealer
from Host import Host
from Logger import Logger
from ServerOptions import server_params, logging_level, server_ports


class Server(Host):
    def __init__(self, logger, **kwargs):
        super().__init__(self, logger, True, **kwargs)
        self.threads = [None, None]
        self.ports = server_ports

    def add_game_thread(self):
        for i, t in enumerate(self.threads):
            if not t or not t.isAlive():
                connection_params = self.build_connection_params(i)
                t_num, self.threads[i] = threading.Thread(target=self.start_game, args=(connection_params,))
                self.logger.debug(f"started game with thread {t_num}")
                msg = self.build_game_start_msg(i)
                return self.transmit(msg)
        rejection_msg = self.build_game_rejection_msg()
        return self.transmit(rejection_msg)

    def await_game_requests(self):
        while True:
            msg = self.receive()
            if self.is_start_game_request(msg):
                self.add_game_thread()

    def is_start_game_request(self, msg):
        return msg.get("start_game")

    def start_game(self, connection_params):
        CardGameDealer(self.logger, **connection_params).init_game()

    def build_game_start_msg(self, thread_num):
        return {
            "game_started": True,
            "ip": self.ip,
            "port": self.ports[thread_num],
            "pack_size": self.pack_size
        }

    def build_game_rejection_msg(self):
        return {"game_started": False}

    def build_connection_params(self, thread_num):
        return {
            "ip": self.ip,
            "port": self.ports[thread_num],
            "pack_size": self.pack_size
        }


Server(Logger(logging_level), **server_params).await_game_requests()
