from random import getrandbits
from string import ascii_uppercase, ascii_lowercase

bitstring_to_int_list = lambda bitstr, **kwargs: tuple(map(int, bitstr))
char_list_to_str = lambda char_list: ''.join(char_list)

bit_flip = lambda b: "0" if b == "1" else "1"

generate_random_individual = lambda vector_length: char_list_to_str(str(getrandbits(1)) for _ in range(vector_length))

f = lambda x: x['fitness']


def bitstring_initial_population(population_size, genome_size, **kwargs):
    return tuple(
        generate_random_individual(genome_size) for _ in range(population_size)
    )


def char_set(size):
    return (ascii_uppercase + ascii_lowercase)[:size]
