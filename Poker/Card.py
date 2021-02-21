from Human_vs_bot.Display import Display

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
        if self.suit == other_card.suit and self.value == other_card.value:
            return True
        return False


    def __str__(self):
        return str(self.value) + str(self.suit)
