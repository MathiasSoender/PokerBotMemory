import math
import random
from collections import deque


class Data:

    def __init__(self, pre_flop=False, fold_node = False):
        self.rewards = {}
        self.N = {}
        self.cum_rewards = {}
        self.split_probabilities = {}
        self.all_probabilities = []
        self.threshold = 500
        self.fold_node = False

        if not pre_flop:
            self.threshold = 150

        if fold_node:
            self.splits = [1]
            self.fold_node = True
            self.threshold = 1

        elif pre_flop:
            self.splits = list(range(1, 6))
        else:
            self.splits = list(range(1, 5))



        for split in self.splits:
            self.rewards[split] = deque([0.001])
            self.N[split] = 1
            self.cum_rewards[split] = 0
            self.split_probabilities[split] = 1 / max(self.splits) * (split - 1)
            self.all_probabilities.append(1 / max(self.splits) * (split - 1))

        self.split_length = len(self.splits)

    def find_split(self, probability):
        assigned_split = 1
        for split in reversed(self.splits):
            if self.split_probabilities[split] <= probability:
                assigned_split = split
                break
        return assigned_split

    def update_split(self, probability):
        if len(self.all_probabilities) > self.threshold:
            _ = self.all_probabilities.pop(random.randrange(len(self.all_probabilities)))

        else:
            self.all_probabilities.append(probability)

        parition_N = math.floor(len(self.all_probabilities) / self.split_length)
        self.all_probabilities = sorted(self.all_probabilities)
        for split in self.splits:
            self.split_probabilities[split] = self.all_probabilities[(split - 1) * parition_N: split * parition_N][0]

    def update_N(self, chosen_split):

        self.N[chosen_split] += 1

    def update(self, chosen_probability, pi, reward, siblings=None):
        # Round to save space
        reward = round(reward, 2)
        chosen_probability = round(chosen_probability, 5)
        chosen_split = self.find_split(chosen_probability)
        self.update_N(chosen_split)
        self.update_cummulative(chosen_split, pi)
        self.update_reward(chosen_split, reward)

        if not self.fold_node:
            self.update_split(chosen_probability)

        if siblings is not None:
            for sibling in siblings:
                sibling.data.decay_cummulative(sibling.data.find_split(chosen_probability))

    def update_cummulative(self, chosen_split, pi):
        self.cum_rewards[chosen_split] += pi

    def update_reward(self, chosen_split, reward):

        # Important: Must be >= as this then works with fold_nodes
        if len(self.rewards[chosen_split]) >= self.threshold:
            self.rewards[chosen_split].popleft()

        self.rewards[chosen_split].append(reward)

    # Decay siblings cum_strats in order to learn best strat faster.
    def decay_cummulative(self, chosen_split, factor=0.999):
        self.cum_rewards[chosen_split] *= factor





    def __str__(self):
        r = []
        for i in self.rewards.keys():
            r.append((i, round(sum(self.rewards[i]), 2)))

        return str(["Rewards: " + str(r), "N: " + str(self.N), "Split probabilities: " + str(self.split_probabilities)])
