from Tree.node import Node
from Tree.Identifier import Identifier
from Tree.data2 import Data
import pickle
import gc
import os
import shutil



class Tree:
    def __init__(self, new_tree=False, path="model", root=None):

        self.nodes = {}
        self.root = root
        self.rounds_trained = 0
        self.child_map = {}


        # For multi-processing. Is reset for each new train session.

        if not new_tree:
            self.get_object(path)
        else:
            if root is None:
                ID = Identifier()
                ID.create_name(is_root=True)
                self.add_node(ID, data=Data(), is_root=True)


    def add_node(self, ID, data=None, is_root=False, parent=None):
        if is_root:
            new_node = Node(ID, data)
            ID.create_name()
            self.root = new_node
            self.nodes[ID.name] = new_node

        else:
            if parent is None:
                raise ValueError("Parent must be given")
            else:
                new_node = Node(ID, data, parent)
                self.nodes[ID.name] = new_node
                self.nodes[parent.identifier.name].add_child(new_node)

                if self.child_map.get(parent.identifier.name) is None:
                    children = set()
                else:
                    children = self.child_map[parent.identifier.name]

                children.add(new_node.identifier.name)
                self.child_map[parent.identifier.name] = children

    def print(self):

        for item in self.nodes.values():
            print(item.__str__())

    """ Expand tree with new nodes if possible """
    def expand_tree(self, current_player, all_players, current_node, controller):

        if current_node.is_leaf() and current_player.chips > 0:

            all_players.update_remaining()
            pot = all_players.pot_size()
            bet1 = True
            bet2 = True
            call = False
            check = False
            allIn = True
            current_bet = all_players.find_max_bet_player().bet

            # A % pot size bet is:
            # a: Find opponenets bet size.
            # b: Calculate the pot now (pot + opponenets bet x 2)

            # Raise: a + (% * b)
            # So basically, calculate pot after figuring out biggest raise.
            # Multiply pot with %, and add biggest raise.
            if ((pot + current_bet) * 0.4 + current_bet) - current_player.bet > current_player.chips:
                bet1 = False
            if ((pot + current_bet) * 0.8 + current_bet) - current_player.bet > current_player.chips:
                bet2 = False


            # Calls must also be available preflop, since blinds have been posted...
            if current_node.identifier.call_available(controller.new_street, controller.preflop,
                                                      name=current_player.name):
                call = True
                fold = True
            else:
                fold = False
                check = True

            if current_player.chips == 0:
                allIn = False
                call = False
                fold = False
                check = False

            elif current_node.identifier.allIn_occured():
                allIn = False

            actions = [(fold, "f"), (call, "ca"), (check, "ch"),
                       (bet1, "b1"), (bet2, "b2"), (allIn, "AL")]

            for action, string in actions:
                if action:
                    # Copies parent identifier
                    iden = Identifier(current_node.identifier)
                    # Checks if new street has arrived
                    iden.update_new_street(controller.new_street)
                    # Update with new action
                    iden.update_street_list((current_player.name, string))
                    iden.create_name()
                    if string == "fold":
                        self.add_node(iden, data=Data(pre_flop=controller.preflop, fold_node=True), parent=current_node)
                    else:
                        self.add_node(iden, data=Data(pre_flop=controller.preflop), parent=current_node)

        controller.new_street = [False, ""]


    """Saves the tree in different files. Useful as pickle has high memory overhead (5x)"""
    def to_object(self, path):
        print("saving tree")
        gc.disable()
        if path not in os.listdir():
            os.makedirs(path)
        else:
            shutil.rmtree(path)
            os.makedirs(path)

        os.chdir(path)
        if "etc" not in os.listdir():
            os.makedirs("etc")
        if "nodes" not in os.listdir():
            os.makedirs("nodes")

        # Dump etc
        os.chdir("etc")
        pickle.dump(self.child_map, open("child_map", "wb"), protocol=4)
        pickle.dump(self.rounds_trained, open("rounds_trained", "wb"), protocol=4)

        self.child_map = None

        os.chdir("..")
        os.chdir("nodes")

        # Dump nodes, remember to cut children.
        idx = 0
        dump_list = [self.root]
        for node in self.nodes.values():
            if ((idx+1) % 50000) == 0:

                pickle.dump(dump_list, open("nodes" + str(idx), "wb"), protocol=4)

                dump_list = []

            node.children = None
            dump_list.append(node)
            idx += 1
        pickle.dump(dump_list, open("nodes" + str(idx), "wb"), protocol=4)

        os.chdir("..")
        os.chdir("..")
        gc.enable()

    """Gets the tree from different files - rebuilds it. Useful as pickle has high memory overhead (5x)"""
    def get_object(self, path):
        os.chdir(path)
        os.chdir("etc")
        gc.disable()
        child_map = pickle.load(open("child_map", "rb"))
        self.child_map = child_map
        child_map = None

        rounds_trained = pickle.load(open("rounds_trained", "rb"))
        self.rounds_trained = rounds_trained
        rounds_trained = None

        os.chdir("..")
        os.chdir("nodes")

        all_nodes = {}
        for node_pack in os.listdir():
            nodes_list = pickle.load(open(node_pack, "rb"))
            nodes_dict = {}

            for node in nodes_list:
                node.children = set()
                nodes_dict[node.identifier.name] = node

            all_nodes = {**all_nodes, **nodes_dict}
            nodes_list = None
            nodes_dict = None

        self.nodes = all_nodes
        all_nodes = None

        self.root = self.nodes["root"]

        for node in self.nodes.values():
            children_names = self.child_map.get(node.identifier.name)
            # Leaves have no children..
            if children_names is not None:
                for c in children_names:
                    node.children.add(self.nodes[c])

        os.chdir("..")
        os.chdir("..")
        gc.enable()


