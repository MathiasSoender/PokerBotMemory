from Player.player import Player


class CO(Player):
    def __init__(self, hand):
        super().__init__(hand)

        self.name = "CO"
        self.chips = 100
        self.position_preflop = 3
        self.position_postflop = 5
        self.range.CO()


