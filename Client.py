from CardGamePlayer import CardGamePlayer
from ClientOptions import logging_level, client_params
from Host import Host
from Logger import Logger


class Client(Host):
    def __init__(self, logger, **kwargs):
        super().__init__(logger, **kwargs)
        self.init_socket()

    def init_game(self):
        start_msg = self.build_start_game_msg()
        self.transmit(start_msg)
        msg = self.receive()
        if not self.is_start_game(msg):
            return self.handle_game_denial()

        CardGamePlayer(self.logger, **self.build_connection_params(msg)).init_game()

    def build_connection_params(self, msg):
        return {
            "ip": msg["ip"],
            "port": msg["port"],
            "pack_size": msg["pack_size"]
        }

    def is_start_game(self, msg):
        return msg.get('game_start')

    def handle_game_denial(self):
        self.logger.info(f"the server isn't available for anymore games, closing...")
        exit(1)

    def build_start_game_msg(self):
        return {"game_start": True}


Client(Logger(logging_level), **client_params).init_game()
