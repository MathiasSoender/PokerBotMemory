from Player.all_players import Players
from Poker.Card import Card
from Player.player_types import CO, BB, BTN, SB, MP, UTG



pp = Players(UTG.UTG([Card(14, "s"), Card(11, "d")]), BB.BB([Card(14,"s"),Card(11,"s")]), SB.SB([Card(2,"s"),Card(7,"d")]),
             MP.MP([Card(14, "s"), Card(5, "d")]), BTN.BTN([Card(14,"s"),Card(5,"d")]), CO.CO([Card(14,"s"),Card(5,"d")]))


pp.MP.folded = True
pp.CO.folded = True
pp.BTN.folded = True

print(pp.determine_winner([Card(14,"s"),Card(14,"s"),Card(12,"h"),Card(2,"s"),Card(3,"c")]))

# Error^