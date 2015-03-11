from datetime import datetime

from adult_selection import full_generational_replacement
from evo_alg import run_simulation
from mate_selection import fitness_proportionate
from problems import one_max
from reproduction import mix, mutate_bit_genome


SIMULATIONS = [
    {
        'problem': one_max,
        'problem_parameters': {
            'population_size': 200,
            'genome_size': 40,
        },

        'adult_selection_method': full_generational_replacement,

        'mate_selection_method': fitness_proportionate,

        'crossover_method': mix,
        'crossover_rate': 0.25,

        'mutation_method': mutate_bit_genome,
        'mutation_rate': 0.1,

        'stop': {
            'fitness': 1.0,
            'generation': None
        }
    },
    {
        'problem': one_max,
        'problem_parameters': {
            'population_size': 300,
            'genome_size': 40,
        },

        'adult_selection_method': full_generational_replacement,

        'mate_selection_method': fitness_proportionate,

        'crossover_method': mix,
        'crossover_rate': 0.25,

        'mutation_method': mutate_bit_genome,
        'mutation_rate': 0.1,

        'stop': {
            'fitness': 1.0,
            'generation': None
        }
    },
    {
        'problem': one_max,
        'problem_parameters': {
            'population_size': 400,
            'genome_size': 40,
        },

        'adult_selection_method': full_generational_replacement,

        'mate_selection_method': fitness_proportionate,

        'crossover_method': mix,
        'crossover_rate': 0.25,

        'mutation_method': mutate_bit_genome,
        'mutation_rate': 0.1,

        'stop': {
            'fitness': 1.0,
            'generation': None
        }
    },
    {
        'problem': one_max,
        'problem_parameters': {
            'population_size': 500,
            'genome_size': 40,
        },

        'adult_selection_method': full_generational_replacement,

        'mate_selection_method': fitness_proportionate,

        'crossover_method': mix,
        'crossover_rate': 0.25,

        'mutation_method': mutate_bit_genome,
        'mutation_rate': 0.1,

        'stop': {
            'fitness': 1.0,
            'generation': None
        }
    }
]


def simulate_n_times(simulation, n):
    results = [run_simulation(simulation, log=False) for _ in range(n)]

    print(
        simulation['problem_parameters']['population_size'],
        sum(r['generation_number'] < 100 for r in results)
    )

    return {
        'data': list((r['generation_number'] for r in results)),
        'label': simulation['problem_parameters']['population_size']
    }


N = 100
datasets = [simulate_n_times(s, N) for s in SIMULATIONS]

import matplotlib.pyplot as plt

n, bins, patches = plt.hist(
    [x['data'] for x in datasets],
    bins=range(0, 150, 10),
    label=["Population {}".format(x['label']) for x in datasets]
)
plt.xlabel('Generations')
plt.ylabel('Occurrences')
plt.legend()
plt.savefig('../report/img/{}.png'.format(datetime.now()))
plt.show()
