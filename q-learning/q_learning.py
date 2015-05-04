from __future__ import print_function, division
from collections import defaultdict
from random import random, choice


class QLearningAgent(object):
    def __init__(self, learning_rate, discount_rate, p, possible_actions):
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.possible_actions = possible_actions
        self.p = p

        self.Q = defaultdict(int)

    @property
    def state(self):
        raise NotImplementedError

    def best_action(self):
        return max(self.possible_actions, key=lambda a: self.Q[self.state, a])

    def select_action(self):
        if random() < self.p:
            return choice(self.possible_actions)

        return self.best_action()

    def run(self):
        raise NotImplementedError()