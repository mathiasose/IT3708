from datetime import datetime

from experiments.average_n_runs import average_n_runs
from plot import plot_results
from problems.simulations import ONE_MAX

avgs = []
x = list(range(1, 101))
for s in [
    {
        'crossover_rate': c,
        'mutation_rate': m
    } for c in (0.75, 1.0) for m in (0.01, 0.005)
]:
    simulation = ONE_MAX
    simulation.update(s)
    label = "{}, {}".format(
        simulation['crossover_rate'],
        simulation['mutation_rate']
    )
    avgs.append({
        'x': x,
        'y': average_n_runs(simulation, n=10, generations=100)['average_fitnesses'],
        'label': label
    })

plot_results(
    datasets=avgs,
    savefig="../report/img/{}_avg.png".format(datetime.now()),
    xlabel="Generation number",
    ylabel="Fitness",
    title="Average fitness with specified crossover rate, mutation rate",
    ncol=4
)
