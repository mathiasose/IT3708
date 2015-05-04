from __future__ import print_function, division

import os

from flatland import Flatland


def flatland_from_file(path):
    with open(path) as f:
        w, h, x, y, n = map(int, f.readline().strip().split(' '))

        grid = [list(map(int, line.strip().split(' '))) for line in f.readlines()]

        return Flatland(grid, (x, y))


def get_flatlands():
    directory = os.path.dirname(__file__)
    return [flatland_from_file(os.path.join(directory, f)) for f in sorted(os.listdir(directory)) if '.txt' in f]
