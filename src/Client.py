"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
repo - https://github.com/solanoam/cni-ex
"""

from src.CardGamePlayer import CardGamePlayer
from src.Host import Host


class Client(Host):
    """
    class managing a client instance that inherit logic from Host
    """
    def __init__(self, logger, **kwargs):
        super().__init__(logger, **kwargs)
        self.init_socket()

    def init_game(self):
        """
        initialize a game and handle success or failure while communicating with the server
        """
        start_msg = self.build_start_game_msg()
        self.transmit(start_msg)
        msg = self.receive()
        if not self.is_start_game(msg):
            return self.handle_game_denial()

        CardGamePlayer(self.logger, **self.build_connection_params(msg)).init_game()

    def build_connection_params(self, msg):
        """
        build a client initialization build params to point to the available listening game server
        :param msg: server response message
        :return: init params for a client
        """
        return {
            "ip": msg["ip"],
            "port": msg["port"],
            "pack_size": msg["pack_size"]
        }

    def is_start_game(self, msg):
        """
        check response whether the server confirmed available for a game or not
        :param msg:
        :return:
        """
        return msg.get('game_start')

    def handle_game_denial(self):
        """
        handle game rejection
        :return:
        """
        self.logger.info(f"the server isn't available for anymore games, closing...")
        exit(1)

    def build_start_game_msg(self):
        """
        build a start game response to be sent as a confirmation
        :return: dictionary
        """
        return {"game_start": True}
