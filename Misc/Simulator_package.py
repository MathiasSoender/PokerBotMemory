
class package:
    def __init__(self, selected_nodes, community, players, pot, winner, request):
        self.selected_nodes = selected_nodes
        self.community = community
        self.players = players
        self.pot = pot
        self.winner = winner
        self.request = request


class pre_computed_package:
    def __init__(self, hand, name, opponents, request, ID, odds = None):
        self.hand = hand
        self.name = name
        self.opponents = opponents
        self.request = request
        self.ID = ID
        self.odds = odds

class tree_package:
    def __init__(self, current_node_name, current_player, all_players, controller, request, ID, is_bot = False, community = [], subtree=None):
        self.current_node_name = current_node_name
        self.current_player = current_player
        self.all_players = all_players
        self.controller = controller
        self.request = request
        self.ID = ID
        self.is_bot = is_bot
        self.community = community
        self.subtree = subtree

class click_package:
    def __init__(self, request, ID):
        self.ID = ID
        self.request = request

