from Player.player import Player


class SB(Player):
    def __init__(self, hand):
        super().__init__(hand)
        self.name = "SB"
        self.chips = 99.5
        self.position_preflop = 5
        self.position_postflop = 1
        self.folded = False
        self.range.SB()
        self.bet = 0.5



