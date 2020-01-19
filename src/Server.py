"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
repo - https://github.com/solanoam/cni-ex
"""

import threading
from src.CardGameDealer import CardGameDealer
from src.Host import Host
from options.ServerOptions import server_ports


class Server(Host):
    """
    managing a server instance
    """
    def __init__(self, logger, **kwargs):
        """
        constructor
        :param logger: logger
        :param kwargs: inherited params
        """
        super().__init__(logger, True, **kwargs)
        self.threads = [None, None]
        self.ports = server_ports

    def add_game_thread(self):
        """
        manage adding a new game thread or rejecation. limited to the initial number of objects in the instance threads
        array.
        """
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
        """
        waiting for incoming requests for games
        :return:
        """
        while True:
            self.logger.debug(f"waiting for game requests")
            msg = self.init_socket()
            if self.is_start_game_request(msg):
                self.logger.debug(f"trying to find room")
                self.add_game_thread()

    def is_start_game_request(self, msg):
        """
        check weather the request is a start game by parsing the client message
        :param msg: client message
        :return: boolean
        """
        return msg.get("game_start")

    def start_game(self, connection_params):
        """
        starts a new server for the game
        :param connection_params: connection params for running the new server
        """
        CardGameDealer(self.logger, **connection_params).init_game()

    def build_game_start_msg(self, thread_num):
        """
        building a response for the client to which it needs to address to start the new game
        :param thread_num: which thread number in the thread array should be initialized
        :return: connection params dictionary object
        """
        return {
            "game_start": True,
            "ip": self.ip,
            "port": self.ports[thread_num],
            "pack_size": self.pack_size
        }

    def build_game_rejection_msg(self):
        """
        build rejection response for the server
        """
        return {"game_start": False}

    def build_connection_params(self, thread_num):
        """
        build new server connection params. synced with the client message.
        :param thread_num: which thread number in the thread array should be initialized
        :return:
        """
        return {
            "ip": self.ip,
            "port": self.ports[thread_num],
            "pack_size": self.pack_size
        }



