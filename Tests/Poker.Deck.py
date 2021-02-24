from Poker.Card import Card
from Poker.Deck import Deck
from Range.Range import Range

d = Deck()

d.draw()
d.draw()
print(len(d.deck))
d.remove_card(Card(2, "s"))
print(len(d.deck))

