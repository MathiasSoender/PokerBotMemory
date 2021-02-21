
class loggerNonStatic:
    def __init__(self, ID):
        self.path = "log" + str(ID) + ".txt"

    def log(self, text, sep = "\n"):
        with open(self.path, "a") as text_file:
            text_file.write(text + sep)

    def new_round(self):
        self.log("\n\n\n############################# NEW HAND ####################### \n\n")

    def end_log(self, players, winner, community, pot):

        hands = []
        com = []
        winners = []
        for w in winner:
            winners.append(str(w))

        for player in players:
            hands.append((player.name, str(player.hand[0]) + str(player.hand[1])))
        for c in community:
            com.append(str(c))
        self.log("Player hands: " + str(hands))
        self.log("Community: " + str(com))
        self.log("Winner: " + str(winners))
        self.log("Pot: " + str(pot))

    def nodes_log(self, nodes, txt = "Before"):
        self.log("")
        self.log(txt)
        for node in nodes:
            ac = str(node[0].identifier.find_current_street()[-1])

            if ac == "F:":
                ac = node[0].identifier.preflop[-1]
            elif ac == "T:":
                ac = node[0].identifier.flop[-1]
            elif ac == "R:":
                ac = node[0].identifier.turn[-1]
            elif ac == "end":
                ac = node[0].identifier.river[-1]

            self.log("Node: " + str(ac) + " " + str(node[0].data))
        self.log("")

    def children_log(self, nodes):
        for node, dis in nodes:
            self.log(str(node.identifier.find_current_street()[-1]) + ": " + str(round(dis,3)) + ", ", sep=" ")
        self.log("")

