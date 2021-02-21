"""
For Real bot:
Idea: Take some node, with "N" below threshold. Create a subtree at this node.
Run multiple simulations at the rooted subtree. Return correct action, kill subtree.
 - Why kill?: When simulating locally, it is only the current hand which is reflected.
 - Would mess up the real game-tree.
"""
import time

from Controllers.Game_controller import game_controller
from Poker.Deck import Deck


class local_simulator:

    def __init__(self, node, controller, players, current_player, deck):
        self.original_node = node
        self.sub_tree = node.subtree()
        self.original_controller = controller
        self.original_players = players
        self.original_player = current_player
        self.original_deck = deck



    @staticmethod
    def local_sim_needed(node):
        if sum(node.data.N.values()) < node.data.threshold:
            return True
        return False

    def start_sim(self, time_threshold = 5):
        t1 = time.time()
        while local_simulator.local_sim_needed(self.original_node) and time.time() - t1 < time_threshold:
            self.original_node = self.sub_tree.root
            current_player = self.start_player
            current_node = self.sub_tree.root.root





