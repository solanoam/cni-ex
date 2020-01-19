"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
repo - https://github.com/solanoam/cni-ex
"""

from src.Host import Host
from src.Deck import Deck

class CardGameDealer(Host):
    def __init__(self, logger, **kwargs):
        """
        constructor
        :param logger: logger
        :param kwargs: inherited params
        """
        super().__init__(logger, True, **kwargs)
        self.init_socket()
        self.deck = Deck(self.logger)
        self.round = 0
        self.player_earnings = 0
        self.tie = False
        self.player_card = None
        self.dealer_card = None
        self.bet = 0

    def init_game(self):
        """
        initializing a game
        :return:
        """
        self.logger.debug(f"starting to a new game")
        self.play_game()

    def play_game(self):
        """
        manages a game and its end
        """
        while len(self.deck) > 0:
            self.logger.info(f"deck length is {len(self.deck)}")
            self.round += 1
            self.handle_game_turn()
        self.logger.info("game concluded")
        self.handle_game_termination()

    def handle_game_turn(self):
        """
        handle a given turn in the game and all of the communications with the client
        :return:
        """
        self.logger.debug(f"handling turn")
        self.handle_player_turn()
        winner = self.handle_dealer_turn()
        if not self.tie:
            end_of_round_msg = self.build_end_of_round_msg(winner)
            self.send_msg_to_player(end_of_round_msg)
        else:
            self.tie = False


    def handle_dealer_turn(self):
        """
        handling the dealer turn and the followed logic
        :return: the round winner (player / dealer / no one (surrender))
        """
        self.logger.debug(f"handling dealer turn")
        self.dealer_card = self.deck.draw_card()
        return self.calculate_winner()

    def calculate_winner(self):
        """
        calculate the winner of the round
        :return: player / dealer / no one
        """
        if self.player_card == self.dealer_card:
            return self.handle_tie() if not self.tie else self.conclude_tie_after_war("player")
        winner = "player" if self.player_card > self.dealer_card else "dealer"
        self.player_earnings += self.bet if self.player_card > self.dealer_card else -self.bet
        return winner

    def handle_player_turn(self):
        """
        handling the player turn and the followed logic and communications with the client
        :return:
        """
        self.logger.debug(f"handling player turn")
        self.player_card = self.deck.draw_card()
        msg = self.build_player_card_msg(self.player_card)
        self.send_msg_to_player(msg)
        player_msg = self.await_player_turn_response()
        if self.is_game_terminated_by_player(player_msg):
            return self.handle_game_termination()
        self.bet = self.parse_player_bet(player_msg)

    def handle_game_termination(self):
        """
        handles game termination by the player
        """
        termination_msg = self.build_termination_msg()
        self.send_msg_to_player(termination_msg)
        self.logger.info("termination msg was sent to the user")
        exit(1)

    def handle_tie(self):
        """
        handle the logic for a tie
        """
        self.tie = True
        tie_msg = self.build_tie_msg()
        self.send_msg_to_player(tie_msg)
        player_tie_msg = self.await_player_turn_response()
        player_tie_decision = self.parse_tie_decision(player_tie_msg)
        if player_tie_decision:
            for i in range(3):
                self.deck.draw_card()
            self.dealer_card = self.deck.draw_card()
            self.bet *= 2
            winner = self.calculate_winner()
            return self.conclude_tie_after_war(winner)
        else:
            self.tie = False
            return "no one"

    def conclude_tie_after_war(self, winner):
        """
        handle the communications after a tie
        :param winner:
        :return:
        """
        end_of_tie_msg = self.build_end_of_tie_msg(winner)
        self.send_msg_to_player(end_of_tie_msg)

    def parse_tie_decision(self, player_tie_msg):
        """
        parse the chosen response from the player
        :param player_tie_msg: client message
        :return: boolean
        """
        return player_tie_msg.get("tie_decision")

    def send_msg_to_player(self, msg):
        """
        send a message to the client
        :param msg: a dictionary based message
        """
        self.transmit(msg)

    def await_player_turn_response(self):
        """
        awaiting a response from the client
        :return: a dictionary based message
        """
        return self.receive()

    def parse_player_bet(self, player_msg):
        """
        parse the player bet from the client response
        :param player_msg: client message
        :return:
        """
        return int(player_msg['player_bet'])

    def is_game_terminated_by_player(self, player_msg):
        """
        parse the decision to terminate the game from a client message
        :param player_msg: client message
        :return: boolean
        """
        return player_msg.get('terminate')

    def build_end_of_round_msg(self, winner):
        """
        build end of round summery message to be sent to the client
        :param winner:
        :return: a summery of the round dictionary
        """
        return {
            "dealer_card": str(self.dealer_card),
            "player_card": str(self.player_card),
            "bet": self.bet,
            "round": self.round,
            "winner": winner
        }

    def build_end_of_tie_msg(self, winner):
        """
        build the end of tie summery message to be sent to the client
        :param winner: who won
        :return: a summery of tie round dictionary
        """
        return {
            "dealer_card": str(self.dealer_card),
            "player_card": str(self.player_card),
            "bet": self.bet,
            "round": self.round,
            "winner": winner,
            "original_bet": self.bet/2
        }

    def build_termination_msg(self):
        """
        build an end of game message to be sent to the client
        :return: end of game message dictionary
        """
        return {
            "player_earnings": self.player_earnings,
            "round": self.round,
            "termination": True
        }

    def build_tie_msg(self):
        """
        build a tie status message to be sent to the client
        :return: a dictionary based tie summery message
        """
        return {
            "round": str(self.round),
            "tie": True,
            "dealer_card": str(self.dealer_card),
            "player_card": str(self.player_card),
            "bet": str(self.bet)
        }

    def build_player_card_msg(self, player_card):
        """
        build a player card message to be sent to the client
        :param player_card: the player drawn card
        :return: a dictionary based card message
        """
        return {"player_card": str(player_card)}
