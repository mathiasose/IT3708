import random
from adult_selection import full_generational_replacement, over_production
from evo_alg import run_simulation, plot_simulation_results
from mate_selection import fitness_proportionate, sigma_scaled, tournament, ranked
from problems import one_max, lolz, surprising_sequences
from reproduction import mutate_bit_genome, mix, splice, mutate_string_genome


LOG = True
PLOT = True

PROBLEMS = (one_max, lolz, surprising_sequences)

ONE_MAX = {
    'problem': one_max,
    'problem_parameters': {
        'population_size': 600,
        'genome_size': 40,
        'target_phenotype': list(random.getrandbits(1) for _ in range(40))
    },

    'adult_selection_method': full_generational_replacement,

    'mate_selection_method': fitness_proportionate,

    'crossover_method': mix,
    'crossover_rate': 0.9,

    'mutation_method': mutate_bit_genome,
    'mutation_rate': 0.01,

    'stop': {
        'fitness': 1.0,
        'generation': 100
    }
}

LOLZ = {
    'problem': lolz,
    'problem_parameters': {
        'population_size': 600,
        'genome_size': 40,
        'z': 21,
    },

    'adult_selection_method': full_generational_replacement,

    'mate_selection_method': tournament,
    'mate_selection_args': {
        'group_size': 20,
        'epsilon': 0.10
    },

    'crossover_method': mix,
    'crossover_rate': 0.9,

    'mutation_method': mutate_bit_genome,
    'mutation_rate': 0.01,

    'stop': {
        'fitness': 1.0,
        'generation': None
    }
}

LOCALLY_SURPRISING = {
    'problem': surprising_sequences,
    'problem_parameters': {
        'char_set_size': 40,
        'population_size': 50,
        'genome_size': 400,
        'local': True
    },

    'adult_selection_method': over_production,

    'mate_selection_method': sigma_scaled,

    'crossover_method': splice,
    'crossover_rate': 0.9,

    'mutation_method': mutate_string_genome,
    'mutation_rate': 0.5,

    'stop': {
        'fitness': 1.0,
        'generation': 100
    },

    'plot_sigmas': False
}

GLOBALLY_SURPRISING = {
    'problem': surprising_sequences,
    'problem_parameters': {
        'char_set_size': 20,
        'population_size': 200,
        'genome_size': 45,
        'local': False
    },

    'adult_selection_method': full_generational_replacement,

    'mate_selection_method': ranked,

    'crossover_method': splice,
    'crossover_rate': 0.25,

    'mutation_method': mutate_string_genome,
    'mutation_rate': 0.01,

    'stop': {
        'fitness': 1.0,
        'generation': None
    },

    'plot_sigmas': False
}

SIMULATIONS = [
    # ONE_MAX,
    LOLZ,
    # LOCALLY_SURPRISING,
    # s
]

if __name__ == "__main__":
    for simulation in SIMULATIONS:
        results = run_simulation(simulation)
        plot_simulation_results(results)
