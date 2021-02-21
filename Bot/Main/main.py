from Bot.Main.mainController import mainController
import time
import random

def main(tables, run_time = 0):
    # Start queues and processes #
    start_time = time.time()
    controller = mainController(tables, testing=True)
    controller.start_processes()
    break_time = time.time() + random.randint(2500, 3500)

    while start_time + run_time > time.time():
        time.sleep(1)

        if time.time() > break_time:
            controller.pause()
            break_time = time.time() + random.randint(3000, 5000)



    # End processes #
    controller.stop_processes()







if __name__ == "__main__":
    main(tables = 1, run_time = 10000)


