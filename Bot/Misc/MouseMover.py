import pyautogui as p
import random


def HumanMovementCreator(EndX, EndY, Certaincy):
    EndPos = (EndX, EndY)
    p.MINIMUM_DURATION = 0.005
    p.MINIMUM_SLEEP = 0.005
    p.PAUSE = 0.005

    i = 0
    while i == 0:
        Pos = p.position()
        PosDifference = ((EndPos[0] - Pos[0]), (EndPos[1] - Pos[1]))

        TotalDifference = abs(PosDifference[0]) + abs(PosDifference[1])

        if TotalDifference > 500:
            Certaincy = Certaincy + 2

        Divider = (PosDifference[0] / Certaincy, PosDifference[1] / Certaincy)
        Divider = (int(Divider[0]), int(Divider[1]))

        if abs(Divider[0]) > abs(Divider[1]):
            Maxer = Divider[0]
        if abs(Divider[1]) > abs(Divider[0]):
            Maxer = Divider[1]
        if abs(Divider[0]) == abs(Divider[1]):
            Maxer = Divider[0]

        if Maxer == 0:
            Maxer = 1

        MoveX = PosDifference[0] / abs(Maxer)
        MoveY = PosDifference[1] / abs(Maxer)

        for o in range(0, abs(Maxer)):
            p.moveRel(MoveX * random.uniform(0.6, 1.4), MoveY * random.uniform(0.6, 1.4), 0.0045)

        Pos = p.position()
        PosDifference = ((EndPos[0] - Pos[0]), (EndPos[1] - Pos[1]))

        if abs(PosDifference[0]) < 15 and abs(PosDifference[1]) < 15:
            p.moveTo(EndX, EndY, random.uniform(0.05, 0.1))
            i = 1

        if TotalDifference > 500:
            Certaincy = Certaincy / 2
