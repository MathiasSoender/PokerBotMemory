import time

from Poker.Card import Card
from Poker.ranking.high_cards import HighCard, HighCard_jit
from Cython_pack import highcards, hand_rankings
from Poker.ranking.hand_ranking import find_rank_jit, rank_hand

import numpy as np

def HighCards():
    h = [Card(8,"s"), Card(13,"d")]
    com = [Card(6,"c"), Card(9,"c"), Card(14,"d"), Card(6,"c"), Card(13, "s")]
    hh = np.array([8, 13, 6, 9, 14, 6, 13])
    cc = ["s", "d", "c", "c", "d", "c", "s"]
    cc = np.array([ord(x) for x in cc])

    t1 = time.time()
    for _ in range(0, 1):
        (HighCard(1, h, com))
    print("normal: " + str(time.time() - t1))

    t1 = time.time()
    for i in range(0, 1):
        if i == 0:
            (HighCard_jit(1, hh, cc))
            t1 = time.time()
            continue
        HighCard_jit(5, hh, cc)
    print("jit: " + str(time.time() - t1))



    t1 = time.time()
    for _ in range(0, 1):
        (highcards.HighCard(1, h, com))
    print("cython: " + str(time.time() - t1))

def Rank():
    h = [Card(14, "s"), Card(13, "s")]
    com = [Card(3, "d"), Card(4, "h"), Card(5, "c"), Card(11, "s"), Card(11, "d")]
    hh = np.array([6, 2, 3, 4, 5, 11, 11])
    cc = ["s", "s", "d", "h", "c", "s", "d"]
    cc = np.array([ord(x) for x in cc])

    t1 = time.time()
    for _ in range(0, 100000):
        a = rank_hand(h, com)
        a.find_rank_initial()
    print("normal: " + str(time.time() - t1))


    t1 = time.time()
    for i in range(0, 100000):
        if i == 0:
            (find_rank_jit(hh, cc))
            t1 = time.time()
            continue
        find_rank_jit(hh, cc)
    print("jit: " + str(time.time() - t1))

    t1 = time.time()
    for _ in range(0, 100000):
        b = hand_rankings.rank_hand(h, com)
        b.find_rank_initial()
    print("cython: " + str(time.time() - t1))

HighCards()
