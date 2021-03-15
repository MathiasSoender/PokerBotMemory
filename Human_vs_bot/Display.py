
class Display:
    def __init__(self):
        self.exit = False



    def print_card(self, card):
        val1 = card.value
        if val1 == 14:
            val1 = "A"
        elif val1 == 13:
            val1 = "K"
        elif val1 == 12:
            val1 = "Q"
        elif val1 == 11:
            val1 = "J"

        s1 = card.suit
        if s1 == "s":
            s1 = "♠"
        elif s1 == "h":
            s1 = "♥"
        elif s1 == "c":
            s1 = "♣"
        elif s1 == "d":
            s1 = "♦"

        return str(val1) + s1

    def start_print(self):
        print("#----------# Welcome to The Singularity Poker AI #----------# \n\n")
        while True:
            print("Press 1 + Enter to start")
            if input() == "1":
                break
        self.loading_init()


    def loading_init(self):
        print("Loading bots...")

    def new_round(self, bank_roll, hands_played):
        print("\n#-#  Hand Done  #-#\n")
        print("Current winning/losses: " + str(bank_roll))
        print("Number of hands played: " + str(hands_played) + "\n")

        while True:
            print("#-# Options: #-#")
            print(" - Press 1 + Enter to exit")
            print(" - Press 2 + Enter for next hand\n")

            inp = input()
            if inp in ["1","2"]:
                break

        if int(inp) == 1:
            self.exit = True

    def new_hand(self, hero):
        print("\n new round started. Your hand: " + self.print_card(hero.hand[0]) + " , " + self.print_card(hero.hand[1]))
        print(" Your position is: " + hero.name)

    def create_community(self, com):
        string_com = ""
        for c in com:
            string_com += self.print_card(c) + " , "
        return string_com

    def print_state(self, controller, players):
        string_com = self.create_community(controller.community)

        def player_string(player):
            if player.folded:
                return "       "

            s = ""
            if player.hero:
                s = "(you), "
            s += player.name + ", "
            s += "bet: " + str(player.bet) + ", "
            s += "chips remain: " + str(player.chips)
            return s
        SB_s = player_string(players.SB)
        BB_s = player_string(players.BB)
        UTG_s = player_string(players.UTG)
        CO_s = player_string(players.CO)
        MP_s = player_string(players.MP)
        BTN_s = player_string(players.BTN)
        pot = str(players.pot_size())

        print("                                    Community: " + string_com[:-3])
        print("")
        print("                  " + UTG_s)
        print("")
        print(BB_s + "                                    " + MP_s)
        print("                                     pot: " + pot)
        print(SB_s + "                                    " + CO_s)
        print("")
        print("                  " + BTN_s)
        print("")


    def actions(self, current_node):
        for idx, child in enumerate(current_node.children):
            print("Press: " + str(idx) + " for: " + str(child.identifier.find_current_street()[-1][1]))

        return current_node.children[int(input())]

    def showdown(self, winner, pot, community, players):
        for w in winner:
            print("Winner is: " + str(w.name) + " hand: " + self.print_card(w.hand[0]) + ", " + self.print_card(w.hand[1]))
        for p in players.players:
            if p not in winner:
                print("Loser: " + str(p.name) + " hand: " + self.print_card(p.hand[0]) + ", " + self.print_card(p.hand[1]))
        print("board: " + str(self.create_community(community)))
        print("pot: " + str(pot))
        print("\n")