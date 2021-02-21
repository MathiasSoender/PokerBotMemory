import time


class timer:
    def __init__(self, timers):
        self.all_timers = dict()
        self.values = dict()
        self.total_time = time.time()
        self.round_time = time.time()
        for t in timers:
            self.values[t] = 0

    def round_timer(self):
        print("time since last: " + str(time.time() - self.round_time))
        self.round_time = time.time()

    def start_timer(self, t):
        self.all_timers[t] = time.time()

    def end_timer(self, t):
        self.values[t] += time.time() - self.all_timers[t]

    def __str__(self):
        out = []
        tot = float(time.time() - self.total_time + 0.0001)
        for val in self.values.keys():
            out.append(
                "Timer: " + str(val) + " taken: " + str(self.values[val]) + "s " + str(self.values[val] / (tot)) + "%")

        return str(out) + "total time: " + str(tot)
