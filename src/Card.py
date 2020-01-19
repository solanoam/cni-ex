"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
"""

from enum import Enum

class CardTypes(Enum):
    """
    enum for card types
    """
    Clubs = 'C'
    Diamonds = 'D'
    Hearts = 'H'
    Spades = 'S'


class CardRanks(Enum):
    """
    enum for card ranks
    """
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 'J'
    Queen = 'Q'
    King = 'K'
    Ace = 'A'

class CardRanksValues(Enum):
    """
    numeric values enum for letter based ranks
    """
    J = 11
    Q = 12
    K = 13
    A = 14

class Card:
    """
    a class for managing a poker based card
    """
    def __init__(self, rank, card_type):
        """
        constructor for card
        :param rank:
        :param card_type:
        """
        self.rank = rank
        self.type = card_type
        self.rank_num_value = self.transform_rank_to_num_value(self.rank)

    def __str__(self):
        """
        string representation
        :return:
        """
        return f"{self.rank}{self.type}"

    def _is_valid_operand(self, operand):
        return isinstance(operand, Card)

    def __eq__(self, other):
        if not self._is_valid_operand(other): raise NotImplemented
        return self.rank_num_value == other.rank_num_value

    def __gt__(self, other):
        if not self._is_valid_operand(other): raise NotImplemented
        return self.rank_num_value > other.rank_num_value

    def __ge__(self, other):
        if not self._is_valid_operand(other): raise NotImplemented
        return self.rank_num_value >= other.rank_num_value

    def __lt__(self, other):
        if not self._is_valid_operand(other): raise NotImplemented
        return self.rank_num_value < other.rank_num_value

    def __le__(self, other):
        if not self._is_valid_operand(other): raise NotImplemented
        return self.rank_num_value <= other.rank_num_value

    def transform_rank_to_num_value(self, value):
        """
        transforming the card letter to a value for comparision reasons
        :param value:
        :return:
        """
        return CardRanksValues[value].value if value in list(map(lambda v: v.name, CardRanksValues)) else value
