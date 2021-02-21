from Poker.Deck import Deck
from Range.Range import Range

d = Deck()
R = Range()
for i in range(0, len(R.range)):
    for j in range(0, len(R.range)):
        hand = d.draw_from_range(0, R.range, i, j)
        print(hand[0], hand[1])
