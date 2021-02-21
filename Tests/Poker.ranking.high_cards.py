from Poker.ranking.high_cards import HighCard
from Poker.Card import Card
import time
from Cython_pack import highcards
# Does not work correctly with straights...

h = [Card(7,"s"), Card(2,"s")]
com = [Card(4,"s"), Card(5,"s"), Card(3,"c"), Card(6,"d"), Card(12, "d")]


print(highcards.HighCard(5, h, com))
