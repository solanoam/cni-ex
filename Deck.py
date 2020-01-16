import random
from Card import CardRanks, CardTypes, Card


class Deck:

    def __init__(self, logger):
        self.logger = logger
        self.cards = self.create_deck()
        self.index = 51
        self.shuffle_deck()

    def __len__(self):
        return self.index + 1

    def create_deck(self):
        cards = []
        for rank in CardRanks:
            for card_type in CardTypes:
                cards.append(Card(rank.value, card_type.value))
        self.logger.info("deck was created")
        return cards

    def shuffle_deck(self):
        random.shuffle(self.cards)
        self.logger.info("deck was shuffled")

    def draw_card(self):
        if self.index >= 0:
            self.index -= 1
            return self.cards[self.index + 1]
        else:
            raise AttributeError("The Deck is out of cards!")

    def destroy_deck(self):
        self.index = -1
