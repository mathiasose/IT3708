from __future__ import print_function, division
from collections import defaultdict
from random import random, choice


class QLearningAgent(object):
    def __init__(self, learning_rate, discount_rate, possible_actions, backup_x):
        self.Q = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        self.lr = learning_rate
        self.dr = discount_rate
        self.temperature = 1.0

        self.possible_actions = possible_actions

        self.backup_x = backup_x
        self.memory = []

    @property
    def state(self):
        raise NotImplementedError

    def score(self):
        raise NotImplementedError

    def move(self, action):
        raise NotImplementedError

    def best_action(self, state):
        eaten, pos = state
        qs = self.Q[eaten][pos]
        if sum(qs.values()) == 0:
            return None

        return max(self.possible_actions, key=lambda a: qs[a])

    def select_action(self):
        exploit = self.best_action(self.state)
        if exploit is None or random() <= self.temperature:
            return choice(self.possible_actions)
        else:
            return exploit

    def memory_add(self, x):
        self.memory.append(x)

        if len(self.memory) > self.backup_x:
            self.memory.pop(0)
