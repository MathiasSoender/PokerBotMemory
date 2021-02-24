import pickle
import gc
import os

class precomputed_odds:

    def __init__(self, filename = "pre_odds", new_odds = False):
        self.odds = dict()
        if not new_odds:
            try:
                self.get_object(filename)
            except:
                print("new pre_odds created")



    def __find_first_key(self, hand, name):
        suited = "OS" # Off suit
        if hand[0].suit == hand[1].suit:
            suited = "S" # Suited

        return name + str(hand[0].value) + str(hand[1].value) + suited

    def __find_second_key(self, opponenets, name):
        opponenets_info = ""
        for player in opponenets.players:
            if player.name != name:
                opponenets_info += str((player.name, player.range_num))
        return opponenets_info

    def __sort_hand(self, hand):
        hand_sorted = []
        if hand[0].value < hand[1].value:
            hand_sorted.append(hand[1])
            hand_sorted.append(hand[0])
        else:
            hand_sorted = hand
        return hand_sorted

    def add(self, hand, name, opponenets, odds, controller=None):
        odds = round(odds, 5)
        hand = self.__sort_hand(hand)

        first_key = self.__find_first_key(hand, name)

        if first_key not in self.odds:
            self.odds[first_key] = dict()

        opponenets_info = self.__find_second_key(opponenets, name)

        if opponenets_info not in self.odds[first_key]:
            self.odds[first_key][opponenets_info] = odds
            if controller is not None:
                controller.expanded_odds.append((opponenets_info, first_key, odds))


    def find_odds(self, hand, name, opponenets):
        hand = self.__sort_hand(hand)

        first_key = self.__find_first_key(hand, name)
        opponenets_info = self.__find_second_key(opponenets, name)

        if first_key not in self.odds:
            return None

        if opponenets_info not in self.odds[first_key]:
            return None

        return self.odds[first_key][opponenets_info]




    def to_object(self, filename):
        gc.disable()
        with open(filename, 'wb') as file:
            pickle.dump(self, file, protocol=pickle.HIGHEST_PROTOCOL)
        gc.enable()


    def get_object(self, filename):
        gc.disable()
        with open(filename, 'rb') as file:
            t = pickle.load(file)
        self.odds = t.odds
        gc.enable()

