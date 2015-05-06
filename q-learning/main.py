from __future__ import print_function, division
import sys

from flatland import FlatlandAgent
from flatlands import flatland_from_file
from gui import FlatlandGUI
from config import *

if __name__ == '__main__':
    txt = sys.argv[1]
    iterations = int(sys.argv[2])

    agent = FlatlandAgent(
        world=flatland_from_file(txt)
    )

    dt = INIT_TEMP / iterations

    replay = []

    update_q = lambda q, r, b: q + agent.lr * (r + agent.dr * b - q)
    best_q = lambda eaten, pos: max(agent.Q[eaten][pos][a] for a in agent.possible_actions)

    for i in xrange(iterations):
        print(i)
        while not agent.finished:
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

        if i == (iterations - 1):
            replay = agent.replay

        agent.reset_world()
        agent.temperature -= dt

    FlatlandGUI(agent, replay)
