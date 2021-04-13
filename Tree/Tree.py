import random
import copy
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


        # For multi-processing. Is reset for each new train session.

        if not new_tree:
            self.get_object(path)
        else:
            if root is None:
                ID = Identifier()
                ID.create_name(is_root=True)
                # Make 1000, so that bet2 is always created.
                D = Data()
                D.N[0] = 1000
                self.add_node(ID, data=D, is_root=True)


    def add_node(self, ID, data=None, is_root=False, parent=None):
        if is_root:
            new_node = Node(ID, data)
            ID.create_name()
            self.root = new_node
            self.nodes[ID.name] = new_node

        else:
            new_node = Node(ID, data)
            self.nodes[ID.name] = new_node
            self.nodes[parent.identifier.name].add_child(new_node)


    def print(self):

        for item in self.nodes.values():
            print(item.__str__())

    """ Expand tree with new nodes if possible """
    def expand_tree(self, current_player, all_players, current_node, controller):


        if current_node.is_leaf() and current_player.chips > 0:

            all_players.update_remaining()
            pot = all_players.pot_size()
            bet = True
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
            if ((pot + current_bet) * 0.5 + current_bet) - current_player.bet > current_player.chips:
                bet = False

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
                       (bet, "b1"), (allIn, "AL")]

            if bet:
                current_node.maximumBet = "b1"

            for action, string in actions:
                if action:
                    # Copies parent identifier
                    iden = Identifier(current_node.identifier)
                    # Checks if new street has arrived
                    iden.update_new_street(controller.new_street)
                    # Update with new action
                    iden.update_street_list((current_player.name, string))
                    iden.create_name()
                    if string == "f":
                        self.add_node(iden, data=Data(fold_node=True), parent=current_node)
                    else:
                        self.add_node(iden, data=Data(), parent=current_node)


        if current_player.chips > 0 and sum(current_node.data.N) > 250 and current_node.maximumBet == "b1":

            all_players.update_remaining()
            pot = all_players.pot_size()
            current_bet = all_players.find_max_bet_player().bet
            bet2 = True
            if ((pot + current_bet) * 0.8 + current_bet) - current_player.bet > current_player.chips:
                bet2 = False

            if bet2:
                b1Child = None
                for c in current_node.children:
                    if c.identifier.is_action("b1"):
                        b1Child = c

                current_node.maximumBet = "b2"
                iden = Identifier(current_node.identifier)
                iden.update_new_street(controller.new_street)
                iden.update_street_list((current_player.name, "b2"))
                iden.create_name()
                self.add_node(iden, data=copy.deepcopy(b1Child.data), parent=current_node)


        controller.new_street = [False, ""]


    """Saves the tree in different files. Useful as pickle has high memory overhead (5x)"""
    def to_object(self, path):
        print("saving tree")
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
        child_map = {}
        for node in self.nodes.values():
            if len(node.children) > 0:
                child_list = []
                for child in node.children:
                    child_list.append(child.identifier.name)
                child_map[node.identifier.name] = child_list

            node.children = None

        pickle.dump(child_map, open("child_map", "wb"), protocol=4)
        pickle.dump(self.rounds_trained, open("rounds_trained", "wb"), protocol=4)

        del child_map

        os.chdir("..")
        os.chdir("nodes")

        # Dump nodes, remember to cut children.
        idx = 0
        self.root.children = None

        dump_list = []
        n_k = list(self.nodes.keys())
        random.shuffle(n_k)

        for i in range(0, len(n_k)):
            if ((idx+1) % 100000) == 0:

                pickle.dump(dump_list, open("nodes" + str(idx), "wb"), protocol=4)

                dump_list = []

            self.nodes[n_k[i]].children = None
            dump_list.append(self.nodes[n_k[i]])
            self.nodes[n_k[i]] = None
            n_k[i] = None

            idx += 1
        pickle.dump(dump_list, open("nodes" + str(idx), "wb"), protocol=4)

        os.chdir("..")
        os.chdir("..")

    """Gets the tree from different files - rebuilds it. Useful as pickle has high memory overhead (5x)"""
    def get_object(self, path):
        os.chdir(path)
        os.chdir("etc")
        child_map = pickle.load(open("child_map", "rb"))

        rounds_trained = pickle.load(open("rounds_trained", "rb"))
        self.rounds_trained = rounds_trained
        del rounds_trained

        os.chdir("..")
        os.chdir("nodes")

        all_nodes = {}
        for node_pack in os.listdir():
            nodes_list = pickle.load(open(node_pack, "rb"))

            for node in nodes_list:
                node.children = []
                all_nodes[node.identifier.name] = node

            del nodes_list

        self.nodes = all_nodes
        del all_nodes

        self.root = self.nodes["root"]
        for node in self.nodes.values():
            children_names = child_map.get(node.identifier.name)
            # Leaves have no children..
            if children_names is not None:
                for c in children_names:
                    node.children.append(self.nodes[c])

        os.chdir("..")
        os.chdir("..")
        del child_map


