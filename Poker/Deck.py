import random
from Poker.Card import Card

class Deck:
    def __init__(self):
        self.deck = []
        suits = ["s","d","h","c"]
        for i in range(2, 15):
            for suit in suits:
                self.deck.append(Card(i, suit))

    def remove_card(self, rm_card):
        for card in self.deck:
            if card.equals(rm_card):
                self.deck.remove(card)
                return True
        return False

    def draw(self, remove = True):
        card = random.choice(self.deck)
        if remove:
            self.remove_card(card)
        return card

    def draw_from_range(self, range_value, current_range, i, j, remove = False):
        # Skip range index below range value.
        if current_range[i][j] in range_value:
            j_cards = [x for x in self.deck if x.value == 14-j]
            i_cards = [x for x in self.deck if x.value == 14-i]

            # suited
            if j > i:
                valid_combinations = [(x, y) for (x, y) in zip(j_cards, i_cards)]

            # unsuited
            else:
                valid_combinations = []
                for j_card in j_cards:
                    for i_card in i_cards:
                        if j_card.suit != i_card.suit\
                           and (i_card, j_card) not in valid_combinations\
                           and (j_card, i_card) not in valid_combinations:

                            valid_combinations.append((i_card, j_card))

            # Any combination available?
            if valid_combinations:
                hand = random.choice(valid_combinations)
                if remove:
                    self.remove_card(hand[0])
                    self.remove_card(hand[1])
                return hand

    def __str__(self):
        return str(self.deck)







