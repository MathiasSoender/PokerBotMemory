import time

from Player.all_players import Players
from Player.player_types import BB, BTN, CO, MP, SB, UTG
from Misc.Simulator_package import tree_package, package
from subtree_trainer.Simulator import sim
import copy
import pickle

class game_controller:
    def __init__(self, tree_Q, own_Q, ID):
        self.preflop = True
        self.street = "preflop"
        self.community = []
        self.players = None
        self.hero = None
        self.tree_Q = tree_Q
        self.own_Q = own_Q
        self.ID = ID

    def start_game(self, deck, heroPos, hand):
        bb = BB.BB(None)
        sb = SB.SB(None)
        btn = BTN.BTN(None)
        co = CO.CO(None)
        mp = MP.MP(None)

        utg = UTG.UTG(None)
        self.players = Players(utg, bb, sb, mp, btn, co)

        self.hero = self.players.find_player(name=heroPos)
        self.hero.hero = True
        self.hero.hand = hand
        deck.remove_card(hand[0])
        deck.remove_card(hand[1])

        return self.hero

    def processActions(self, folded_info, bets_info, BB=0.02, current_player=None, current_node=None):

        if current_player is None:
            current_player = self.players.UTG
            print("updated")

        elif current_player.name == self.hero.name:
            current_player = self.find_next_player(current_player)

        if current_node is None:
            current_node = self.request_node(None, None, None, self.ID)
            print("requesting")
            current_node.identifier.name = "P:"

        while current_player.name != self.hero.name:
            # Check if player folded:
            folded = False
            actual_bet = 0
            print("stuck")

            for name, f_info in folded_info:
                if current_player.name == name and f_info:
                    # A simple hack - change the name (Tree Service only looks at name when fetching)
                    current_node.identifier.name += self.update_node_name(current_player.name, "f")
                    folded = True

            if not folded:
                current_bet = self.players.find_max_bet_player().bet
                for name, b_info in bets_info:
                    b_info /= BB

                    if current_player.name == name:
                        # check
                        if b_info == 0:
                            current_node.identifier.name += self.update_node_name(current_player.name, "ch")

                        # call
                        elif b_info == current_bet:
                            # Case if BB checks preflop (would think it was a call otherwise)
                            if current_player.name == "BB" and self.preflop and b_info == 1:
                                current_node.identifier.name += self.update_node_name(current_player.name, "ch")
                            else:
                                current_node.identifier.name += self.update_node_name(current_player.name, "ca")

                        # bets
                        else:
                            bet_action = self.find_bet_action(current_bet, b_info)
                            current_node.identifier.name += self.update_node_name(current_player.name, bet_action)
                            actual_bet = b_info

            current_node = self.request_node(current_node, None, None, self.ID)
            self.process_action_human(current_node, current_player, actual_bet)

            current_player = self.find_next_player(current_player)

        self.players.update_remaining()
        print(current_player)
        print(current_node)
        return current_node

    def process_action_human(self, current_node, player, actual_bet):
        if self.preflop:
            player.update_range_num(current_node)

        if current_node.identifier.is_action("f"):
            player.folded = True
            player.bet = 0

        elif current_node.identifier.is_action("AL"):
            player.chips = 0
            player.bet = 100
            self.players.set_done_actions(False)

        elif current_node.identifier.is_action("ca"):
            player.chips = self.players.find_max_bet_player().chips


        elif current_node.identifier.is_action("b1") or current_node.identifier.is_action("b2"):
            player.chips = max(player.chips - (actual_bet - player.bet), 0)
            player.bet = actual_bet
            self.players.set_done_actions(False)

        player.action_done = True

    def do_action_bot(self, current_node, player):
        # Before doing action, check if the node is minimal visited.

        if sum(current_node.data.N.values()) < 200 and current_node.identifier.name != "P:":
            self.tree_Q.put(tree_package(current_node.identifier.name, None, None, None, "getSubtree", self.ID, None))
            subTree = self.own_Q.get()
            start_time = time.time()
            last_two = current_node.identifier.name[-2:]

            while start_time + 5 > time.time():
                subTree = sim(subTree, copy.deepcopy(self.community), copy.deepcopy(self.players),
                              copy.deepcopy(self.street), copy.deepcopy(last_two))

            self.tree_Q.put(tree_package(current_node.identifier.name, subTree, None, None, "updateSubtree", self.ID, None))

            current_node = subTree.root
            print("size of subtree: " + str(len(subTree.nodes)))


        new_node, _ = current_node.select_child(player.win_odds, greedy=False)

        if self.preflop:
            player.update_range_num(new_node)

        if new_node.identifier.is_action("f"):
            player.folded = True
            player.bet = 0

        elif new_node.identifier.is_action("AL"):
            player.chips = 0
            player.bet = 100
            self.players.set_done_actions(False)

        elif new_node.identifier.is_action("ca"):
            player.chips = self.players.find_max_bet_player().chips

        # bet1 = 40%, 2.5BB

        elif new_node.identifier.is_action("b1"):
            current_bet = self.players.find_max_bet_player().bet

            # This is an open. Last statement may not be needed.
            if self.preflop and not self.players.has_opened() and current_bet == 1:
                player.chips = 97.5
                player.bet = 2.5
            else:

                new_bet = (self.players.pot_size() + current_bet) * 0.4 + current_bet
                player.chips = max(player.chips - (new_bet - player.bet), 0)
                player.bet = new_bet

            self.players.set_done_actions(False)

        # bet2 = 80%, 3BB
        elif new_node.identifier.is_action("b2"):
            current_bet = self.players.find_max_bet_player().bet

            if self.preflop and not self.players.has_opened() and current_bet == 1:

                player.chips = 96.5
                player.bet = 3.5
            else:
                new_bet = (self.players.pot_size() + current_bet) * 0.8 + current_bet
                player.chips = max(player.chips - (new_bet - player.bet), 0)
                player.bet = new_bet

            self.players.set_done_actions(False)

        player.action_done = True

        return new_node

    def find_next_player(self, current_player):
        self.players.update_remaining()
        next_player = None

        if self.preflop:
            current_pos = current_player.position_preflop
            while next_player is None:
                if current_pos >= self.players.max_position["preflop"]:
                    current_pos = self.players.min_position["preflop"] - 1

                next_player = self.players.find_player(position=current_pos + 1, preflop=True)
                current_pos += 1




        else:
            current_pos = current_player.position_postflop
            while next_player is None:
                if current_pos >= self.players.max_position["postflop"]:
                    current_pos = self.players.min_position["postflop"] - 1

                next_player = self.players.find_player(position=current_pos + 1, preflop=False)
                current_pos += 1
                print("pos is: " + str(current_pos))

        return next_player

    def request_node(self, current_node, current_player, all_players, ID):
        if current_node is not None:
            self.tree_Q.put(
                tree_package(current_node.identifier.name, current_player, all_players, None, "process", ID, is_bot=True))
        else:
            self.tree_Q.put(tree_package(None, current_player, all_players, None, "root", ID, is_bot=True))
        current_node = self.own_Q.get()
        return current_node

    def update_node_name(self, name, action):
        return "(" + name + ", " + action + ")"

    def find_bet_action(self, current_bet, new_bet):
        print("cur bet : " + str(current_bet))
        print("new bet : " + str(new_bet))
        print("pot : " + str(self.players.pot_size()))

        pot_size = (-current_bet + new_bet) / (self.players.pot_size() + current_bet)
        print("pot size bet:" + str(pot_size))
        if new_bet >= 95:
            return "AL"

        if not self.players.has_opened() and self.preflop:
            if 3 >= new_bet >= 2:
                return "b1"
            elif 6 >= new_bet > 3:
                return "b2"
            else:
                return "AL"

        if 0.6 > pot_size > 0:
            return "b1"
        elif 1.2 > pot_size >= 0.6:
            return "b2"
        else:
            return "AL"

    def click_action(self, cur_node, clicker):
        print("doing action for: " + str(cur_node) + " pot size: " + str(self.players.pot_size()))
        Open = True
        if self.hero.name == "SB" and self.players.pot_size() - self.hero.bet == 1:
            Open = False
        if self.players.pot_size() - self.hero.bet == 1.5:
            Open = False

        if cur_node.identifier.is_action("f"):
            clicker.fold()

        elif cur_node.identifier.is_action("ca"):
            if cur_node.identifier.allIn_occured():
                clicker.max()
            else:
                clicker.call()

        elif cur_node.identifier.is_action("b1"):
            clicker.bet1(Open)

        elif cur_node.identifier.is_action("b2"):
            clicker.bet2(Open)

        elif cur_node.identifier.is_action("AL"):
            clicker.max()

        elif cur_node.identifier.is_action("ch"):
            clicker.check()

    def update_street(self, deck, players, current_node, community):
        streets = ["preflop", "flop", "turn", "river", "end"]
        self.street = streets[streets.index(self.street) + 1]
        self.preflop = False

        for c in community:
            self.community.append(c)
            deck.remove_card(c)

        players.update_remaining()
        current_player = players.find_player(position=players.min_position["postflop"], preflop=False)
        players.set_done_actions(False, reset_bets=True)

        if self.street == "flop":
            current_node.identifier.name += "F:"

        elif self.street == "turn":
            current_node.identifier.name += "T:"

        elif self.street == "river":
            current_node.identifier.name += "R:"

        return current_player, current_node

    def process_unseen_actions_flop(self, current_node, folded_info):
        current_node = self.request_node(current_node, None, None, self.ID)
        print(current_node)

        while list(current_node.children)[0].identifier.flop == []:
            name, ac = list(current_node.children)[0].identifier.find_current_street()[-1]

            for p_name, folded in folded_info:
                if p_name == name:
                    if folded:
                        if p_name == "BB" and self.players.find_max_bet_player().bet == 1:
                            current_node.identifier.name += self.update_node_name(name, "ch")
                        else:
                            current_node.identifier.name += self.update_node_name(name, "f")
                    else:
                        if p_name == "BB" and self.players.find_max_bet_player().bet == 1:
                            current_node.identifier.name += self.update_node_name(name, "ch")
                        else:
                            current_node.identifier.name += self.update_node_name(name, "ca")

                    current_node = self.request_node(current_node, None, None, self.ID)
                    self.process_action_human(current_node, self.players.find_player(name=name), None)
            print(current_node)
        return current_node

    def process_unseen_actions_turn(self, current_node, folded_info):
        current_node = self.request_node(current_node, None, None, self.ID)
        print(current_node)

        while list(current_node.children)[0].identifier.turn == []:
            name, ac = list(current_node.children)[0].identifier.find_current_street()[-1]

            for p_name, folded in folded_info:
                if p_name == name:
                    if folded:
                        current_node.identifier.name += self.update_node_name(name, "f")
                    else:
                        if self.players.find_max_bet_player().bet == 0:
                            current_node.identifier.name += self.update_node_name(name, "ch")
                        else:
                            current_node.identifier.name += self.update_node_name(name, "ca")

                    current_node = self.request_node(current_node, None, None, self.ID)
                    self.process_action_human(current_node, self.players.find_player(name=name), None)
            print(current_node)
        return current_node

    def process_unseen_actions_river(self, current_node, folded_info):
        current_node = self.request_node(current_node, None, None, self.ID)
        print(current_node)

        while list(current_node.children)[0].identifier.river == []:
            name, ac = list(current_node.children)[0].identifier.find_current_street()[-1]

            for p_name, folded in folded_info:
                if p_name == name:
                    if folded:
                        current_node.identifier.name += self.update_node_name(name, "fo")
                    else:
                        if self.players.find_max_bet_player().bet == 0:
                            current_node.identifier.name += self.update_node_name(name, "ch")
                        else:
                            current_node.identifier.name += self.update_node_name(name, "ca")

                    current_node = self.request_node(current_node, None, None, self.ID)
                    self.process_action_human(current_node, self.players.find_player(name=name), None)
            print(current_node)
        return current_node
