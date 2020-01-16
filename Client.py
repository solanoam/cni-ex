from Host import Host
from Deck import Deck
from Card import Card


class Client(Host):
    def __init__(self, logger, sock, **kwargs):
        super().__init__(self, logger, sock, **kwargs)
        self.player_bet = 0
        self.player_msg =''
        self.dealer_msg =''
        self.tie_decision ='' 
        self.player_card = None 

    
    def handle_player_game(self):
        self.player_msg=''            # enter your massage from logger ,fix syntex
        send_msg_to_dealer(self.player_msg)  # send msg to start convo
        dealer_msg = self.await_response_from_dealer()
        if self.is_start_game_failed(dealer_msg):
            return self.handle_game_deny_message()
        player_card=dealer_msg["player_card"]
        player_bet= # syntex to get bet from logger
        player_msg = self.build_player_bet_msg(self.player_bet)
        send_msg_to_dealer(player_msg)

        


    def is_start_game_failed(self, dealer_msg):
        return delaer_msg.get('game deny')
    
    def handle_game_deny_message(self):
        # check what to do when geting deny message 

    def build_player_bet_msg(self,player_bet):
        return {"player_bet": str(player_bet)}
    
    def await_response_from_dealer(self):
        return self.receive()

    def send_msg_to_dealer (self, msg):
        self.transmit(msg)

     


    
    
