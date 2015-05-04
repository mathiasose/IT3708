from __future__ import division

AGENT_DIRECTIONS = NORTH, WEST, SOUTH, EAST = 'N', 'W', 'S', 'E'
NOOP = 'NOOP'

DELTAS = {
    NORTH: (0, -1),
    WEST: (-1, 0),
    SOUTH: (0, 1),
    EAST: (1, 0),
    NOOP: (0, 0)
}

is_start = lambda x: x == -2
is_food = lambda x: x > 0
is_poison = lambda x: x == -1

EMPTY = 0
is_empty = lambda x: x == EMPTY or is_start(x)

ACTIONS = AGENT_DIRECTIONS


def tuple_add(*tuples):
    return tuple(map(sum, zip(*tuples)))


class TorusWorld:
    def __init__(self, grid):
        self.w, self.h = len(grid[0]), len(grid)
        self.grid = grid

    def get_tile(self, x, y):
        return self.grid[y][x]

    def set_tile(self, x, y, value):
        self.grid[y][x] = value

    def absolute_coordinates(self, x, y):
        return x % self.w, y % self.h

    def get_count_of_value(self, value):
        return sum(sum(cell == value for cell in row) for row in self.grid)

    def get_count_of_predicate(self, predicate):
        return sum(sum(predicate(cell) for cell in row) for row in self.grid)

    def get_coordinates_of_value(self, value):
        return list((x, y) for x in xrange(self.w) for y in xrange(self.w) if self.get_tile(x, y) == value)
