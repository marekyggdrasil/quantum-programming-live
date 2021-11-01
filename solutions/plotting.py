import numpy as np
import itertools
import matplotlib.pyplot as plt

def histogram(unique, counts, N, nsamples=None, title=None, filename=None):
    labels = []
    outcomes = []
    for i, comb in enumerate(list(itertools.product([0, 1], repeat=N))):
        idxs = list(np.where(unique == i)[0])
        if len(idxs) == 0:
            outcomes.append(0)
        else:
            cnt = counts[idxs[0]]
            outcomes.append(cnt)
        txt = ''.join([str(c) for c in list(comb)])
        labels.append(r'$\left \vert {0} \right >$'.format(txt))
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.set_title(title)
    ax.grid(zorder=0)
    if nsamples is not None:
        ax.set_ylim([0, nsamples])
    x = range(2**N)
    width = 0.8
    ax.bar(x, outcomes, width, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    fig.savefig(filename, transparent=True)
