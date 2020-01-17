from Host import Host
from Deck import Deck

class CardGameDealer(Host):
    def __init__(self, logger, sock, **kwargs):
        super().__init__(self, logger, sock, **kwargs)
        self.deck = Deck(self.logger)
        self.round = 0
        self.player_earnings = 0
        self.tie = False
        self.player_card = None
        self.dealer_card = None
        self.bet = 0

    def play_game(self):
        while len(self.deck) >= 0:
            self.round += 1
            self.handle_game_turn()
        self.logger.info("game concluded")

    def handle_game_turn(self):
        self.handle_player_turn()
        if not self.player_card and not self.bet: return
        winner = self.handle_dealer_turn()
        if not self.tie:
            end_of_round_msg = self.build_end_of_round_msg(winner)
            self.send_msg_to_player(end_of_round_msg)
        else:
            self.tie = True

    def handle_dealer_turn(self):
        self.dealer_card = self.deck.draw_card()
        return self.calculate_winner()

    def calculate_winner(self):
        if self.player_card == self.dealer_card:
            return self.handle_tie() if not self.tie else self.conclude_tie_after_war("player")
        winner = "player" if self.player_card > self.dealer_card else "dealer"
        self.logger(f"the winner of round {self.round} is {winner}")
        return winner

    def handle_player_turn(self):
        self.player_card = self.deck.draw_card()
        msg = self.build_player_card_msg(self.player_card)
        self.send_msg_to_player(msg)
        player_msg = self.await_player_turn_response()
        if self.is_game_terminated_by_player(player_msg):
            return self.handle_game_termination()
        self.bet = self.parse_player_bet(player_msg)

    def handle_game_termination(self):
        termination_msg = self.build_termination_msg()
        self.send_msg_to_player(termination_msg)
        self.logger.info("termination msg was sent to the user")
        self.deck.destroy_deck()
        self.logger.info("deck was destroyed")
        self.player_card = False
        self.bet = False

    def handle_tie(self):
        self.tie = True
        tie_msg = self.build_tie_msg()
        self.send_msg_to_player(tie_msg)
        player_tie_msg = self.await_player_turn_response()
        player_tie_decision = self.parse_tie_decision(player_tie_msg)
        if player_tie_decision == 'war':
            for i in range(3):
                self.deck.draw_card()
            self.dealer_card = self.deck.draw_card()
            self.bet *= 2
            winner = self.calculate_winner()
            return self.conclude_tie_after_war(winner)

    def conclude_tie_after_war(self, winner):
        end_of_tie_msg = self.build_end_of_tie_msg(winner)
        self.send_msg_to_player(end_of_tie_msg)

    def parse_tie_decision(self, player_tie_msg):
        return player_tie_msg.get("tie_decision")

    def send_msg_to_player(self, msg):
        self.transmit(msg)

    def await_player_turn_response(self):
        return self.receive()

    def parse_player_bet(self, player_msg):
        return player_msg['player_bet']

    def is_game_terminated_by_player(self, player_msg):
        return player_msg['terminate']

    def build_end_of_round_msg(self, winner):
        return {"dealer_card": str(self.dealer_card), "player_card": str(self.player_card), "bet": self.bet, "round": self.round, "winner": winner}

    def build_end_of_tie_msg(self, winner):
        return {"dealer_card": str(self.dealer_card), "player_card": str(self.player_card), "bet": self.bet, "round": self.round, "winner": winner, "original_bet": self.bet/2}

    def build_termination_msg(self):
        return {"player_earnings": self.player_earnings, "round": self.round, "termination": True}

    def build_tie_msg(self):
        return {"The result of round": str(self.round) , "is a tie!" ,"Dealer’s card": str(self.dealer_card) ,"Player’s card": str (self.player_card), "The bet": str(self.bet) }
         

    def build_player_card_msg(self, player_card):
        return {"player_card": str(player_card)}
