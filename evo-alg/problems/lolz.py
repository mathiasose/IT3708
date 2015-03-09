from utils import bitstring_to_int_list, bitstring_initial_population

NAME = 'LOLZ'

generate_initial_population = bitstring_initial_population

geno_to_pheno = bitstring_to_int_list


def fitness_evaluation(phenotype, z, **kwargs):
    first_symbol = phenotype[0]
    lolz = 0

    for i, b in enumerate(phenotype):
        if b == first_symbol:
            lolz = i + 1
        else:
            break

    if first_symbol == 0 and lolz > z:
        lolz = z

    return (lolz - 1) / (len(phenotype) - 1)


def phenotype_representation(phenotype, **kwargs):
    return str(phenotype)
