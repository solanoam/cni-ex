from enum import Enum


class CardTypes(Enum):
    Clubs = 'C'
    Diamonds = 'D'
    Hearts = 'H'
    Spades = 'S'


class CardRanks(Enum):
    One = 1
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


class Card:
    def __init__(self, rank, card_type):
        self.rank = rank
        self.type = card_type

    def __str__(self):
        return f"{self.rank}{self.type}"

    def _is_valid_operand(self, operand):
        return isinstance(operand, Card)

    def __eq__(self, other):
        if self._is_valid_operand(other): raise NotImplemented
        return self.rank == other.rank

    def __gt__(self, other):
        if self._is_valid_operand(other): raise NotImplemented
        return self.rank > other.rank

    def __ge__(self, other):
        if self._is_valid_operand(other): raise NotImplemented
        return self.rank >= other.rank

    def __lt__(self, other):
        if self._is_valid_operand(other): raise NotImplemented
        return self.rank < other.rank

    def __le__(self, other):
        if self._is_valid_operand(other): raise NotImplemented
        return self.rank <= other.rank
