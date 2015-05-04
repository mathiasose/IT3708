from __future__ import print_function, division
from copy import deepcopy

from flatland import FlatlandAgent
from flatlands import get_flatlands
from gui import FlatlandGUI


ITERATIONS = 100
P = 0.25

FLATLAND = get_flatlands()[0]
AGENT = FlatlandAgent(
    world=FLATLAND,
    learning_rate=0.5,
    discount_rate=0.5,
    p=0.25
)

if __name__ == '__main__':
    Q = AGENT.Q

    last_agent = None

    for _ in xrange(ITERATIONS):
        game = deepcopy(FLATLAND)
        game.agent = deepcopy(AGENT)

        game.agent.Q = Q

        Q = game.agent.Q

        while not game.agent.finished:
            first_state = game.agent.state
            action = game.agent.select_action()
            reward = game.agent.move(action)
            second_state = game.agent.state

            assert first_state != second_state

            a = game.agent.learning_rate
            g = game.agent.discount_rate
            best_next = max(Q[second_state, a] for a in game.agent.possible_actions)

            Q[first_state, action] += a * (reward + g * best_next - Q[first_state, action])

        print(game.agent.actions)
        last_agent = game.agent

    FlatlandGUI(deepcopy(AGENT), last_agent.actions)