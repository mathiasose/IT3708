from __future__ import print_function, division

from flatland import Flatland


def flatland_from_file(path):
    with open(path) as f:
        w, h, x, y, n = map(int, f.readline().strip().split(' '))

        grid = [list(map(int, line.strip().split(' '))) for line in f.readlines()]

        return Flatland(grid, (x, y))
