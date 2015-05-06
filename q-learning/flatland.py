from __future__ import print_function, division
from copy import deepcopy

from q_learning import QLearningAgent
from utils import *
from config import *


class FlatlandAgent(QLearningAgent):
    def __init__(self, world, learning_rate=LEARNING_RATE, discount_rate=DISCOUNT_RATE, temperature=INIT_TEMP):
        super(FlatlandAgent, self).__init__(
            learning_rate,
            discount_rate,
            temperature,
            possible_actions=ACTIONS,
            backup_x=BACKUP_X
        )

        self.world = world
        self.original = deepcopy(world)

        self.x, self.y = self.world.agent_initial_position

        self.food_eaten = set()
        self.poison_eaten = 0

        self.replay = []

    def reset_world(self):
        self.world = deepcopy(self.original)
        self.x, self.y = self.world.agent_initial_position

        self.food_eaten = set()
        self.poison_eaten = 0

        self.replay = []
        self.memory = []

    @property
    def position(self):
        return self.x, self.y

    @property
    def steps(self):
        return len(self.replay)

    @property
    def state(self):
        return tuple(sorted(self.food_eaten)), self.position

    @property
    def finished(self):
        return self.position == self.world.agent_initial_position and self.world.get_count_of_predicate(is_food) == 0

    def move(self, direction):
        self.replay.append(direction)

        self.x, self.y = self.world.absolute_coordinates(*tuple_add(self.position, DELTAS[direction]))

        if self.finished:
            return COMPLETION

        tile = self.world.get_tile(self.x, self.y)

        if is_food(tile):
            self.food_eaten.add(tile)
            self.world.set_tile(self.x, self.y, EMPTY)
            return REWARD
        elif is_poison(tile):
            self.world.set_tile(self.x, self.y, EMPTY)
            self.poison_eaten += 1
            return PENALTY
        else:
            return STEP

    @property
    def status(self):
        return '''
Food eaten:   {f}
Poison eaten: {p}
Steps:        {s}
        '''.format(
            f=len(self.food_eaten),
            p=self.poison_eaten,
            s=self.steps
        )


class Flatland(TorusWorld):
    def __init__(self, grid, agent_pos):
        TorusWorld.__init__(self, grid)
        self.agent_initial_position = agent_pos
