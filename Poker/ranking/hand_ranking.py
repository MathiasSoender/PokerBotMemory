import copy

class rank_hand:
    def __init__(self, Hand, Community):
        self.rank = 1
        self.Hand = Hand
        self.Community = Community

        self.HandAndCom = []
        self.Suits = []
        for c in Community:
            self.HandAndCom.append(c.value)
        for H in Hand:
            self.HandAndCom.append(H.value)

        for c in Community:
            self.Suits.append(c.suit)
        for H in Hand:
            self.Suits.append(H.suit)

        self.unique = list(set(self.HandAndCom))
        self.counts = 0
        for ele in self.HandAndCom:
            self.counts = max(list(self.HandAndCom).count(ele), self.counts)


    def Quads(self):
        if self.counts == 4:
            self.rank = 8

    def Full_house(self):
        two_same = False
        three_same = False
        three_same_twice = False
        for i in range(len(self.unique)):
            if self.HandAndCom.count(self.unique[i]) == 2:
                two_same = True
            if self.HandAndCom.count(self.unique[i]) == 3:
                if three_same:
                    three_same_twice = True
                three_same = True
            if (two_same or three_same_twice) and three_same:
                self.rank = 7
                return


    def Flush(self):
        counts_suit = 0
        for ele in self.Suits:
            counts_suit = max(counts_suit, list(self.Suits).count(ele))

            if counts_suit >= 5:

                self.rank = 6
                return


    def Straight(self):
        # Straight:
        if self.unique[0] == 2 and self.unique[-1] == 14:
            straightSum = 2
        else:
            straightSum = 1
        for i in range(0, len(self.unique) - 1):
            if self.unique[i] + 1 == self.unique[i + 1]:
                straightSum += 1
            else:
                straightSum = 1
            if straightSum >= 5:
                self.rank = 5
                return



    def Set(self):
        if self.counts == 3:
            self.rank = 4


    def Two_pair(self):
        TwoPairs = 0
        for i in range(len(self.unique)):
            if self.HandAndCom.count(self.unique[i]) == 2:
                TwoPairs += 1

            if TwoPairs>=2:
                self.rank = 3
                return

    def One_pair(self):
        if self.counts == 2:
            self.rank = 2

    def find_rank_initial(self):
        methods = [self.Quads, self.Full_house, self.Flush, self.Straight, self.Set, self.Two_pair, self.One_pair]
        rank_foo = 1
        for m in methods:
            m()
            if self.rank != rank_foo:
                return

    def find_rank_second(self, vil_rank):
        methods = [self.One_pair, self.Two_pair, self.Set, self.Straight, self.Flush, self.Full_house, self.Quads]
        for m in methods:
            m()
            if self.rank > vil_rank:
                return



