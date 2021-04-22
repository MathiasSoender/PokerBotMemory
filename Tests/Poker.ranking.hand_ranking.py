from Poker.ranking.hand_ranking import rank_hand, find_rank_jit
from Poker.Card import Card
from Cython_pack import hand_rankings
import time
from Poker.ranking.high_cards import HighCard, HighCard_jit

import numpy as np

def toJitInputFindRank(hand, com):
    handandcom = np.array([0] * (len(com) + 2))
    suits = np.array([""] * (len(com) + 2))

    for i, c in enumerate(com):
        handandcom[i] = c.value
        suits[i] = c.suit


    handandcom[-2] = hand[0].value
    handandcom[-1] = hand[1].value
    suits[-2] = hand[0].suit
    suits[-1] = hand[1].suit

    cc = np.array([ord(x) for x in suits])

    return handandcom, cc






h = [Card(6,"s"), Card(7,"s")]
com = [Card(2,"s"), Card(3,"s"), Card(10,"s"), Card(4,"s"), Card(3,"s")]

com2, suits = toJitInputFindRank(h, com)



a = rank_hand(h, com)
a.find_rank_initial()
print("normal: " + str(a.rank))
print(HighCard(a.rank, h, com))

rJit = find_rank_jit(com2, suits)
print("jit: " + str(rJit))
print(HighCard_jit(rJit, com2, suits))

