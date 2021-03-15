import os


def ParseNumberOfHands():
    os.chdir(r"C:\Users\Mathi\AppData\Local\PokerStars.DK\HandHistory\SoenderG")
    s = 0
    for f in os.listdir():
        with open(f) as file:
            try:
                for line in file.readlines():
                    if "PokerStars Zoom" in line:
                        s += 1
            except:
                print(f)



    return s

print(ParseNumberOfHands())

