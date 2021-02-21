from Player.player import Player


class BTN(Player):
    def __init__(self, hand):
        super().__init__(hand)

        self.name = "BTN"
        self.chips = 100
        self.position_preflop = 4
        self.position_postflop = 6
        self.range.BTN()


