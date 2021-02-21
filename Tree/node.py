from Tree.data import Data
import math
import random
from Tree.Identifier import Identifier
import copy

class Node:
    def __init__(self, identifier: Identifier, data: Data, parent=None):
        self.children = set()
        self.identifier = identifier
        self.data = data
        self.parent = parent


    """ Finds a rooted subtree of node """
    def subtree(self):
        from Tree.Tree import Tree

        new_root = copy.copy(self)
        new_root.parent = None

        T = Tree(new_tree=True, root = new_root)
        child_list = [new_root]

        for c in new_root.children:
            c.parent = new_root

        while len(child_list) > 0:
            node = child_list.pop()
            for c in node.children:
                child_list.append(c)
            T.nodes[node.identifier.name] = node

        return T

    def find_distribution(self, win_probability):
        # Softmax
        softmax_sum = 0
        softmax_distribution = []

        for child in self.children:
            child_split = child.data.find_split(win_probability)
            softmax_sum += math.exp(sum(child.data.rewards[child_split]) / child.data.threshold)

        for child in self.children:
            child_split = child.data.find_split(win_probability)
            softmax_distribution.append((child,
                                         math.exp(sum(child.data.rewards[child_split]) / child.data.threshold) /
                                         softmax_sum))

        return softmax_distribution


    def siblings(self):
        if self.parent is not None:
            siblings = []
            for sibling in self.parent.children:
                if sibling.identifier.name != self.identifier.name:
                    siblings.append(sibling)
            return siblings
        return None


    def select_child(self, win_probability, greedy = True, LOG = None, prob = 25):
        # Zips the distribution into: Children, distribution values
        dis = self.find_distribution(win_probability)
        Children, distribution = zip(*dis)

        # Some probability of being epsilon-greedy:
        if greedy and random.randint(0, prob) == 1:
            child = random.choice(Children)

            if LOG is not None:
                LOG.log("E-greedy child selection")

            return child, 1/len(Children)

        # Otherwise use the soft-max distribution
        if LOG is not None:
            LOG.children_log(dis)
        child = random.choices(population=Children, weights=distribution, k=1)[0]

        return child, distribution[Children.index(child)]

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def add_child(self, new_node):
        self.children.add(new_node)

    def depth(self):
        depth = 1
        current_parent = self.parent
        while current_parent is not None:
            current_parent = current_parent.parent
            depth += 1
        return depth

    def local_node(self):
        children = set()
        for c in self.children:
            children.add(copy.copy(c))

        new_node = copy.copy(self)
        new_node.parent = None
        new_node.children = children
        for c in new_node.children:
            c.children = set()
            c.parent = None

        return new_node


    def __str__(self):
        return str((self.identifier.name, self.data.__str__()))