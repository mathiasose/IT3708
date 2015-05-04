from __future__ import print_function, division

from q_learning import QLearningAgent
from utils import *


REWARD = 1
COMPLETION = 10
PENALTY = -5


class FlatlandAgent(QLearningAgent):
    def __init__(self, world, learning_rate, discount_rate, p):
        super(FlatlandAgent, self).__init__(learning_rate, discount_rate, p, possible_actions=ACTIONS)

        self.world = world
        self.x, self.y = self.world.agent_initial_position

        self.food_eaten = []
        self.actions = []

    @property
    def steps(self):
        return len(self.actions)

    @property
    def position(self):
        return self.x, self.y

    @property
    def finished(self):
        return self.world.get_count_of_predicate(is_food) == 0 and self.position == self.world.agent_initial_position

    @property
    def state(self):
        return tuple(self.food_eaten), self.position

    def move(self, direction):
        self.x, self.y = self.world.absolute_coordinates(*tuple_add(self.position, DELTAS[direction]))

        self.actions.append(direction)

        tile = self.world.get_tile(self.x, self.y)

        if is_food(tile):
            self.food_eaten.append(tile)
            self.world.set_tile(self.x, self.y, EMPTY)
            return REWARD
        elif is_poison(tile):
            self.world.set_tile(self.x, self.y, EMPTY)
            return PENALTY
        elif self.finished:
            return COMPLETION
        else:
            return 0


class Flatland(TorusWorld):
    def __init__(self, grid, agent_pos):
        TorusWorld.__init__(self, grid)
        self.agent_initial_position = agent_pos
