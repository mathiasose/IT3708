from math import sqrt
from pprint import pprint

from plot import plot_results
from reproduction import crossover
from utils import f


LOG = True


def run_simulation(simulation, log=LOG):
    problem = simulation.get('problem')
    problem_parameters = simulation.get('problem_parameters', {})
    population_size = problem_parameters.get('population_size')
    adult_selection = simulation.get('adult_selection_method')
    mate_selection = simulation.get('mate_selection_method')
    mate_selection_args = simulation.get('mate_selection_args', {})
    crossover_rate = simulation.get('crossover_rate')
    crossover_method = simulation.get('crossover_method')
    n_children = simulation.get('n_children', 2)
    mutation_method = simulation.get('mutation_method')
    mutation_chance = simulation.get('mutation_rate')
    stop = simulation.get('stop', {})
    stop_fitness = stop.get('fitness')
    stop_generation = stop.get('generation')

    # STEP 0: Initialize child genotype population
    population = []
    children = [{'genotype': genotype} for genotype in problem.generate_initial_population(**problem_parameters)]

    average_fitnesses = []
    sigmas = []
    best_fitnesses = []

    if log:
        print("Start simulation")
        pprint(simulation, indent=2)

    generation_number = 0
    while True:
        generation_number += 1

        # STEP 1: Development: Generate Phenotypes from Genotypes
        for individual in children:
            individual['phenotype'] = problem.geno_to_pheno(individual['genotype'], **problem_parameters)

        # STEP 2: Test Fitness of Phenotypes
        for individual in children:
            individual['fitness'] = problem.fitness_evaluation(individual['phenotype'], **problem_parameters)

        # STEP 3: Adult Selection
        population = adult_selection(
            old_population=population,
            children=children,
            m=population_size
        )
        children = []

        total_fitness = sum(f(x) for x in population)
        average_fitness = total_fitness / population_size
        deviations = ((f(x) - average_fitness) ** 2 for x in population)
        sigma = sqrt(sum(deviations) / population_size)

        best_individual = max(population, key=f)

        # STEP 4: Parent Selection
        pairs = mate_selection(
            population=population,
            sigma=sigma,
            average_fitness=average_fitness,
            **mate_selection_args
        )

        # STEP 5: Reproduction
        mutation_func = lambda x: mutation_method(x, p=mutation_chance, **problem_parameters)
        for pair in pairs:
            new_genotypes = crossover(
                *pair,
                crossover_rate=crossover_rate,
                method=crossover_method,
                n_children=n_children
            )

            # STEP 5.5: Mutation
            mutated_genotypes = map(mutation_func, new_genotypes)

            children.extend({'genotype': g} for g in mutated_genotypes)

        if log:
            print(
                '''
GENERATION {n}
AVG:\t{avg_fitness}
STD:\t{sigma}
BEST:\t{best_fitness}
{best_phenotype}
                '''
                .format(
                    n=generation_number,
                    avg_fitness=average_fitness,
                    sigma=sigma,
                    best_phenotype=problem.phenotype_representation(
                        best_individual['phenotype'],
                        **problem_parameters
                    ),
                    best_fitness=best_individual['fitness']
                )
            )

        average_fitnesses.append(average_fitness)
        sigmas.append(sigma)
        best_fitnesses.append(best_individual['fitness'])

        if stop_fitness and f(best_individual) >= stop_fitness:
            if log:
                print('FITNESS STOP')
            break
        elif stop_generation and generation_number >= stop_generation:
            if log:
                print('GENERATION STOP')
            break

            # Begin Next Generation

    return {
        'simulation': simulation,
        'generation_number': generation_number,
        'average_fitnesses': average_fitnesses,
        'sigmas': sigmas,
        'best_fitnesses': best_fitnesses,
        'final_population': population,
        'final_best_individual': best_individual
    }


def plot_simulation_results(simulation_results, title=None, savefig=None):
    x = list(range(1, simulation_results['generation_number'] + 1))

    datasets = [
        {
            'y': simulation_results['average_fitnesses'],
            'x': x,
            'label': 'Average fitness'
        },
        {
            'y': simulation_results['best_fitnesses'],
            'x': x,
            'label': 'Best fitness'
        }
    ]

    if simulation_results['simulation'].get('plot_sigmas', True):
        datasets.append({
            'y': simulation_results['sigmas'],
            'x': x,
            'label': r'$\sigma$'
        })

    title = title or "{} {} generations".format(
        simulation_results['simulation']['problem'].NAME,
        simulation_results['generation_number']
    )

    plot_results(datasets, xlabel='generations', ylabel='fitness', title=title, savefig=savefig)
