from Tree.data import Data
import numpy
from scipy.stats import truncnorm
import time
import random
def thresh_hold_test():
    Many = {1:0, 2:0, 3:0, 4:0, 5:0}
    many2 = {1:0, 2:0, 3:0, 4:0, 5:0}
    r = 1
    for _ in range(0, r):
        d = Data(pre_flop=True)
        d.threshold = 10000

        probs = []
        for _ in range(0, 1000):
            probs.append(random.randint(0,100)/100)

        for prob in probs:
            d.update(prob,1,1)

        for key in d.split_probabilities.keys():
            Many[key] += d.split_probabilities[key]

    for val in Many.values():
        val /= r

    for _ in range(0, r):
        d = Data(pre_flop=True)
        d.threshold = 250

        probs = []
        for _ in range(0, 1000):
            probs.append(random.randint(0,100)/100)

        for prob in probs:
            d.update(prob,1,1)

        for key in d.split_probabilities.keys():
            many2[key] += d.split_probabilities[key]

    for val in many2.values():
        val /= r
    print(d)


def fold_node_test():
    d = Data(pre_flop=True, fold_node=True)
    for _ in range(0, 10):
        r = random.randint(0, 100) / 100
        d.update(r, 1, -1)

    print(d.split_probabilities)
    print(d.all_probabilities)
    print(d.rewards)
    print(d)



thresh_hold_test()

