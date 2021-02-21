from Player.player import Player


class BB(Player):
    def __init__(self, hand):
        super().__init__(hand)
        self.name = "BB"
        self.chips = 99
        self.position_preflop = 6
        self.position_postflop = 2
        self.range.BB()
        self.bet = 1




