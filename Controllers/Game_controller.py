from Player.all_players import Players
from Player.player_types import BB, BTN, CO, MP, SB, UTG
import copy
from Misc.Simulator_package import tree_package

class game_controller:
    def __init__(self):
        self.current_turn = 1
        self.preflop = True
        self.game_ended = False
        self.street = "preflop"
        self.selected_nodes = []
        self.new_street = []
        self.community = []


    def start_game(self, deck):
        bb = BB.BB([deck.draw(), deck.draw()])
        sb = SB.SB([deck.draw(), deck.draw()])
        btn = BTN.BTN([deck.draw(), deck.draw()])
        co = CO.CO([deck.draw(), deck.draw()])
        mp = MP.MP([deck.draw(), deck.draw()])
        utg = UTG.UTG([deck.draw(), deck.draw()])
        players = Players(utg, bb, sb, mp, btn, co)
        self.new_street = [True, "P:"]

        return players

    def do_action(self, current_node, player, players, LOG = None, Human = False, is_local_sim = False):
        # Prob_of_child = Pi
        if not Human:
            new_node, prob_of_child = current_node.select_child(player.win_odds, LOG=LOG, prob=30)
        else:
            new_node = current_node
            prob_of_child = 1

        if self.preflop:
            player.update_range_num(new_node)

        # Info which is passed to master
        if is_local_sim:
            self.selected_nodes.append((new_node, player.win_odds, player, prob_of_child))
        else:
            self.selected_nodes.append((new_node.identifier, player.win_odds, player, prob_of_child))

        if new_node.identifier.is_action("fold"):
            player.folded = True
            player.bet = 0

        elif new_node.identifier.is_action("allIn"):
            player.chips = 0
            player.bet = 100
            players.set_done_actions(False)

        elif new_node.identifier.is_action("call"):
            player.chips = players.find_max_bet_player().chips

        # bet1 = 40%, 2.5BB
        elif new_node.identifier.is_action("bet1"):
            current_bet = players.find_max_bet_player().bet

            # This is an open. Last statement may not be needed.
            if self.preflop and not players.has_opened() and current_bet == 1:
                player.chips = 97.5
                player.bet = 2.5
            else:
                # Pot already holds the bets
                new_bet = (players.pot_size() + current_bet) * 0.4 + current_bet

                player.chips = max(player.chips - (new_bet - player.bet), 0)
                player.bet = new_bet

            players.set_done_actions(False)

        # bet2 = 80%, 3BB
        elif new_node.identifier.is_action("bet2"):
            current_bet = players.find_max_bet_player().bet

            if self.preflop and not players.has_opened() and current_bet == 1:
                player.chips = 96.5
                player.bet = 3.5
            else:
                new_bet = (players.pot_size() + current_bet) * 0.8 + current_bet
                player.chips = max(player.chips - (new_bet - player.bet), 0)
                player.bet = new_bet

            players.set_done_actions(False)

        player.action_done = True


        return new_node

    def check_if_game_ended(self, players):
        if players.remaining_length() == 1 or self.street == "end":
            self.game_ended = True
            return
        for player in players.players:
            if player.chips != 0:
                self.game_ended = False
                return
        self.game_ended = True


    def check_if_street_ended(self, players):
        if players.done_actions():
            return True
        return False


    def update_street(self, deck, players):
        streets = ["preflop", "flop", "turn", "river", "end"]
        self.street = streets[streets.index(self.street)+1]
        self.preflop = False

        if self.street == "flop":
            for _ in range(3):
                self.community.append(deck.draw())
            self.new_street = [True, "F:"]

        elif self.street in ["turn", "river"]:
            self.community.append(deck.draw())
            if self.street == "turn":
                self.new_street = [True, "T:"]
            else:
                self.new_street = [True, "R:"]

        current_player = players.find_player(position=players.min_position["postflop"], preflop=self.preflop)
        players.set_done_actions(False, reset_bets=True)

        return current_player



    def find_winner(self, players, deck):

        if players.remaining_length() == 1:
            winner = players.players
        else:
            while len(self.community) < 5:
                self.community.append(deck.draw())

            winner = players.determine_winner(self.community)

        return winner

    """ Used only by master """
    def back_prop(self, pot, winner):
        name_winners = [w.name for w in winner]

        for node, odds, player, pi in self.selected_nodes:
            if player.folded:
                node.data.update(odds, pi, player.chips - 100, node.siblings())
            else:
                # If the player has won, all chips in the pot / len(winners) is associated to his nodes
                if player.name in name_winners:
                    # pi = probability of selecting child.
                    # - his own chips (he does not win these, simply gets em back)
                    node.data.update(odds, pi, pot / len(winner) - (100 - player.chips), node.siblings())
                else:
                    node.data.update(odds, pi, player.chips - 100, node.siblings())


    def find_next_player(self, current_player, players):
        players.update_remaining()
        next_player = None


        if self.preflop:
            current_pos = current_player.position_preflop
            while next_player is None:
                if current_pos >= players.max_position["preflop"]:
                    current_pos = players.min_position["preflop"] - 1

                next_player = players.find_player(position=current_pos+1, preflop=True)
                current_pos += 1



        else:
            current_pos = current_player.position_postflop
            while next_player is None:
                if current_pos >= players.max_position["postflop"]:
                    current_pos = players.min_position["postflop"] - 1

                next_player = players.find_player(position=current_pos+1, preflop=False)
                current_pos += 1

        return next_player

    def request_node(self, current_node, tree_Q, P, current_player, all_players, ID):
        if current_node is not None:
            tree_Q.put(tree_package(current_node.identifier.name, current_player, all_players, self, "process", ID))
        else:
            tree_Q.put(tree_package(None, current_player, all_players, self, "root", ID))

        current_node = P.get()
        return current_node


