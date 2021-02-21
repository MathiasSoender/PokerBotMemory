from Misc.Logger import loggerNonStatic
from Tree.node import Node
from Tree.Identifier import Identifier
from Tree.data import Data
import pickle
import gc
import os
from Controllers.Game_controller import game_controller
import time
import traceback
import sys

from subtree_trainer.Simulator import sim


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
                self.add_node(ID, data=Data(), is_root=True)

    def all_nodes(self):
        return self.nodes.values()

    def all_leaves(self):
        nodes = self.all_nodes()
        leaves = []
        for node in nodes:
            if node.is_leaf():
                leaves.append(node)
        return leaves

    def get_node(self, name):

        for node in self.nodes.values():
            if node.identifier.name == name:
                return node

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
                # self.get_node(parent.identifier.name).add_child(new_node)
                self.nodes[parent.identifier.name].add_child(new_node)
    def print(self):

        for item in self.nodes.values():
            print(item.__str__())

    """ Ensures that the tree is maximal. """

    def expand_tree(self, current_player, all_players, current_node, controller):
        # Actions are: b1, b2, allIn, call, fold, check

        if current_node.is_leaf() and current_player.chips > 0:

            all_players.update_remaining()
            pot = all_players.pot_size()
            bet1 = True
            bet2 = True
            bet3 = True
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
            if ((pot + current_bet) * 1 + current_bet) - current_player.bet > current_player.chips:
                bet3 = False

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

            actions = [(fold, "fold"), (call, "call"), (check, "check"),
                       (bet1, "bet1"), (bet2, "bet2"), (allIn, "allIn")]
            # (bet3, "bet3")

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

    def to_object(self, filename):
        gc.disable()
        with open(filename, 'wb') as Tree_file:
            pickle.dump(self, Tree_file, protocol=4)
        gc.enable()


    """overwrites the current Tree with a Tree object located in a file"""

    def get_object(self, filename):
        gc.disable()
        with open(filename, 'rb') as Tree_file:
            t = pickle.load(Tree_file)
        self.nodes = t.nodes
        self.root = t.root
        self.rounds_trained = t.rounds_trained
        gc.enable()


def tree_service(tree_Q, channels, new_tree, path, is_bot=False):
    try:
        os.chdir("..")
        if is_bot:
            os.chdir("..")
        os.chdir("Simulator_main")
        T = Tree(new_tree=new_tree, path=path)

        if is_bot:
            tree_Q.put(1)

        logger = loggerNonStatic("master")

        while True:
            res = tree_Q.get()

            if res.request == "process":
                current_node = T.nodes[res.current_node_name]
                if not res.is_bot:
                    T.expand_tree(res.current_player, res.all_players, current_node, res.controller)
                channels[res.ID].put(current_node.local_node())

            elif res.request == "root":
                T.rounds_trained += 1
                current_node = T.root
                if not res.is_bot:
                    T.expand_tree(res.current_player, res.all_players, current_node, res.controller)
                channels[res.ID].put(T.root.local_node())

            elif res.request == "backprop":
                nodes_for_update = []
                for iden, odds, player, pi in res.selected_nodes:
                    # Finds the correct node for update
                    node_ = T.nodes[iden.name]
                    nodes_for_update.append((node_, odds, player, pi))

                g_controller = game_controller()
                g_controller.selected_nodes = nodes_for_update
                logger.end_log(res.players, res.winner, res.community, res.pot)
                logger.nodes_log(g_controller.selected_nodes)

                g_controller.back_prop(res.pot, res.winner)

                logger.nodes_log(g_controller.selected_nodes, "After")


            elif res.request == "getSubtree":
                if res.current_node_name[-2:] in ["F:", "T:", "R:"]:
                    res.current_node_name = res.current_node_name[:-2]
                sub_tree = T.nodes[res.current_node_name].subtree()
                channels[res.ID].put(sub_tree)
                print("done fetching subtree")


            elif res.request == "updateSubtree":
                print("getting subtree")
                sub_tree = res.current_player
                print("Gotten subtree")
                for node in sub_tree.nodes.values():
                    print(node)
                    if node.identifier.name in T.nodes:
                        T.nodes[node.identifier.name].data = node.data
                    else:
                        T.add_node(node.identifier, node.data, parent=T.nodes[node.parent.identifier.name])



            elif res.request == "stop":
                break

            if ((T.rounds_trained + 1) % 150000 == 0) and is_bot is False:
                print("intermediate save of model")
                T.to_object("model"+str(T.rounds_trained))
                T.rounds_trained += 1

        T.to_object("model")
        print("Tree service shutdown")
        print("Len: " + str(len(T.nodes)))
        print("rounds trained: " + str(T.rounds_trained))
    except SystemExit:
        raise
    except:
        traceback.print_exc(file=sys.stdout)
