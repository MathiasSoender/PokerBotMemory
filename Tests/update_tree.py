import random
import os
from Tree.Tree import Tree
from Tree.data import Data

def update(tree):
    """
    On the fly updates to a tree
    :param tree:
    """
    K = 0
    for n in tree.nodes.values():
        if n.data.threshold == 500:
            n.data.threshold = 350

            for r in n.data.rewards.values():
                while len(r) >= n.data.threshold:
                    r.popleft()

            while len(n.data.all_probabilities) > n.data.threshold:
                n.data.all_probabilities.pop(random.randrange(len(n.data.all_probabilities)))
        K += 1
        if (K % 10000) == 0:
            print("10k done")
    tree.to_object("model_updated")


def kill_cumlative(tree):
    for n in tree.nodes.values():
        if hasattr(n, 'cum_rewards'):
            n.cum_rewards = None
            del n.cum_rewards

def change_strings(tree):
    replaces = [("bet1", "b1"), ("bet2", "b2"), ("fold", "f"), ("allIn", "AL"), ("call", "ca"),
                ("check", "ch")]
    r = 0
    for n in tree.nodes.values():

        for old, new in replaces:

            for i in range(0, len(n.identifier.preflop)):
                n.identifier.preflop[i] = (n.identifier.preflop[i][0], n.identifier.preflop[i][1].replace(old, new))

            for i in range(0, len(n.identifier.flop)):
                n.identifier.flop[i] = (n.identifier.flop[i][0], n.identifier.flop[i][1].replace(old, new))

            for i in range(0, len(n.identifier.turn)):
                n.identifier.turn[i] = (n.identifier.turn[i][0], n.identifier.turn[i][1].replace(old, new))

            for i in range(0, len(n.identifier.river)):
                n.identifier.river[i] = (n.identifier.river[i][0], n.identifier.river[i][1].replace(old, new))

        r += 1
        if (r % 10000) == 0:
            print("10000 rounds done")

        if n.identifier.name != "root":
            n.identifier.name = ""
            n.identifier.create_name()


os.chdir("..")
os.chdir("Simulator_main")
T = Tree()
change_strings(T)
T.to_object("model_string_short")


