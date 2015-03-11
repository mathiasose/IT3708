from datetime import datetime

from evo_alg import run_simulation, plot_simulation_results
from problems.simulations import ONE_MAX

def average_n_runs(simulation, n, generations):
    simulation['stop'].update({'fitness': None, 'generation': generations})
    datasets = [run_simulation(simulation, log=False) for _ in range(n)]

    sum_dataset = {
        'average_fitnesses': [0 for _ in range(generations)],
        'sigmas': [0 for _ in range(generations)],
        'best_fitnesses': [0 for _ in range(generations)]
    }

    for i in range(generations):
        for dataset in datasets:
            for key in sum_dataset.keys():
                sum_dataset[key][i] += dataset[key][i]

    avg_func = lambda x: float(x) / n

    avg_dataset = {
        'generation_number': generations,
        'simulation': simulation,
        'average_fitnesses': list(map(avg_func, sum_dataset['average_fitnesses'])),
        'sigmas': list(map(avg_func, sum_dataset['sigmas'])),
        'best_fitnesses': list(map(avg_func, sum_dataset['best_fitnesses']))
    }

    return avg_dataset

if __name__ == "__main__":
    S = ONE_MAX
    N = 10
    G = 100

    avg_dataset = average_n_runs(S, N, G)

    plot_simulation_results(
        avg_dataset,
        title="Averages {} runs of {}".format(
            N,
            S['problem'].NAME
        ),
        savefig="../report/img/{}.png".format(datetime.now())
    )
