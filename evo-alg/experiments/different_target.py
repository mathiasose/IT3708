import datetime
import random

from adult_selection import full_generational_replacement
from experiments.average_n_runs import average_n_runs
from mate_selection import fitness_proportionate
from plot import plot_results
from problems import one_max
from reproduction import mutate_bit_genome, mix


simulation = {
    'problem': one_max,
    'problem_parameters': {
        'population_size': 600,
        'genome_size': 40,
    },

    'adult_selection_method': full_generational_replacement,

    'mate_selection_method': fitness_proportionate,
    'mate_selection_args': {
        'group_size': 20,
        'epsilon': 0.01,
    },

    'crossover_method': mix,
    'crossover_rate': 0.9,

    'mutation_method': mutate_bit_genome,
    'mutation_rate': 0.01,

    'stop': {
        'fitness': None,
        'generation': 100
    }
}

G = 100
N = 100
X = list(range(1, G + 1))
results = [
    {
        'x': X,
        'y': average_n_runs(simulation, N, G)['average_fitnesses'],
        'label': "All 1s"
    }
]

target = list(random.getrandbits(1) for _ in range(40))
simulation.update({'target_phenotype': target})
results.append({
    'x': X,
    'y': average_n_runs(simulation, N, G)['average_fitnesses'],
    'label': "Random string"
})

plot_results(
    datasets=results,
    savefig="../report/img/{}.png".format(datetime.datetime.now()),
    xlabel="Generation number",
    ylabel="Fitness",
    title="Different target strings",
    ncol=2
)
