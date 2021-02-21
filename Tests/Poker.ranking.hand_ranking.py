from Poker.ranking.hand_ranking import rank_hand
from Poker.Card import Card
from Cython_pack import hand_rankings
import time

h = [Card(14,"s"), Card(2,"s")]
com = [Card(3,"d"), Card(4,"h"), Card(5,"c"), Card(11,"s")]

t1 = time.time()
for _ in range(0,10000):
    a = rank_hand(h, com)
    a.find_rank_initial()
print(time.time() - t1)

t1 = time.time()
for _ in range(0,10000):
    b = hand_rankings.rank_hand(h, com)
    b.find_rank_initial()
print(time.time() - t1)
