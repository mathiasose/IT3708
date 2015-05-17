from __future__ import print_function, division
from copy import deepcopy
from math import sqrt
from time import time

from flatland import FlatlandAgent
from q_learning import Q2, Q3
from scenarios import flatland_from_file
from utils import manhattan_distance

ITERATIONS = 5000

TEMPERATURE = 1.0

N = 1

if __name__ == '__main__':
    times = {
        2: [],
        3: []
    }
    flatland = flatland_from_file('../scenarios/5-even-bigger.txt')
    backup_x = int(sqrt(manhattan_distance((0, 0), (flatland.w, flatland.h))))

    for i in xrange(N):
        print(2, i)
        agent = FlatlandAgent(
            world=deepcopy(flatland),
            step_limit=flatland.w * flatland.h,
            backup_x=backup_x,
            temperature=TEMPERATURE,
            delta_t=TEMPERATURE / ITERATIONS
        )
        agent.Q = Q2()

        start = time()
        agent.train()
        finish = time()

        times[2].append(finish - start)

    for i in xrange(N):
        print(3, i)
        agent = FlatlandAgent(
            world=deepcopy(flatland),
            step_limit=flatland.w * flatland.h,
            backup_x=backup_x,
            temperature=TEMPERATURE,
            delta_t=TEMPERATURE / ITERATIONS
        )
        agent.Q = Q3()

        start = time()
        agent.train()
        finish = time()

        times[3].append(finish - start)

    print(times)
    print('Q2 avg', sum(times[2]) / 10)
    print('Q3 avg', sum(times[3]) / 10)