from abc import ABC, abstractmethod

from Evaluation.naiveHandEvaluation import evalHand
from Range.Range import Range
import copy
import random
from Poker.Deck import Deck
from Misc.Simulator_package import pre_computed_package
import gc

from Tree.Identifier import PN_int_to_string, A_int_to_string


class Player(ABC):
    def __init__(self, hand):
        self.folded = False
        self.hand = hand
        self.range = Range()
        self.win_odds = 0
        self.range_num = [0, 1, 2, 3, 4, 5]
        self.name = ""
        self.chips = None
        self.bet = 0
        self.action_done = False
        self.last_odds = "preflop"
        self.hero = False

    def compute_rounds(self, all_opponents):
        rounds = 500 * all_opponents.remaining_length()

        if self.last_odds != "preflop":
            rounds *= 0.5
        if self.last_odds == "turn":
            rounds *= 0.5
        if self.last_odds == "river":
            rounds *= 0.5

        return int(rounds)

    def check_pre_computed(self, street, pre_computed_Q, channel, ID, all_opponents):

        if self.last_odds != "preflop" and self.last_odds == street:
            return False
        self.last_odds = street

        if pre_computed_Q is not None and street == "preflop":
            pre_computed_Q.put(pre_computed_package(self.hand, self.name, all_opponents, "process", ID))
            isComputed, precomputed = channel.get()

            if isComputed:
                self.win_odds = precomputed
                return False
        return True



    def determine_odds(self, all_opponents, controller, pre_computed_Q = None, ID = None, channel = None):
        community = controller.community
        street = controller.street

        # Check if odds has been calcuated before
        if not self.check_pre_computed(street, pre_computed_Q, channel, ID, all_opponents):
            return

        rounds = self.compute_rounds(all_opponents)

        win_percentage = 0

        # Make deep copies of all relevant objects:
        random_hands_opponents = copy.deepcopy(all_opponents)
        current_deck = Deck()
        for d in range(0, len(self.hand + community)):
            current_deck.remove_card((self.hand + community)[d])

        for _ in range(rounds):
            current_community = copy.deepcopy(community)

            # Fill community with random cards. We do not remove these, may be an issue (improves runtime tho)
            while len(current_community) < 5:
                current_community.append(current_deck.draw(remove=False))

            for opponent in random_hands_opponents.players:
                # Start by drawing valid hand:
                # Exclude your own current hand:
                if opponent.name != self.name:
                    opponent.hand = None
                i = 0
                while opponent.hand is None:
                    opponent.hand = current_deck.draw_from_range(opponent.range_num, opponent.range.range,
                                                                 random.randrange(0, 13), random.randrange(0, 13),
                                                                 remove=False)
                    i += 1
                    if i > 5000:
                        return
            # All opponents have a hand now, from their range. Find winner
            winners = random_hands_opponents.determine_winner(current_community)

            # assign win
            if len(winners) == 1 and winners[0].name == self.name:
                win_percentage += 1
            # Win percentage reflects split pots:
            elif len(winners) > 1:
                for winner in winners:
                    if winner.name == self.name:
                        win_percentage += 1 / len(winners)
                        break

        self.win_odds = (win_percentage / rounds) + evalHand(self.hand, street)
        if pre_computed_Q is not None:
            pre_computed_Q.put((pre_computed_package(self.hand, self.name, all_opponents,
                                                     "add", ID, odds=self.win_odds)))

    def update_range_num(self, node):
        _open = False
        _shove = False
        _threeBet = False
        _fourBet = False
        _multiWay = False
        _big_open = False

        # Select all previous actions:
        for name, action in node.identifier.preflop[0:-1]:
            name = PN_int_to_string(name)
            action = A_int_to_string(action)
            if action in ["b1", "b2", "b3"]:
                if _threeBet:
                    _fourBet = True
                if _open:
                    _threeBet = True

                if action == "bet3":
                    _big_open = True
                _open = True
                _multiWay = False

            elif action == "ca":
                _multiWay = True

            elif action == "AL":
                _shove = True
                _multiWay = False



        name, action = node.identifier.preflop[-1]
        name = PN_int_to_string(name)
        action = A_int_to_string(action)
        if name != self.name:
            raise Exception("Error in update_range_num... last action is not equal the player")

        # Special rules for the BB
        if self.name == "BB":
            # If the last action is check, we know that 1+ players limped.
            if action == "ch":
                self.range_num = [0, 1]
                return

            elif action == "ca":
                if _shove:
                    self.range_num = [5]
                elif _fourBet:
                    self.range_num = [4]
                elif _threeBet:
                    self.range_num = [3]
                elif _open:
                    if _big_open:
                        if _multiWay:
                            self.range_num = [2]
                        else:
                            self.range_num = [3]
                    else:
                        if _multiWay:
                            self.range_num = [1, 2]
                        else:
                            self.range_num = [2]
                return

        # All players:
        if action in ["b1", "b2", "b3"]:
            if _fourBet:
                self.range_num = [5]
            elif _threeBet:
                self.range_num = [4, 5]
            elif _open:
                self.range_num = [3, 4, 5]
            else:
                if action == "bet3":
                    self.range_num = [2, 3, 4, 5]
                else:
                    self.range_num = [1, 2, 3, 4, 5]


        elif action == "AL":
            if not _fourBet and not _multiWay:
                self.range_num = [4, 5]
            else:
                self.range_num = [5]

        elif action == "fo":
            self.range_num = [0]

        elif action == "ca":
            if _shove:
                self.range_num = [5]
            elif _fourBet:
                self.range_num = [4]
            elif _threeBet:
                self.range_num = [3]
            elif _open:
                self.range_num = [2]
            # Limp:
            else:
                self.range_num = [0]

    def __str__(self):
        return str((self.name + ", "+ "folded: " + str(self.folded) + ", chips: " + str(self.chips) +
                    ", range num: " + str(self.range_num) + ", hand: " + str(self.hand[0]) + str(self.hand[1])))
