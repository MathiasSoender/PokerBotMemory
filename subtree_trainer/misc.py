from Controllers.Game_controller import game_controller
from Poker.Deck import Deck
import random


def parse_actions(root, community, players, street, denote):
    GC = game_controller()

    D = Deck()
    GC.community = community
    GC.new_street = [False, ""]
    if not community:
        GC.preflop = True
    else:
        GC.preflop = False

    GC.street = street

    if denote in ["F:", "T:", "R:"]:
        GC.new_street = [True, denote]

    # Deck stuff
    for c in community:
        D.remove_card(c)

    for c in players.find_hero().hand:
        D.remove_card(c)


    # Draw valid hand for opponents:
    for p in players.players:
        if not p.folded and not p.hero:
            while p.hand is None:
                p.hand = D.draw_from_range(p.range_num, p.range.range, random.randrange(0, 13), random.randrange(0, 13))
            p.hand = list(p.hand)

    for p in players.players:
        print("name: " + str(p.name) + " hand: " + str(p.hand))




    return GC, D, players

