import random
import os
from Tree.Tree import Tree
import numpy as np

def update(tree):
    for node in tree.nodes.values():
        node.data.all_probabilities = np.array(node.data.all_probabilities)
    return tree

os.chdir("..")
os.chdir("Simulator_main")
T = Tree()
T.to_object("model_string_short")


