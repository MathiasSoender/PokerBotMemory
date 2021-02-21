from Player.player import Player


class MP(Player):
    def __init__(self, hand):
        super().__init__(hand)

        self.name = "MP"
        self.chips = 100
        self.position_preflop = 2
        self.position_postflop = 4
        self.range.MP()


