from Player.all_players import Players
from Poker.Card import Card
from Player.player_types import CO, BB, BTN, SB, MP, UTG

p = Players(CO.CO([Card(14,"s"),Card(5,"d")]),
            BB.BB([Card(14,"s"),Card(5,"d")]),
            BTN.BTN([Card(14,"s"),Card(5,"d")]),
            SB.SB([Card(14,"s"),Card(14,"d")]),
            MP.MP([Card(14, "s"), Card(5, "d")]),
            UTG.UTG([Card(14, "s"), Card(5, "d")]))

print(p.determine_winner([Card(5,"s"),Card(10,"d"),Card(7,"h"),Card(4,"c"),Card(14,"c")]))