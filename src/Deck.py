"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
"""

import random
from src.Card import CardRanks, CardTypes, Card

class Deck:
    """
    class for managing a deck of cards
    """
    def __init__(self, logger):
        """
        constructor
        :param logger:
        """
        self.logger = logger
        self.cards = self.create_deck()
        self.index = 51
        self.shuffle_deck()

    def __len__(self):
        """
        get the length of the remaining deck of cards
        :return:
        """
        return self.index + 1

    def create_deck(self):
        """
        create the initial deck
        :return:
        """
        cards = []
        for rank in CardRanks:
            for card_type in CardTypes:
                cards.append(Card(rank.value, card_type.value))
        self.logger.debug("deck was created")
        return cards

    def shuffle_deck(self):
        """
        shuffle the created deck
        :return:
        """
        random.shuffle(self.cards)
        self.logger.debug("deck was shuffled")

    def draw_card(self):
        """
        get a card back and reduce the size of the deck
        :return: Card
        """
        if self.index >= 0:
            self.index -= 1
            return self.cards[self.index + 1]
        else:
            raise AttributeError("The Deck is out of cards!")

    def destroy_deck(self):
        """
        finish the deck
        :return:
        """
        self.index = -1
