from CardGamePlayer import CardGamePlayer
from ClientOptions import logging_level, client_params
from Host import Host
from Logger import Logger


class Client(Host):
    def __init__(self, logger, sock, **kwargs):
        super().__init__(self, logger, sock, **kwargs)

    def init_game(self):
        CardGamePlayer(self.logger, self.socket, **self.build_connection_params()).play_game()

    def build_connection_params(self):
        return {
            "target_ip": self.target_ip,
            "target_port": self.target_port,
            "pack_size": self.pack_size
        }


Client(Logger(logging_level), **client_params).init_game()
