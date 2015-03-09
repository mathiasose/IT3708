import matplotlib.pyplot as plt


def plot_results(datasets, xlabel=None, ylabel=None, savefig=None, title=None, ncol=5):
    subplot = plt.subplot()

    if title:
        plt.suptitle(title)

    if xlabel:
        plt.xlabel(xlabel)

    if ylabel:
        plt.ylabel(ylabel)

    for dataset in datasets:
        subplot.plot(dataset['x'], dataset['y'], label=dataset['label'])

    box = subplot.get_position()
    subplot.set_position([
        box.x0,
        box.y0 + box.height * 0.1,
        box.width,
        box.height * 0.9
    ])

    subplot.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.10),
        fancybox=True,
        shadow=True,
        ncol=ncol
    )

    if savefig:
        plt.savefig(savefig)

    plt.show()