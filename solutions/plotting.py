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

def nicebars(values, labels, maxval=None, axhline=None, axhline_text=None, title=None, filename=None):
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.set_title(title)
    ax.grid(zorder=0)
    if maxval is not None:
        ax.set_ylim([0, maxval])
    width = 0.8
    ax.bar(range(len(values)), values, width, zorder=3)
    if axhline is not None:
        ax.axhline(y=axhline, linestyle='--', color='black', zorder=4)
        if axhline_text is not None:
            plt.text(-0.75, axhline, axhline_text, fontsize=10, va='center', ha='center')
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(labels)
    fig.savefig(filename, transparent=True)

# from: https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
def plotTeleportationOutcomes(outcomes, corrs, labels, title, filename=None):
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    rects1 = ax.bar(x - width/2, outcomes, width, label='not corrected')
    rects2 = ax.bar(x + width/2, corrs, width, label='corrected')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('fidelity')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    if filename is not None:
        fig.savefig(filename, transparent=True)

def plotTimeEvolution(times, fidelities, potentials, title, marks=[], filename=None):
    fig, axs = plt.subplots(2, 1, constrained_layout=True)

    for mark in marks:
        axs[0].axvline(x=mark, color='black', linestyle='--')
        axs[1].axvline(x=mark, color='black', linestyle='--')

    axs[0].set_title('Fidelities')
    for fid, label in fidelities:
        axs[0].plot(times, fid, label=label)
    axs[0].grid()
    axs[0].legend()

    axs[1].set_title('Potentials')
    for pot, label in potentials:
        axs[1].plot(times, pot, label=label)
    axs[1].grid()
    axs[1].legend()

    fig.tight_layout()
    if filename is not None:
        fig.savefig(filename, transparent=True)
