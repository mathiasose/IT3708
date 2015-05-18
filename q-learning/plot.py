from __future__ import division, print_function

import matplotlib.pyplot as plt


def plot_temperatures(ideal, experienced):
    plt.title("Ideal temperature vs. experienced temperature")
    plt.plot(ideal, label='ideal')
    plt.plot(experienced, '.', label='experienced')
    # plt.plot(map(lambda t: abs(operator.sub(*t)), zip(ideal, experienced)), label='difference')
    plt.legend(loc='best')
    plt.show()
