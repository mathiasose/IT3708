from __future__ import print_function, division
from math import exp
from random import random, choice


class QLearningAgent(object):
    def __init__(self, Q, learning_rate, discount_rate, temperature, possible_actions):
        self.Q = Q

        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.temperature = temperature

        self.possible_actions = possible_actions

    @property
    def state(self):
        raise NotImplementedError

    def best_action(self):
        return max(self.possible_actions, key=lambda a: self.Q[self.state, a])

    def select_action(self):
        best_action = self.best_action()

        q = self.Q[self.state, best_action]

        try:
            f = exp(-q / self.temperature)
            p_val = min(1.0, f)
        except OverflowError:
            p_val = 1.0

        if random() > p_val:
            return best_action
        else:
            return choice(self.possible_actions)

    def run(self):
        raise NotImplementedError()
