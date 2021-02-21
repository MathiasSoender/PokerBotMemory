from Tree.node import Node
from Tree.Tree import Tree
from Tree.data import Data
import time

T = Tree(path=r"C:\Users\Mathi\Desktop\cards7\Simulator_main\model")

for n in T.nodes.values():
    if len(n.children) > 5:
        print(n)
