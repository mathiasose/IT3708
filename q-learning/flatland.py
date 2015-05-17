from __future__ import print_function, division
from copy import deepcopy

from q_learning import QLearningAgent, Q3
from utils import *
from config import *


class FlatlandAgent(QLearningAgent):
    def __init__(self,
                 world,
                 learning_rate=LEARNING_RATE,
                 discount_rate=DISCOUNT_RATE,
                 step_limit=0,
                 backup_x=BACKUP_X,
                 temperature=1.0,
                 delta_t=0.1
    ):
        super(FlatlandAgent, self).__init__(
            Q=Q3(),
            learning_rate=learning_rate,
            discount_rate=discount_rate,
            possible_actions=ACTIONS,
            backup_x=backup_x,
            temperature=temperature,
            delta_t=delta_t
        )

        self.world = world
        self.original = deepcopy(world)

        self.x, self.y = self.world.agent_initial_position

        self.food_eaten = set()
        self.poison_eaten = 0

        self.step_limit = step_limit

        self.steps = 0

    def reset(self):
        self.world = deepcopy(self.original)
        self.x, self.y = self.world.agent_initial_position

        self.food_eaten = set()
        self.poison_eaten = 0

        self.memory = []

        self.steps = 0

        self.explore = 0
        self.exploit = 0

    @property
    def position(self):
        return self.x, self.y

    @property
    def state(self):
        return tuple(sorted(self.food_eaten)), self.position

    @property
    def finished(self):
        return self.position == self.world.agent_initial_position and self.world.get_count_of_predicate(is_food) == 0

    @property
    def timeout(self):
        return self.step_limit and self.steps >= self.step_limit

    def move(self, direction):
        self.steps += 1

        self.x, self.y = self.world.absolute_coordinates(*tuple_add(self.position, DELTAS[direction]))

        if self.finished:
            return COMPLETION

        tile = self.world.get_tile(self.x, self.y)

        if is_food(tile):
            self.food_eaten.add(tile)
            self.world.set_tile(self.x, self.y, EMPTY)
            return REWARD
        elif is_poison(tile):
            self.poison_eaten += 1
            self.world.set_tile(self.x, self.y, EMPTY)
            return PENALTY
        else:
            return STEP


class Flatland(TorusWorld):
    def __init__(self, grid, agent_pos):
        TorusWorld.__init__(self, grid)
        self.agent_initial_position = agent_pos
