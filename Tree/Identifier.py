import copy


class Identifier:
    __slots__ = 'preflop', 'flop', 'turn', 'river', 'name'

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
                    idname = PN_int_to_string(idname)
                    action = A_int_to_string(action)
                    self.name += "(" + str(idname) + ", " + str(action) + ")"

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
                if action in [1.0, 2.0, 3.0, 7.0]:
                    return True

        if self.find_current_street() == self.preflop:
            name = PN_string_to_int(name)
            if name in [1.0, 2.0, 3.0, 4.0, 5.0]:
                return True


        return False

    def allIn_occured(self):
        for _, action in self.find_current_street():
            if action == 7.0:
                return True
        return False

    def is_action(self, action):
        _, chosen_action = self.find_current_street()[-1]
        if chosen_action == A_string_to_int(action):
            return True
        return False

    def update_street_list(self, new_element, street=None):
        transformed_element = (PN_string_to_int(new_element[0]), A_string_to_int(new_element[1]))
        if street is None:
            self.find_current_street().append(transformed_element)

        else:
            if street is "river":
                self.river.append(transformed_element)
            elif street is "turn":
                self.turn.append(transformed_element)
            elif street is "flop":
                self.flop.append(transformed_element)
            elif street is "preflop":
                self.preflop.append(transformed_element)

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



def PN_int_to_string(name_int):

    if name_int == 1.0:
        return "UTG"
    if name_int == 2.0:
        return "MP"
    if name_int == 3.0:
        return "CO"
    if name_int == 4.0:
        return "BTN"
    if name_int == 5.0:
        return "SB"
    if name_int == 6.0:
        return "BB"


def A_int_to_string(action_int):
    if action_int == 1.0:
        return "b1"
    if action_int == 2.0:
        return "b2"
    if action_int == 3.0:
        return "b3"
    if action_int == 4.0:
        return "f"
    if action_int == 5.0:
        return "ca"
    if action_int == 6.0:
        return "ch"
    if action_int == 7.0:
        return "AL"

def PN_string_to_int(name):
    if name == "UTG":
        return 1.0
    if name == "MP":
        return 2.0
    if name == "CO":
        return 3.0
    if name == "BTN":
        return 4.0
    if name == "SB":
        return 5.0
    if name == "BB":
        return 6.0
def A_string_to_int(action):
    if action == "b1":
        return 1.0
    if action == "b2":
        return 2.0
    if action == "b3":
        return 3.0
    if action == "f":
        return 4.0
    if action == "ca":
        return 5.0
    if action == "ch":
        return 6.0
    if action == "AL":
        return 7.0


def tuple_int_to_string(TUPLE):
    return (PN_int_to_string(TUPLE[0]), A_int_to_string(TUPLE[1]))