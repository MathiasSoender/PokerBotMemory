import numpy as np
import heapq
from numba import jit, njit




# Figure out a way to determine the 5 greatest cards.
def HighCard(Rank, Hand, Community):
    High = np.zeros(5)
    HandAndCom = []
    Suits = []
    for c in Community:
        HandAndCom.append(c.value)
    for H in Hand:
        HandAndCom.append(H.value)

    for c in Community:
        Suits.append(c.suit)
    for H in Hand:
        Suits.append(H.suit)

    HandAndCom = np.array(HandAndCom)
    HandAndComSorted = sorted(HandAndCom, reverse=True)

    if Rank == 1:
        High = heapq.nlargest(5, HandAndCom)

    elif Rank == 2:
        for i in range(0, len(HandAndCom)):
            if np.count_nonzero(HandAndCom == HandAndCom[i]) == 2:
                High[0:2] = [HandAndCom[i]] * 2
        HandAndCom = list(filter((High[0]).__ne__, HandAndCom))
        High[2:] = heapq.nlargest(3, HandAndCom)

    elif Rank == 3:
        i = 0
        # Sorts the list with decreasing order
        HandAndComSorted = -np.sort(-HandAndCom)
        HandAndComSortedfoo = list(-np.sort(-HandAndCom))

        while i < len(HandAndComSorted):
            # Removes non pairs
            if np.count_nonzero(HandAndComSorted == HandAndComSorted[i]) != 2:
                HandAndComSorted = np.delete(HandAndComSorted, i)
                i -= 1

            i += 1
        # Grabs top two pairs, kicker is always last element, biggest pair first.
        High[0:4] = HandAndComSorted[0:4]
        HandAndComSortedfoo.remove(High[0])
        HandAndComSortedfoo.remove(High[0])
        HandAndComSortedfoo.remove(High[2])
        HandAndComSortedfoo.remove(High[2])
        High[4] = max(HandAndComSortedfoo)





    elif Rank == 4:
        for i in range(0, len(HandAndComSorted)):
            if np.count_nonzero(HandAndComSorted == HandAndComSorted[i]) == 3 and High[0] == 0:
                High[0:3] = [HandAndComSorted[i]] * 3
                HandAndComSorted = list(filter((High[0]).__ne__, HandAndComSorted))
                break
        High[3:] = heapq.nlargest(2, HandAndComSorted)

    elif Rank == 5:
        HandAndComSorted = list(reversed(list(set(HandAndCom))))
        j = 1
        High[0] = HandAndComSorted[0]

        for i in range(0, len(HandAndComSorted) - 1):
            if HandAndComSorted[i] - 1 == HandAndComSorted[i + 1]:
                High[j] = HandAndComSorted[i + 1]
                j += 1
            else:
                High = np.zeros(5)
                High[0] = HandAndComSorted[i + 1]
                j = 1
            if High[4] != 0:
                break

    elif Rank == 6:
        maxsuit = max(set(Suits), key=list(Suits).count)
        allC = list(Hand) + Community

        i = 0
        while i < len(allC):

            if allC[i].suit != maxsuit:
                allC.remove(allC[i])
                i -= 1
            i += 1

        values_cards = []
        for card in allC:
            values_cards.append(card.value)

        High = heapq.nlargest(5, values_cards)

    elif Rank == 7:
        i = 0
        while i < len(HandAndComSorted):

            if np.count_nonzero(HandAndComSorted == HandAndComSorted[i]) == 3 and High[0] == 0:
                High[0:3] = [HandAndComSorted[i]] * 3
                HandAndComSorted = list(filter((High[0]).__ne__, HandAndComSorted))
            elif np.count_nonzero(HandAndComSorted == HandAndComSorted[i]) in (2, 3):
                High[3:5] = [HandAndComSorted[i]] * 2
                HandAndComSorted = list(filter((High[3]).__ne__, HandAndComSorted))

            i += 1


    elif Rank == 8:
        for i in range(0, len(HandAndCom)):
            if np.count_nonzero(HandAndCom == HandAndCom[i]) == 4:
                High[0:4] = [HandAndCom[i]] * 4

        HandAndCom = list(filter((High[0]).__ne__, HandAndCom))
        High[4:] = heapq.nlargest(1, HandAndCom)

    return list(High)




def toJitInputFindRank(hand, com):
    handandcom = np.array([0] * (len(com) + 2))
    suits = np.array([""] * (len(com) + 2))

    for i, c in enumerate(com):
        handandcom[i] = c.value
        suits[i] = c.suit


    handandcom[-2] = hand[0].value
    handandcom[-1] = hand[1].value
    suits[-2] = hand[0].suit
    suits[-1] = hand[1].suit

    cc = np.array([ord(x) for x in suits])

    return handandcom, cc

@jit(nopython=True)
def HighCard_jit(Rank, HandAndCom, Suits):
    High = np.zeros(5)

    HandAndComSorted = np.sort(HandAndCom)[::-1]

    if Rank == 1:
       High[0:5] = HandAndComSorted[:5]

    elif Rank == 2:
        for i in range(0, len(HandAndComSorted)-1):
            if HandAndComSorted[i] == HandAndComSorted[i+1]:
                High[0:2] = np.array([HandAndComSorted[i]] * 2)
        HandAndComSorted = HandAndComSorted[np.where(HandAndComSorted != High[0])]

        High[2:] = HandAndComSorted[:3]

    elif Rank == 3:

        for i in range(0, len(HandAndComSorted)-1):
            if HandAndComSorted[i] == HandAndComSorted[i+1]:
                if High[0] == 0:
                    High[0:2] = np.array([HandAndComSorted[i]] * 2)
                else:
                    High[2:4] = np.array([HandAndComSorted[i]] * 2)

        HandAndComSorted = HandAndComSorted[np.where(HandAndComSorted != High[0])]
        HandAndComSorted = HandAndComSorted[np.where(HandAndComSorted != High[3])]

        High[4] = max(HandAndComSorted)


    elif Rank == 4:
        for i in range(0, len(HandAndComSorted)-2):
            if HandAndComSorted[i] == HandAndComSorted[i+1] == HandAndComSorted[i+2]:
                High[0:3] = np.array([HandAndComSorted[i]] * 3)
                HandAndComSorted = HandAndComSorted[np.where(HandAndComSorted != High[0])]
                break

        High[3:] = HandAndComSorted[:2]


    elif Rank == 5:
        HandAndComSorted = np.unique(HandAndComSorted)[::-1]
        j = 1
        High[0] = HandAndComSorted[0]

        for i in range(0, len(HandAndComSorted) - 1):
            if HandAndComSorted[i] - 1 == HandAndComSorted[i + 1]:
                High[j] = HandAndComSorted[i + 1]
                j += 1
            else:
                High = np.zeros(5)
                High[0] = HandAndComSorted[i + 1]
                j = 1
            if High[4] != 0:
                break

    elif Rank == 6:
        maxsuit = np.argmax(np.bincount(Suits))
        suitset = np.zeros(7)

        for i in range(0, len(Suits)):
            if Suits[i] == maxsuit:
                suitset[i] = HandAndCom[i]


        suitset = np.sort(suitset)[::-1]

        High = suitset[0:5]

    elif Rank == 7:

        for i in range(0, len(HandAndComSorted)-2):
            if HandAndComSorted[i] == HandAndComSorted[i+1] == HandAndComSorted[i+2]:
                High[0:3] = np.array([HandAndComSorted[i]] * 3)
                HandAndComSorted = HandAndComSorted[np.where(HandAndComSorted != High[0])]
                break

        for i in range(0, len(HandAndComSorted) - 1):
            if HandAndComSorted[i] == HandAndComSorted[i + 1]:
                High[3:5] = np.array([HandAndComSorted[i]] * 2)
                break

    elif Rank == 8:
        for i in range(0, len(HandAndComSorted) - 3):
            if HandAndComSorted[i] == HandAndComSorted[i + 1] == HandAndComSorted[i + 2] == HandAndComSorted[i + 3]:
                High[0:4] = np.array([HandAndComSorted[i]] * 4)
                break

        HandAndComSorted = HandAndComSorted[np.where(HandAndComSorted != High[0])]
        High[4] = max(HandAndComSorted)

    return High