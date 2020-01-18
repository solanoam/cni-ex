from CardGamePlayer import CardGamePlayer
from ClientOptions import logging_level, client_params
from Host import Host
from Logger import Logger


class Client(Host):
    def __init__(self, logger, sock, **kwargs):
        super().__init__(self, logger, sock, **kwargs)

    def init_game(self):
        start_msg = self.build_start_game_msg()
        self.transmit(start_msg)
        msg = self.receive()
        if self.is_start_game_failed(msg):
            return self.handle_game_denial()

        CardGamePlayer(self.logger, **self.build_connection_params(msg)).init_game()

    def build_connection_params(self, msg):
        return {
            "target_ip": msg["target_ip"],
            "target_port": msg["target_port"],
            "pack_size": msg["pack_size"]
        }

    def is_start_game_failed(self, msg):
        return msg.get('game_deny')

    def handle_game_denial(self):
        self.logger(f"the server isn't available for anymore games, closing...")
        exit(1)

    def build_start_game_msg(self):
        return {"game_start": True}


Client(Logger(logging_level), **client_params).init_game()
