from __future__ import print_function, division
from collections import defaultdict
from random import random, choice


class Q2(object):
    """
    Wrapping data structure for Q-Learning with a two levels of keys
    """
    def __init__(self):
        self.Q = defaultdict(lambda: defaultdict(float))

    def get(self, key):
        state, action = key
        return self.Q[state][action]

    def set(self, key, value):
        state, action = key
        self.Q[state][action] = value

    def best_action(self, part_key, actions):
        d = self.Q.get(part_key, None)
        if d is None:
            return None

        return max(actions, key=lambda action: d[action])

    def best_q(self, part_key):
        d = self.Q.get(part_key, None)
        if d is None:
            return 0.0

        return max(d[a] for a in d.keys())


class Q3(object):
    """
    Wrapping data structure for Q-Learning with a three levels of keys
    """
    def __init__(self):
        self.Q = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

    def get(self, key):
        (a, b), c = key
        return self.Q[a][b][c]

    def set(self, key, value):
        (a, b), c = key
        self.Q[a][b][c] = value

    def best_action(self, part_key, actions):
        a, b = part_key
        d = self.Q.get(a, None)
        if d is None:
            return None

        d = d.get(b, None)
        if d is None:
            return None

        return max(actions, key=lambda action: d[action])

    def best_q(self, part_key):
        a, b = part_key
        d = self.Q.get(a, None)
        if d is None:
            return 0

        d = d.get(b, None)
        if d is None:
            return 0

        return max(d[a] for a in d.keys())


class QLearningAgent(object):
    def __init__(self, Q, learning_rate, discount_rate, possible_actions, backup_x, temperature=1.0, delta_t=0.1):
        self.Q = Q

        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.initial_temperature = temperature
        self.temperature = temperature
        self.delta_t = delta_t

        self.possible_actions = possible_actions

        self.backup_x = backup_x
        self.memory = []

        self.explore = 0
        self.exploit = 0

    @property
    def state(self):
        raise NotImplementedError()

    @property
    def finished(self):
        raise NotImplementedError()

    @property
    def timeout(self):
        return False

    def score(self):
        raise NotImplementedError()

    def move(self, action):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()

    def select_action(self):
        exploit = self.Q.best_action(self.state, self.possible_actions)
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

    def update_q_value(self, value, reward, best_next):
        return value + self.learning_rate * (reward + self.discount_rate * best_next - value)

    def train(self, after_iteration=None):
        while self.temperature > 0:
            while not (self.finished or self.timeout):
                first_state = self.state
                action = self.select_action()
                reward = self.move(action)

                second_state = self.state
                self.memory_add((first_state, action, reward, second_state))

                for s1, action, reward, s2 in self.memory[::-1]:
                    key = (s1, action, )

                    val = self.Q.get(key)
                    self.Q.set(key, self.update_q_value(val, reward, self.Q.best_q(s2)))

            if after_iteration:
                after_iteration()

            self.reset()

            self.temperature -= self.delta_t
