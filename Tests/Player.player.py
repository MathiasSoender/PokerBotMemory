from Player.player_types import BB, BTN, CO, MP, SB, UTG
from Player.all_players import Players
from Poker.Card import Card
from Poker.Deck import Deck
from Controllers.Game_controller import game_controller

gc = game_controller()
import time
P = Players(UTG.UTG([Card(11, "s"), Card(5, "d")]),
            BB.BB([Card(2, "s"), Card(7, "d")]),
            SB.SB([Card(14, "s"), Card(13, "d")]),
            MP.MP([Card(6, "s"), Card(8, "d")]),
            BTN.BTN([Card(10, "s"), Card(9, "s")]),
            CO.CO([Card(14, "c"), Card(14, "d")]))

P.UTG.folded = True


t1 = time.time()
for k in range(0, 100):
    P.SB.determine_odds(P, gc)
    P.SB.last_odds = k
    print(P.SB.win_odds)
print(time.time()-t1)
