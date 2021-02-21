# Working
import time

from Bot.Readers.misc import change_dir
from Bot.Readers.readerCard import find_card


class ReaderHand:

    def __init__(self, ID):
        self.Hand = []
        self.Conf1 = 0
        self.Conf2 = 0

        if ID == 0:
            self.leftNumRegion = (433, 456, 25, 30)
            self.rightNumRegion = (486, 456, 28, 30)
            self.leftSuitRegion = (457, 456, 40, 40)
            self.rightSuitRegion = (509, 456, 40, 40)


        elif ID == 1:
            self.leftNumRegion = (433, 456, 25, 30)
            self.rightNumRegion = (486, 456, 28, 30)
            self.leftSuitRegion = (457, 456, 40, 40)
            self.rightSuitRegion = (509, 456, 40, 40)


    def Read(self):
        change_dir("cards")
        Conf1, card1 = find_card(self.leftNumRegion, self.leftSuitRegion)
        self.Conf1 = Conf1
        self.Hand.append(card1)

        Conf2, card2 = find_card(self.rightNumRegion, self.rightSuitRegion)
        self.Conf2 = Conf2
        self.Hand.append(card2)

        print("Hand is: " + str(self.Hand[0]) + " " + str(self.Hand[1]))

if __name__ == "__main__":
    time.sleep(1)
    R = ReaderHand(ID=0)
    R.Read()

