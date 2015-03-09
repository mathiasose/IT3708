import random

from utils import bit_flip, char_list_to_str, char_set


random_bool = lambda: random.getrandbits(1)


def splice(a, b):
    if random_bool():  # 50% chance to reorder the two parents
        a, b = b, a

    position = random.randint(0, len(a))
    return a[:position] + b[position:]


def mix(a, b):
    return char_list_to_str(a[i] if random_bool() else b[i] for i in range(len(a)))


def crossover(a, b, crossover_rate, method=splice, n_children=2):
    genotype_a, genotype_b = a['genotype'], b['genotype']

    children = []
    for _ in range(n_children):
        if random.random() > crossover_rate:
            children.append(genotype_a if random_bool() else genotype_b)
        else:
            children.append(method(genotype_a, genotype_b))

    return tuple(children)


def mutate_bit_components(bitstring, p, **kwargs):
    return char_list_to_str(bit_flip(b) if random.random() <= p else b for b in bitstring)


def mutate_bit_genome(bitstring, p, **kwargs):
    if random.random() <= p:
        pos = random.randint(0, len(bitstring) - 1)
        char_list = list(bitstring)
        char_list[pos] = bit_flip(char_list[pos])
        bitstring = char_list_to_str(char_list)

    return bitstring


def no_mutation(bitstring, p, **kwargs):
    return bitstring


def mutate_string_components(string, p, char_set_size, **kwargs):
    return char_list_to_str(random.choice(char_set(char_set_size)) if random.random() <= p else c for c in string)


def mutate_string_genome(string, p, char_set_size, **kwargs):
    if random.random() <= p:
        pos = random.randint(0, len(string) - 1)
        char_list = list(string)
        char_list[pos] = random.choice(char_set(char_set_size))
        string = char_list_to_str(char_list)

    return string


CROSSOVER_METHODS = (splice, mix)

MUTATION_METHODS = (
    mutate_bit_components, mutate_bit_genome, mutate_string_components, mutate_string_genome, no_mutation
)