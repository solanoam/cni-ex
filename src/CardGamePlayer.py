"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
repo - https://github.com/solanoam/cni-ex
"""

from src.Host import Host
from src.Card import Card


class CardGamePlayer(Host):
    """
    class that manages a client session for playing a war card game against the server. handles printing to the screen
    via logger and holds logic for responses to the server
    """
    def __init__(self, logger, **kwargs):
        """
        constructor
        :param logger: logger
        :param kwargs: inherited init params
        """
        super().__init__(logger, **kwargs)
        self.init_socket()
        self.player_bet = 0
        self.player_card = None
        self.dealer_card = None
        self.is_terminated = False

    def init_game(self):
        """
        initialize a game
        :return:
        """
        msg = self.build_init_msg()
        self.send_msg_to_dealer(msg)
        self.play_game()

    def play_game(self):
        """
        wrapper for playing the card game
        :return:
        """
        while not self.is_terminated:
            self.handle_game_turn()

    def handle_game_turn(self):
        """
        handle a turn within the card game
        """
        self.handle_player_turn()
        dealer_msg = self.await_response_from_dealer()
        if self.is_tie(dealer_msg):
            return self.handle_tie(dealer_msg)
        self.prompt_round_outcome(dealer_msg)

    def prompt_round_outcome(self, msg):
        """
        prompt to the screen the outcome of a round
        :param msg: server message
        """
        self.logger.info(f"the outcome for this round: {msg['round']}")
        self.logger.info(f"winner is {msg['winner']} with a bet of {msg['bet']} { '(original bet was ' + str(int(msg['original_bet'])) + ')' if msg.get('original_bet') else ''}, player card - {msg['player_card']}, dealer card - {msg['dealer_card']}:")

    def handle_player_turn(self):
        """
        handle a player turn and communication with the server
        :return:
        """
        msg = self.await_response_from_dealer()
        if self.is_game_terminated(msg):
            self.prompt_termination_msg(msg)
            exit(1)
        given_card = self.parse_dealer_bet_request(msg)
        player_msg = self.ask_for_player_bet(given_card)
        self.send_msg_to_dealer(player_msg)

    def handle_tie(self, dealer_tie_msg):
        """
        handle a tie event and communicate with the server
        :param dealer_tie_msg:
        """
        user_input = self.handle_tie_prompt(dealer_tie_msg)
        tie_msg = self.build_player_tie_msg(user_input)
        self.send_msg_to_dealer(tie_msg)
        if not user_input:
            self.logger.info(f"not going to war and moving to the next round")
        msg = self.await_response_from_dealer()
        return self.prompt_round_outcome(msg)

    def handle_tie_prompt(self, dealer_tie_msg):
        """
        handle the tie prompt to the screen and manages inputs from the user
        :param dealer_tie_msg: server message
        """
        self.logger.info(f"its a tie. Dealer Card: {dealer_tie_msg['dealer_card']}, Player Card: {dealer_tie_msg['player_card']}")
        self.logger.info("Do you wish to go to war?")
        user_input = self.handle_tie_input()
        return user_input

    def handle_tie_input(self):
        """
        handle receiving the tie input from the user
        :return:
        """
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
        """
        manages receiving player bet
        :param given_card: card given by the server
        """
        self.logger.info(f"Your Card is {given_card}.")
        return self.handle_player_bet_prompt()

    def handle_player_bet_prompt(self):
        """
        handle printing the instruction regarding the bet itself
        :return:
        """
        self.logger.info("What Should your respond to the dealer?")
        user_input = self.handle_user_bet_input()
        if self.is_terminated:
            self.handle_game_termination()
        return self.build_player_bet_msg(user_input)

    def handle_user_bet_input(self):
        """
        handle getting the user input regarding the bet
        """
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
        """
        handle getting the user input regarding the bet value
        """
        self.logger.info("Please insert your bet amount:")
        while True:
            user_input = input()
            try:
                user_input_value = int(user_input)
                return user_input_value
            except ValueError:
                self.logger.warning("This amount is not valid, try again:")

    def validate_input(self, input: str, correct_input):
        """
        validate a correct input
        :param input: given input
        :param correct_input: correct input
        :return: boolean
        """
        return bool(input.capitalize() == correct_input or input.lower() == correct_input)

    def is_tie(self, msg):
        """
        parse the server response for tie
        :param msg: server message
        :return: boolean
        """
        return msg.get('tie')

    def build_player_bet_msg(self, player_bet):
        """
        build a response for the player bet
        :param player_bet: bet
        :return: message response
        """
        return {"player_bet": str(player_bet)}

    def build_player_tie_msg(self, is_tie):
        """
        build a response for tie
        :param is_tie:
        :return: message response
        """
        return {"tie_decision": is_tie}

    def parse_dealer_bet_request(self, msg):
        """
        parse the given card by the server message
        :param msg: server message
        :return:
        """
        card = msg["player_card"]
        return self.build_card(card)

    def build_card(self, card):
        """
        create a card form a string
        :param card: string of a card
        :return:
        """
        return Card(card[:-1], card[-1:])

    def handle_game_termination(self):
        """
        handle game termination response from the server
        """
        self.send_msg_to_dealer({"terminate": True})
        msg = self.await_response_from_dealer()
        self.prompt_termination_msg(msg)
        exit(1)

    def prompt_termination_msg(self, msg):
        """
        promts messages to the client screen regarding game termination
        :param msg:
        """
        self.logger.info(f"The dealer has ended your game.")
        self.logger.info(f"We have ended our match on round {msg['round']} with earnings of {msg['player_earnings']}")

    def await_response_from_dealer(self):
        """
        await server response and return the message
        :return: server response dictionary
        """
        return self.receive()

    def send_msg_to_dealer(self, msg):
        """
        send a dictionary based message to the server
        :param msg: message to be sent
        """
        self.transmit(msg)

    def is_game_terminated(self, msg):
        """
        check if the game is terminated by parsing the server response
        :param msg: server response
        :return: boolean
        """
        return msg.get("termination")

    def build_init_msg(self):
        """
        build the initial response for a new game
        :return: message
        """
        return {"init_game": True}