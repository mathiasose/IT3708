from __future__ import print_function, division
from collections import defaultdict
from copy import deepcopy

from flatland import FlatlandAgent
from flatlands import get_flatlands
from gui import FlatlandGUI


LEARNING_RATE = 0.1
DISCOUNT_RATE = 0.1

ITERATIONS = 1000
INIT_TEMP = 1.0
DELTA_TEMP = INIT_TEMP / ITERATIONS

FLATLAND = get_flatlands()[1]

if __name__ == '__main__':
    last_agent = None

    for i in xrange(ITERATIONS):
        game = deepcopy(FLATLAND)
        game.agent = FlatlandAgent(
            Q=defaultdict(int) if last_agent is None else last_agent.Q,
            world=game,
            learning_rate=LEARNING_RATE,
            discount_rate=DISCOUNT_RATE,
            temperature=INIT_TEMP - i * DELTA_TEMP
        )

        while not game.agent.finished:
            first_state = game.agent.state
            action = game.agent.select_action()
            reward = game.agent.move(action)
            second_state = game.agent.state

            assert first_state != second_state

            a = game.agent.learning_rate
            g = game.agent.discount_rate
            best_next = max(game.agent.Q[second_state, a] for a in game.agent.possible_actions)

            game.agent.Q[first_state, action] += a * (reward + g * best_next - game.agent.Q[first_state, action])

        print(i, game.agent.actions)
        last_agent = game.agent

    FlatlandGUI(
        FlatlandAgent(
            Q=last_agent.Q,
            world=deepcopy(FLATLAND),
            learning_rate=LEARNING_RATE,
            discount_rate=DISCOUNT_RATE,
            temperature=INIT_TEMP
        ),
        last_agent.actions
    )
