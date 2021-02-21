from Player.player import Player


class UTG(Player):
    def __init__(self, hand):
        super().__init__(hand)

        self.name = "UTG"
        self.chips = 100
        self.position_preflop = 1
        self.position_postflop = 3
        self.range.UTG()


