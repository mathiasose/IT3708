import random

from utils import char_list_to_str, char_set


NAME = 'SURPRISING SEQUENCES'


def generate_initial_population(population_size, genome_size, char_set_size, **kwargs):
    S = char_set(char_set_size)
    return tuple(
        char_list_to_str(random.choice(S) for _ in range(genome_size))
        for _ in range(population_size)
    )


def geno_to_pheno(genotype, **kwargs):
    return tuple(genotype)


def fitness_evaluation(phenotype, local=False, **kwargs):
    def sequences():
        L = len(phenotype)
        for i in range(L - 1):
            for j in range(i + 1, L):
                yield "{}{}{}".format(phenotype[i], j - i - 1, phenotype[j])
                if local:
                    break

    axb_sequences = list(sequences())
    return (len(set(axb_sequences)) - 1) / (len(axb_sequences) - 1)


def phenotype_representation(phenotype, char_set_size, genome_size, **kwargs):
    return "S={}, L={}: {}".format(
        char_set_size,
        genome_size,
        ", ".join(phenotype)
    )