from __future__ import print_function, division
from math import sqrt
from time import time
import argparse

from flatland import FlatlandAgent
from scenarios import flatland_from_file
from gui import FlatlandGUI
from utils import manhattan_distance


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a Q-Learning Flatland scenario')
    parser.add_argument(
        '--scenario',
        nargs='?',
        type=str,
        required=True,
        help='Path to a .txt with a Flatland scenario'
    )
    parser.add_argument(
        '--iterations',
        nargs='?',
        type=int,
        required=True,
        help='Number of iterations to run'
    )
    parser.add_argument(
        '--temperature',
        nargs='?',
        type=float,
        default=1.0,
        help='Starting temperature'
    )
    parser.add_argument(
        '--backup',
        nargs='?',
        type=int,
        default=None,
        help='Defaults to a value proportionate to the world size'
    )
    parser.add_argument(
        '--plot',
        action='store_true'
    )
    args = parser.parse_args()

    flatland = flatland_from_file(args.scenario)

    backup_x = args.backup
    if args.backup is None:
        backup_x = int(sqrt(manhattan_distance((0, 0), (flatland.w, flatland.h))))

    agent = FlatlandAgent(
        world=flatland,
        step_limit=flatland.w * flatland.h,
        backup_x=backup_x,
        temperature=args.temperature,
        delta_t=args.temperature / args.iterations
    )

    ideal_temp = []
    experienced_temp = []

    start = time()

    def after():
        e = agent.explore / agent.steps

        ideal_temp.append(agent.temperature)
        experienced_temp.append(e)

        print(
            round(agent.temperature, 3),
            round(e, 3),
            agent.steps,
            len(agent.food_eaten),
            agent.poison_eaten
        )

    agent.train(after)

    finish = time()

    print("Time: {}s".format(finish - start))

    if args.plot:
        from plot import plot_temperatures
        plot_temperatures(ideal_temp, experienced_temp)

    agent.temperature = -1
    FlatlandGUI(agent)

