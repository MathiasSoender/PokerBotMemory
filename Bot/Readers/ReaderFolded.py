# Works

import pyautogui as py

from Bot.Readers.misc import change_dir


class ReaderFolded:
    def __init__(self, ID):
        self.folded = []

        if ID == 0:
            self.leftBottom = (100, 340, 70, 50)
            self.leftTop = (125, 140, 70, 50)
            self.top = (450, 79, 70, 50)
            self.rightTop = (780, 140, 70, 50)
            self.rightBottom = (810, 340, 70, 50)


        elif ID == 1:
            self.leftBottom = (100, 340, 70, 50)
            self.leftTop = (125, 140, 70, 50)
            self.top = (450, 79, 70, 50)
            self.rightTop = (780, 140, 70, 50)
            self.rightBottom = (810, 340, 70, 50)

    # player_order = [p1, p2, p3 ...], e.g: ["UTG", "MP", "CO", "BTN", "SB"] if hero is BB
    def Read(self, player_order):
        change_dir("fold")
        self.folded = []

        all_positions = [self.leftBottom, self.leftTop, self.top, self.rightTop, self.rightBottom]

        for p in range(0, len(player_order)):
            if py.locateOnScreen("folded.png", confidence=0.85, region=all_positions[p], grayscale=True) is not None:
                self.folded.append((player_order[p], False))
            else:
                self.folded.append((player_order[p], True))

        print("Folded is: " + str(self.folded))


if __name__ == "__main__":
    import time

    time.sleep(1)
    t1 = time.time()
    R = ReaderFolded(ID=0)
    R.Read(["UTG", "MP", "CO", "BTN", "SB"])
    print(time.time() - t1)

    print(R.folded)
