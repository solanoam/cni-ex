from enum import Enum


class CardTypes(Enum):
    Clubs = 'C'
    Diamonds = 'D'
    Hearts = 'H'
    Spades = 'S'


class CardRanks(Enum):
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
    J = 11
    Q = 12
    K = 13
    A = 14

class Card:
    def __init__(self, rank, card_type):
        self.rank = rank
        self.type = card_type
        self.rank_num_value = self.transform_rank_to_num_value(self.rank)

    def __str__(self):
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
        return CardRanksValues[value].value if value in list(map(lambda v: v.name, CardRanksValues)) else value
