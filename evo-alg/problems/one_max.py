from utils import bitstring_to_int_list, bitstring_initial_population

NAME = 'ONE MAX'

generate_initial_population = bitstring_initial_population

geno_to_pheno = bitstring_to_int_list


def fitness_evaluation(phenotype, target_phenotype=None, **kwargs):
    l = len(phenotype)
    if target_phenotype:
        return sum(phenotype[i] == target_phenotype[i] for i in range(l)) / l

    return sum(phenotype) / l


def phenotype_representation(phenotype, **kwargs):
    return str(phenotype)
