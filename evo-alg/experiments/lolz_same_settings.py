import datetime
from evo_alg import plot_simulation_results
from experiments.average_n_runs import average_n_runs
from problems.simulations import LOLZ

simulation = LOLZ

r = average_n_runs(simulation, 100, 100)

plot_simulation_results(
    r,
    # title="Averages {} runs of {}".format(
    #     N,
    #     S['problem'].NAME
    # ),
    savefig="../report/img/{}.png".format(datetime.datetime.now())
)
