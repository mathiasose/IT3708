from adult_selection import ADULT_SELECTION_METHODS

from evo_alg import run_simulation, plot_simulation_results
from mate_selection import MATE_SELECTION_METHODS
from problems.simulations import SIMULATIONS, PROBLEMS
from reproduction import CROSSOVER_METHODS, MUTATION_METHODS


def int_choice(hi, lo=0):
    while True:
        try:
            n = int(input("Choice [{}-{}]:\t".format(lo, hi)))
        except ValueError:
            continue

        if n > hi or n < lo:
            continue

        return n


def give_choice(options):
    for i, option in enumerate(options):
        print("({})\t{}".format(i, option))

    n = int_choice(hi=len(options))

    return options[n]


if __name__ == "__main__":
    while True:
        print("Choose a preset:")
        for i, k in enumerate(SIMULATIONS):
            print("({})\t{}\t{}".format(i, k['problem'].NAME, k['problem_parameters']))

        n = int_choice(hi=len(SIMULATIONS) - 1)
        simulation = SIMULATIONS[n]

        while True:
            choices = set(simulation.keys())
            choices.update(set(simulation['problem_parameters'].keys()))
            choices.update(set(simulation['stop'].keys()))
            choices.remove('problem_parameters')
            choices.remove('stop')
            choices = sorted(list(choices))

            def getter(key):
                if key in simulation:
                    return simulation[key]

                if key in simulation['problem_parameters']:
                    return simulation['problem_parameters'][key]

                if key in simulation['stop']:
                    return simulation['stop'][key]

            def setter(key, value):
                if key in simulation:
                    simulation[key] = value

                if key in simulation['problem_parameters']:
                    simulation['problem_parameters'][key] = value

                if key in simulation['stop']:
                    simulation['stop'][key] = value

            print("\nChange parameters?")
            for i, k in enumerate(choices):
                print("({})\t{} = {}".format(i, k, getter(k)))

            run_n = len(choices)
            print("({})\t{}".format(run_n, "Run simulation"))

            n = int_choice(hi=run_n)
            if n == run_n:
                break

            selection = choices[n]

            attr_options = {
                'problem': PROBLEMS,
                'adult_selection_method': ADULT_SELECTION_METHODS,
                'crossover_method': CROSSOVER_METHODS,
                'mutation_method': MUTATION_METHODS,
                'mate_selection_method': MATE_SELECTION_METHODS
            }

            if selection in attr_options.keys():
                setter(selection, give_choice(attr_options[selection]))
                continue

            user_in = input("{}:\t".format(selection))

            if type(getter(selection)) == int:
                user_in = int(user_in)
            elif type(getter(selection)) == float:
                user_in = float(user_in)
            elif type(getter(selection)) == bool:
                user_in = bool(user_in)

            setter(selection, user_in)

        print()
        results = run_simulation(simulation)
        plot_simulation_results(results)