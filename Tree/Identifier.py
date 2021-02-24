import copy


class Identifier:
    def __init__(self, ID=None):

        if ID is None:
            self.preflop = []
            self.flop = []
            self.turn = []
            self.river = []
            self.name = ""
        else:
            self.preflop = copy.deepcopy(ID.preflop)
            self.flop = copy.deepcopy(ID.flop)
            self.turn = copy.deepcopy(ID.turn)
            self.river = copy.deepcopy(ID.river)
            self.name = ""

    def create_name(self, is_root=False):
        if is_root:
            self.name = "root"
            return

        all_actions = [("P", self.preflop), ("F", self.flop), ("T", self.turn), ("R", self.river)]

        for denote, street_list in all_actions:
            for idname, action in street_list:
                if idname == denote:
                    self.name += denote + ":"
                else:
                    self.name += "(" + idname + ", " + action + ")"

    def find_current_street(self):
        if self.river:
            return self.river
        elif self.turn:
            return self.turn
        elif self.flop:
            return self.flop
        else:
            return self.preflop

    def call_available(self, new_street, preflop, name=None):
        # Special case
        if new_street[0] and not preflop:
            return False

        if not new_street[0]:
            for _, action in self.find_current_street():
                if action in ["b1", "b2", "b3", "AL"]:
                    return True

        if self.find_current_street() == self.preflop:
            if name in ["UTG", "MP", "CO", "SB", "BTN"]:
                return True


        return False

    def allIn_occured(self):
        for _, action in self.find_current_street():
            if action == "AL":
                return True
        return False

    def is_action(self, action):
        _, chosen_action = self.find_current_street()[-1]
        if chosen_action == action:
            return True
        return False

    def update_street_list(self, new_element, street=None):
        if street is None:
            self.find_current_street().append(new_element)
        else:
            if street is "river":
                self.river.append(new_element)
            elif street is "turn":
                self.turn.append(new_element)
            elif street is "flop":
                self.flop.append(new_element)
            elif street is "preflop":
                self.preflop.append(new_element)

    def update_new_street(self, new_street):
        is_new, street = new_street
        if is_new:
            if street == "P:" and self.preflop == []:
                self.preflop = ["P:"]

            elif street == "F:" and self.flop == []:
                self.flop = ["F:"]

            elif street == "T:" and self.turn == []:
                self.turn = ["T:"]

            elif street == "R:" and self.river == []:
                self.river = ["R:"]

    def __str__(self):
        return str(self.name)
