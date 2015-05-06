from __future__ import print_function, division
from math import sqrt
import sys

from flatland import FlatlandAgent
from flatlands import flatland_from_file
from gui import FlatlandGUI

from time import time

if __name__ == '__main__':
    txt = sys.argv[1]
    iterations = int(sys.argv[2])

    flatland = flatland_from_file(txt)
    area = flatland.w * flatland.h

    agent = FlatlandAgent(
        world=flatland,
        timeout=area,
        backup_x=int(sqrt(area))
    )

    dt = 1.0 / iterations

    replay = []

    update_q = lambda q, r, b: q + agent.lr * (r + agent.dr * b - q)
    best_q = lambda eaten, pos: max(agent.Q[eaten][pos][a] for a in agent.possible_actions)

    start = time()

    for i in xrange(iterations):
        while (not agent.finished) and (not agent.timeout or agent.steps < agent.timeout):
            s1 = agent.state
            action = agent.select_action()
            reward = agent.move(action)

            s2 = agent.state
            agent.memory_add((s1, action, reward, s2))

            for s1, action, reward, s2 in agent.memory[::-1]:
                e1, p1 = s1
                e2, p2 = s2

                val = agent.Q[e1][p1][action]
                agent.Q[e1][p1][action] = update_q(val, reward, best_q(e2, p2))

        print(i, agent.steps, len(agent.food_eaten), agent.poison_eaten)
        if i == (iterations - 1):
            replay = agent.replay

        agent.reset_world()
        agent.temperature -= dt

    finish = time()

    print("Time: {}s".format(finish - start))

    agent.temperature = -1
    FlatlandGUI(agent)
