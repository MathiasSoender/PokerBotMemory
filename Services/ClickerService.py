import time


def ClickMaster(Click_channels, Click_queue):
    # Grab the first request for lock
    while True:
        res = Click_queue.get()
        if res.request == "get":
            Click_channels[res.ID].put(200)
            time.sleep(1)
            Click_channels[res.ID].get()

        elif res.request == "stop":
            return