import random

from utils import f


def roulette(population, scaling_func, **kwargs):
    """
    an individual may be part of multiple pairs,
    but not the same pairing multiple times
    nor in a pair with itself
    """

    def generate_roulette():
        """
        returns a function that when called will select an indidividual from the population
        based on the normalized fitness value as decided by fitness_func
        """

        scaled_fitnesses = list((x, scaling_func(x)) for x in population)

        scaled_fitnesses.sort(key=lambda x: x[1])

        roulette = dict()

        current_sum = 0.0
        for ind, p in scaled_fitnesses:
            next_sum = current_sum + p
            roulette[(current_sum, next_sum)] = ind
            current_sum = next_sum

        sorted_by_lower_bound = sorted(roulette.keys(), key=lambda x: x[0])

        def get_one():
            r = random.random()

            for (lo, hi) in sorted_by_lower_bound:
                if lo <= r < hi:
                    return roulette[(lo, hi)]

        return get_one

    spin = generate_roulette()
    pairs = list()
    n_pairs = len(population) / 2

    while len(pairs) < n_pairs:
        a, b = spin(), spin()

        # if a == b or (a, b) in pairs or (b, a) in pairs:
        # continue

        pairs.append((a, b))

    return pairs


def fitness_proportionate(**kwargs):
    total_fitness = sum(f(x) for x in kwargs.get('population'))
    scaling_func = lambda x: f(x) / total_fitness

    return roulette(scaling_func=scaling_func, **kwargs)


def sigma_scaled(**kwargs):
    sigma = kwargs.get('sigma')
    average_fitness = kwargs.get('average_fitness')
    population = kwargs.get('population')

    expected_value_func = lambda x: 1 if sigma == 0 else 1 + ((f(x) - average_fitness) / (2 * sigma))
    sigma_sum = sum(expected_value_func(x) for x in population)
    scaling_func = lambda x: expected_value_func(x) / sigma_sum

    return roulette(scaling_func=scaling_func, **kwargs)


def stochastic_uniform(**kwargs):
    scaling_func = lambda x: 1

    return roulette(scaling_func=scaling_func, **kwargs)


def ranked(**kwargs):
    population = kwargs.get('population')

    min_f = min(f(x) for x in population)
    max_f = max(f(x) for x in population)
    sorted_population = sorted(population, key=f, reverse=True)
    scaling_func = lambda x: min_f + (max_f - min_f) * sorted_population.index(x) / (len(population) - 1)

    return roulette(scaling_func=scaling_func, **kwargs)


def tournament(population, group_size, epsilon, **kwargs):
    def get_one(group):
        r = random.random()

        if r < epsilon:
            return random.choice(group)

        return max(group, key=f)

    pairs = list()
    n_pairs = len(population) / 2

    while len(pairs) < n_pairs:
        pool = list(population)

        group_a = random.sample(pool, group_size)
        a = get_one(group_a)
        pool.remove(a)

        group_b = random.sample(pool, group_size)
        b = get_one(group_b)

        pairs.append((a, b))

    return pairs


def eugenics(population, **kwargs):
    """
    Variation on deterministic uniform where the two best are paired,
    then the next two,
    and so on.
    """
    s = sorted(population, key=f, reverse=True)

    pairs = list()
    n_pairs = len(population) / 2
    while len(pairs) < n_pairs:
        a = s.pop(0)
        b = s.pop(0)

        pairs.append((a, b))

    return pairs


MATE_SELECTION_METHODS = (
    fitness_proportionate, sigma_scaled, stochastic_uniform, ranked, tournament, eugenics
)