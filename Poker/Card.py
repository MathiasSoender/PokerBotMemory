class Card:
    def __init__(self, value, suit):
        if isinstance(suit, str):
            self.suit = suit
        else:
            raise TypeError("Suit is not string...")
        if isinstance(value, int):
            self.value = value
        else:
            raise TypeError("Value is not int...")

    def equals(self, other_card):
        return self.__eq__(other_card)

    def __members(self):
        return self.value, self.suit

    def __eq__(self, other):
        return self.__members() == other.__members()

    def __str__(self):
        return str(self.value) + str(self.suit)

    def __hash__(self):
        return hash(self.__members())
