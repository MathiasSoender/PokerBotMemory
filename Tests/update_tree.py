import random
import os
from Tree.Tree import Tree
from Tree.data import Data

def update(tree):
    """
    On the fly updates to a tree
    :param tree:
    """
    for n in tree.nodes.values():
        if n.data.threshold == 250:
            n.data.threshold = 150

            for r in n.data.rewards.values():
                while len(r) >= n.data.threshold:
                    r.popleft()

            while len(n.data.all_probabilities) > n.data.threshold:
                n.data.all_probabilities.pop(random.randrange(len(n.data.all_probabilities)))

            print("one")
    tree.to_object("model_updated")

os.chdir("..")
os.chdir("Simulator_main")
T = Tree()
update(T)


