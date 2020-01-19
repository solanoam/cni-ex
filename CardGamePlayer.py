from Host import Host
from Card import Card


class CardGamePlayer(Host):
    def __init__(self, logger, **kwargs):
        super().__init__(logger, **kwargs)
        self.init_socket()
        self.player_bet = 0
        self.player_card = None
        self.dealer_card = None
        self.is_terminated = False

    def init_game(self):
        msg = self.build_init_msg()
        self.send_msg_to_dealer(msg)
        self.play_game()

    def play_game(self):
        while not self.is_terminated:
            self.handle_game_turn()

    def handle_game_turn(self):
        self.handle_player_turn()
        dealer_msg = self.await_response_from_dealer()
        if self.is_tie(dealer_msg):
            return self.handle_tie(dealer_msg)
        self.prompt_round_outcome(dealer_msg)

    def prompt_round_outcome(self, msg):
        self.logger.info(f"the outcome for this round: {msg['round']}")
        self.logger.info(f"winner is {msg['winner']} with a bet of {msg['bet']} { '(original bet was ' + str(int(msg['original_bet'])) + ')' if msg.get('original_bet') else ''}, player card - {msg['player_card']}, dealer card - {msg['dealer_card']}:")

    def handle_player_turn(self):
        msg = self.await_response_from_dealer()
        if self.is_game_terminated(msg):
            self.prompt_termination_msg(msg)
            exit(1)
        given_card = self.parse_dealer_bet_request(msg)
        player_msg = self.ask_for_player_bet(given_card)
        self.send_msg_to_dealer(player_msg)

    def handle_tie(self, dealer_tie_msg):
        user_input = self.handle_tie_prompt(dealer_tie_msg)
        tie_msg = self.build_player_tie_msg(user_input)
        self.send_msg_to_dealer(tie_msg)
        if not user_input:
            self.logger.info(f"not going to war and moving to the next round")
        msg = self.await_response_from_dealer()
        return self.prompt_round_outcome(msg)

    def handle_tie_prompt(self, dealer_tie_msg):
        self.logger.info(f"its a tie. Dealer Card: {dealer_tie_msg['dealer_card']}, Player Card: {dealer_tie_msg['player_card']}")
        self.logger.info("Do you wish to go to war?")
        user_input = self.handle_tie_input()
        return user_input

    def handle_tie_input(self):
        while True:
            self.logger.info(" # Y - Yes # N - No #")
            user_input = input()

            if self.validate_input(user_input, "Y"):
                return True

            elif self.validate_input(user_input, "N"):
                return False

            else:
                self.logger.info("Please choose a valid option:")

    def ask_for_player_bet(self, given_card):
        self.logger.info(f"Your Card is {given_card}.")
        return self.handle_player_bet_prompt()

    def handle_player_bet_prompt(self):
        self.logger.info("What Should your respond to the dealer?")
        user_input = self.handle_user_bet_input()
        if self.is_terminated:
            self.handle_game_termination()
        return self.build_player_bet_msg(user_input)

    def handle_user_bet_input(self):
        while True:

            self.logger.info("# B-Bet # T-Terminate # ")
            user_input = input()

            if self.validate_input(user_input, "B"):
                return self.handle_user_bet_amount()

            elif self.validate_input(user_input, "T"):
                self.is_terminated = True
                return "T"

            else:
                self.logger.info("Please choose a valid option:")

    def handle_user_bet_amount(self):
        self.logger.info("Please insert your bet amount:")
        while True:
            user_input = input()
            try:
                user_input_value = int(user_input)
                return user_input_value
            except ValueError:
                self.logger.warning("This amount is not valid, try again:")

    def validate_input(self, input: str, correnct_input):
        return bool(input.capitalize() == correnct_input or input.lower() == correnct_input)

    def is_tie(self, msg):
        return msg.get('tie')

    def build_player_bet_msg(self, player_bet):
        return {"player_bet": str(player_bet)}

    def build_player_tie_msg(self, is_tie):
        return {"tie_decision": is_tie}

    def parse_dealer_bet_request(self, msg):
        card = msg["player_card"]
        return self.build_card(card)

    def build_card(self, card):
        return Card(card[:-1], card[-1:])

    def handle_game_termination(self):
        self.send_msg_to_dealer({"terminate": True})
        msg = self.await_response_from_dealer()
        self.prompt_termination_msg(msg)
        exit(1)

    def prompt_termination_msg(self, msg):
        self.logger.info(f"The dealer has ended your game.")
        self.logger.info(f"We have ended our match on round {msg['round']} with earnings of {msg['player_earnings']}")

    def await_response_from_dealer(self):
        return self.receive()

    def send_msg_to_dealer(self, msg):
        self.transmit(msg)

    def is_game_terminated(self, msg):
        return msg.get("termination")

    def build_init_msg(self):
        return {"init_game": True}