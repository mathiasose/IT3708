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

    last_actions = None
    for i in xrange(iterations):
        while not agent.finished:
            eat1, pos1 = agent.state
            action = agent.select_action()
            reward = agent.move(action)

            eat2, pos2 = agent.state
            qs2 = agent.Q[eat2][pos2]
            best = max(qs2[a] for a in agent.possible_actions)

            qs1 = agent.Q[eat1][pos1]
            qs1[action] += agent.lr * (reward + agent.dr * best - qs1[action])

        print(i, end='\n' if i % 50 == 0 else ' ')
        last_actions = agent.actions

        agent.reset_world()
        agent.temperature -= dt

    FlatlandGUI(agent, last_actions)
