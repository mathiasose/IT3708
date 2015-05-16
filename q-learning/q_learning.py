from __future__ import print_function, division
from collections import defaultdict
from random import random, choice


class QLearningAgent(object):
    def __init__(self, learning_rate, discount_rate, possible_actions, backup_x, temperature=1.0, dt=0.1):
        self.Q = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        self.lr = learning_rate
        self.dr = discount_rate
        self.temperature = temperature
        self.dt = dt

        self.possible_actions = possible_actions

        self.backup_x = backup_x
        self.memory = []

        self.explore = 0
        self.exploit = 0

    @property
    def state(self):
        raise NotImplementedError

    @property
    def finished(self):
        raise NotImplementedError

    @property
    def timeout(self):
        return False

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
            self.explore += 1
            return choice(self.possible_actions)
        else:
            self.exploit += 1
            return exploit

    def memory_add(self, x):
        self.memory.append(x)

        if len(self.memory) > (self.backup_x + 1):
            self.memory.pop(0)

    def update_q(self, q, r, b):
        return q + self.lr * (r + self.dr * b - q)

    def best_q(self, eaten, pos):
        d = self.Q.get(eaten, None)
        if d is None:
            return 0

        d = d.get(pos, None)
        if d is None:
            return 0

        return max(d[a] for a in d.keys())

    def train(self, after_iteration=None):
        while self.temperature > 0:
            while not (self.finished or self.timeout):
                first_state = self.state
                action = self.select_action()
                reward = self.move(action)

                second_state = self.state
                self.memory_add((first_state, action, reward, second_state))

                for s1, action, reward, s2 in self.memory[::-1]:
                    e1, p1 = s1
                    e2, p2 = s2

                    val = self.Q[e1][p1][action]
                    self.Q[e1][p1][action] = self.update_q(val, reward, self.best_q(e2, p2))

            if after_iteration:
                after_iteration()

            self.temperature -= self.dt
