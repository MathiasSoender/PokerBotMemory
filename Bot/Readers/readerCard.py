import pyautogui as py
from Poker.Card import Card


def find_card(current_region_c, current_region_s):
    broken = False
    suits_denom = ["s", "h", "c", "d"]


    n = 0.95

    while broken is False:
        if n <= 0.91:
            n = 0.95

        for x in range(2, 15):
            if py.locateOnScreen(str(x) + ".png", confidence=n, region=current_region_c, grayscale=True) is not None:
                Val = x
                broken = True
                break

        n = n - 0.01

    for s in suits_denom:
        if py.locateOnScreen(str(s) + ".png", confidence=0.95, region=current_region_s) is not None:
            suit = s
            break

    return n + 0.01, Card(Val, suit)