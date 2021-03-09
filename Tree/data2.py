import math
import random


class Data:
    __slots__ = 'N', 'split_probabilities', 'all_probabilities', 'c_reward', 'fold_node', 'splits'

    def __init__(self, pre_flop=False, fold_node=False):
        self.N = []
        self.split_probabilities = []
        self.all_probabilities = []
        self.c_reward = []

        self.fold_node = False

        if fold_node:
            self.splits = [0]
            self.fold_node = True

        elif pre_flop:
            self.splits = list(range(0, 5))
        else:
            self.splits = list(range(0, 5))

        for split in self.splits:
            self.c_reward.append(0)
            self.N.append(0)
            if fold_node:
                self.split_probabilities.append(0)
                self.all_probabilities.append(0)
            else:
                self.split_probabilities.append(1 / max(self.splits) * split)
                self.all_probabilities.append(1 / max(self.splits) * split)

    def __str__(self):

        return str(["Rewards: " + str(self.c_reward), "N: " + str(self.N),
                    "Split probabilities: " + str(self.split_probabilities)])

    def find_split(self, probability):
        assigned_split = 0
        for split in reversed(self.splits):
            if self.split_probabilities[split] <= probability:
                assigned_split = split
                break
        return assigned_split

    def update_split(self, probability):
        if self.fold_node:
            threshold = 1
        else:
            threshold = 200

        if len(self.all_probabilities) > threshold:
            _ = self.all_probabilities.pop(random.randrange(len(self.all_probabilities)))

        else:
            self.all_probabilities.append(probability)

        parition_N = math.floor(len(self.all_probabilities) / len(self.splits))
        self.all_probabilities = sorted(self.all_probabilities)

        for split in self.splits:
            self.split_probabilities[split] = self.all_probabilities[split * parition_N: (split + 1) * parition_N][0]

    def update_N(self, chosen_split):
        self.N[chosen_split] += 1

    def update(self, chosen_probability, reward):
        # Round to save space
        reward = round(reward, 2)
        chosen_probability = round(chosen_probability, 5)
        chosen_split = self.find_split(chosen_probability)
        self.update_reward(chosen_split, reward)
        self.update_N(chosen_split)

        if not self.fold_node:
            self.update_split(chosen_probability)

    def update_reward(self, chosen_split, reward):

        if self.fold_node:
            self.c_reward[chosen_split] = reward
        else:
            self.c_reward[chosen_split] = self.c_reward[chosen_split] * 0.995 + reward
