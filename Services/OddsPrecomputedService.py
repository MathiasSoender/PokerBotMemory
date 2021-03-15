import os

from Misc.Precomputed import precomputed_odds


def pre_computed_service(Pre_computed_queue, channels, is_bot = False, path = "pre_odds"):
    r = 0
    os.chdir("..")
    if is_bot:
        os.chdir("..")
    os.chdir("Simulator_main")

    pre_computed = precomputed_odds()
    while True:
        res = Pre_computed_queue.get()

        if res.request == "process":
            odds = pre_computed.find_odds(res.hand, res.name, res.opponents)

            if odds is None:
                channels[res.ID].put((False, 0))
            else:
                channels[res.ID].put((True, odds))

        elif res.request == "add":
            pre_computed.add(res.hand, res.name, res.opponents, res.odds)

        elif res.request == "stop":
            break
        r += 1

        if (r + 1) % 100000 == 0:
            pre_computed.to_object("pre_odds")

    pre_computed.to_object("pre_odds")
    print("pre_computed service shutdown")

if __name__ == "__main__":
    import multiprocessing as mp
    asd = mp.Queue()
    ps = mp.Process(target=pre_computed_service,
                                           args=(asd, None))
    ps.start()
