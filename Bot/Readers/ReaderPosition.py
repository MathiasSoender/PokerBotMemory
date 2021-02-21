#Works

import pyautogui as py

from Bot.Readers.misc import change_dir


class ReaderPosition:
    def __init__(self, ID):

        self.Position = None
        self.order = []


        if ID == 0:
            self.regions = [("BTN", (371, 431, 45, 45)), ("SB", (690, 395, 45, 45)), ("BB", (735, 240, 45, 45)),
                            ("UTG", (504, 187, 45, 45)), ("CO", (187, 328, 45, 45)), ("MP", (288, 190, 45, 45))]


        elif ID == 1:
            self.regions = [("BTN", (371, 431, 45, 45)), ("SB", (690, 395, 45, 45)), ("BB", (735, 240, 45, 45)),
                            ("UTG", (504, 187, 45, 45)), ("CO", (187, 328, 45, 45)), ("MP", (288, 190, 45, 45))]

    def Read(self):
        change_dir("position")

        for pos, region in self.regions:
            if py.locateOnScreen("button.png", confidence=0.9, region=region) is not None:
                self.Position = pos
                self.find_order()
                break



        print("Position: " + str(self.Position))

    def find_order(self):
        std_order = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        self.order = std_order[std_order.index(self.Position)+1:] + std_order[:std_order.index(self.Position)]





if __name__ == "__main__":
    import time
    time.sleep(1)
    t1 = time.time()
    R = ReaderPosition(ID=0)
    R.Read()
    print(time.time() - t1)


