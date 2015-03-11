from adult_selection import full_generational_replacement
from evo_alg import run_simulation
from mate_selection import ranked
from problems import surprising_sequences
from reproduction import splice, mutate_string_genome

s = {
    'problem': surprising_sequences,
    'problem_parameters': {
        'char_set_size': 20,
        'population_size': 200,
        'genome_size': 45,
        'local': True
    },

    'adult_selection_method': full_generational_replacement,

    'mate_selection_method': ranked,

    'crossover_method': splice,
    'crossover_rate': 0.75,

    'mutation_method': mutate_string_genome,
    'mutation_rate': 0.1,

    'stop': {
        'fitness': 1.0,
        'generation': 1000
    },

    'plot_sigmas': False
}

for S in (3, 5, 10, 15, 20):
    print("S={}".format(S))
    L = S
    stops = 0
    while True:
        s['problem_parameters'].update({
            'char_set_size': S,
            'genome_size': L
        })
        r = run_simulation(s, log=False)
        if r['generation_number'] < 1000:
            print(r['generation_number'], '\t', surprising_sequences.phenotype_representation(
                r['final_best_individual']['phenotype'],
                char_set_size=S,
                genome_size=L)
            )
            L = max(int(L * 1.1), L + 1)
            stops = 0
        else:
            stops += 1
            print('1000 stop')
            if stops == 3:
                break

'''
POP = 200
1 	 S=3, L=3: C, C, B
1 	 S=3, L=4: B, B, C, B
1 	 S=3, L=5: A, B, B, C, A
1 	 S=3, L=6: A, B, C, C, A, C
1 	 S=3, L=7: B, C, A, C, C, B, A

1 	 S=5, L=5: E, C, D, D, C
1 	 S=5, L=6: E, E, D, A, C, A
1 	 S=5, L=7: C, B, A, C, A, D, E
1 	 S=5, L=8: A, E, C, D, A, B, E, A
1 	 S=5, L=9: D, D, E, B, E, D, B, C, A
1 	 S=5, L=10: E, D, C, C, B, E, A, E, B, D
3 	 S=5, L=11: E, B, A, D, A, C, C, B, E, C, D
6 	 S=5, L=12: D, C, A, D, B, C, B, E, A, A, C, D

1 	 S=10, L=10: B, D, A, B, J, B, G, I, F, C
1 	 S=10, L=11: D, C, A, J, F, J, I, C, E, I, I
1 	 S=10, L=12: H, E, C, J, F, D, H, I, D, F, B, A
1 	 S=10, L=13: F, E, A, B, A, G, J, F, D, J, H, H, D
1 	 S=10, L=14: F, G, C, A, H, C, G, J, F, J, E, B, D, A
1 	 S=10, L=15: I, E, A, D, B, D, F, G, G, F, E, B, J, C, E
1 	 S=10, L=16: G, F, J, F, A, E, D, C, I, F, C, H, B, A, G, J
1 	 S=10, L=17: B, E, J, I, D, I, A, F, E, A, D, J, G, I, C, D, B
2 	 S=10, L=18: B, J, F, H, I, F, I, D, C, G, E, J, A, C, B, I, A, J
3 	 S=10, L=19: C, D, H, A, G, F, J, E, F, H, I, I, G, B, D, B, I, E, C
2 	 S=10, L=20: F, G, H, C, J, A, A, H, F, D, J, B, E, B, J, C, I, J, D, F
118 	 S=10, L=22: D, B, J, F, F, J, E, A, B, G, D, E, C, I, C, F, A, G, C, H, J, B
748 	 S=10, L=24: E, D, A, B, C, E, I, J, G, B, J, H, G, F, C, F, A, D, D, I, E, B, H, C

1 	 S=15, L=15: O, A, N, K, B, G, H, O, M, D, H, L, J, O, L
1 	 S=15, L=16: O, E, H, L, N, I, G, F, D, L, H, H, M, C, K, A
1 	 S=15, L=17: A, F, O, B, D, H, J, D, A, G, N, M, E, M, I, O, E
1 	 S=15, L=18: I, O, L, H, J, A, E, F, M, B, M, O, J, L, A, H, H, I
1 	 S=15, L=19: H, C, B, E, N, I, K, A, J, H, A, D, L, K, J, O, N, H, N
1 	 S=15, L=20: E, M, J, O, F, M, B, K, I, N, I, A, A, O, G, F, D, J, E, K
1 	 S=15, L=22: J, F, D, A, J, M, I, F, L, C, G, G, E, L, E, O, B, A, M, N, K, G
3 	 S=15, L=24: O, G, H, N, B, J, K, I, L, G, O, L, A, K, M, C, F, L, D, E, B, I, N, E
3 	 S=15, L=26: D, C, G, M, E, F, M, L, J, A, N, L, F, G, I, K, I, D, E, O, N, K, A, C, C, N
5 	 S=15, L=28: D, B, G, C, M, M, L, C, J, O, D, G, N, E, G, H, A, I, F, K, F, H, I, C, L, B, K, D
6 	 S=15, L=30: N, I, J, G, H, H, F, A, O, M, E, L, C, M, K, A, F, G, J, C, D, O, E, N, H, B, N, F, E, K
175 	 S=15, L=33: L, O, B, N, A, I, F, H, H, L, M, G, E, O, K, J, D, C, G, F, M, N, F, J, I, K, N, O, A, L, B, K, B
176 	 S=15, L=36: L, K, L, G, O, I, B, G, F, J, C, B, I, H, E, D, A, O, M, J, K, N, A, K, D, C, M, B, O, O, H, F, I, G, L, N

1 	 S=20, L=20: I, J, A, A, S, K, O, M, K, D, K, P, C, Q, B, I, C, K, R, E
1 	 S=20, L=22: N, R, R, D, A, E, F, L, H, P, A, H, L, E, K, Q, B, G, T, L, T, R
1 	 S=20, L=24: J, A, I, S, D, H, R, O, I, Q, N, D, C, M, D, L, S, H, N, F, L, O, K, B
1 	 S=20, L=26: A, G, L, Q, R, S, G, B, E, L, I, T, K, H, N, F, K, B, L, G, D, J, D, E, C, Q
2 	 S=20, L=28: M, I, P, N, I, T, B, J, S, D, L, G, H, O, B, S, K, A, I, C, L, D, K, T, P, R, Q, R
3 	 S=20, L=30: K, R, C, E, N, E, O, O, K, F, L, T, P, R, L, D, S, I, N, K, Q, N, I, L, C, M, E, J, N, A
9 	 S=20, L=33: M, O, L, I, B, A, J, B, N, P, C, S, H, E, R, A, A, G, J, D, Q, B, Q, G, L, P, M, N, F, K, T, J, N
6 	 S=20, L=36: H, M, J, L, D, K, S, L, G, I, R, C, D, N, B, O, B, C, Q, J, R, P, I, T, M, F, K, K, P, R, Q, O, E, G, H, A
6 	 S=20, L=39: L, S, T, L, E, C, F, S, P, D, M, D, H, P, G, T, E, I, L, A, R, C, B, G, R, J, N, I, C, O, Q, K, K, P, F, D, S, L, Q
18 	 S=20, L=42: I, D, G, B, H, B, S, J, P, I, L, E, R, I, J, A, A, C, D, B, N, O, Q, K, H, N, G, R, C, K, E, F, Q, M, T, P, H, J, L, F, S, L
81 	 S=20, L=46: I, B, G, N, P, P, Q, S, G, L, N, C, O, M, T, B, H, L, F, I, R, K, J, T, E, A, C, A, B, L, A, S, H, J, E, O, Q, D, M, K, P, I, M, N, F, G
'''