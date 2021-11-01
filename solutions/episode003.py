import numpy as np
import itertools

from plotting import histogram

from qutip import basis, tensor, sigmax, qeye, snot

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

def prepareMeasurements(N, psi):
    # all the possible outcomes for N qubits
    confs = list(itertools.product([0, 1], repeat=N))
    # probability distribution
    P = []
    for conf in confs:
        # c=<outcomes|psi>
        psi_ref = tensor([basis(2, m) for m in conf])
        # probability of measuring this outcomes
        p = np.abs(psi.overlap(psi_ref))**2
        # put p in the distribution
        P.append(p)
    return confs, np.array(P)


def simulateMeasurements(conf, P, n):
    return np.random.choice(range(len(conf)), n, p=P)


N = 2
samples = 2000

# heads
heads = basis(2, 0)

# tails
tails = basis(2, 1)

# operators
X1 = tensor(sigmax(), qeye(2))
X2 = tensor(qeye(2), sigmax())

H1 = snot(N=N, target=0)
H2 = snot(N=N, target=1)

P0 = tensor(basis(2, 0)*basis(2, 0).dag(), qeye(2))
P1 = tensor(basis(2, 1)*basis(2, 1).dag(), qeye(2))

II = tensor(qeye(2), qeye(2))

cH2 = P0*II + P1*H2
cH0 = P0*H2 + P1*II

# Coins challenge 1
# Two coins are placed heads on the table. Nothing happens. Program a quantum simulation of that scenario. Provide quantum circuit and histogram of counts of measurement outcomes.

psi = tensor(heads, heads)
conf, P = prepareMeasurements(N, psi)
measurements = simulateMeasurements(conf, P, samples)
unique, counts = np.unique(measurements, return_counts=True)

histogram(unique, counts, N, nsamples=samples, title='test', filename='res.png')

# Coins challenge 2
# Two coins are placed heads on the table. We flip the first coin. Program a quantum simulation of that scenario. Provide quantum circuit and histogram of counts of measurement outcomes.

psi = tensor(heads, heads)
psif = X1*psi
conf, P = prepareMeasurements(N, psif)
measurements = simulateMeasurements(conf, P, samples)
unique, counts = np.unique(measurements, return_counts=True)

histogram(unique, counts, N, nsamples=samples, title='test', filename='res.png')

# Coins challenge 3
# Two coins are placed heads on the table. We throw the second coin. Program a quantum simulation of that scenario. Provide quantum circuit and histogram of counts of measurement outcomes.

psi = tensor(heads, heads)
psif = H2*psi
conf, P = prepareMeasurements(N, psif)
measurements = simulateMeasurements(conf, P, samples)
unique, counts = np.unique(measurements, return_counts=True)

histogram(unique, counts, N, nsamples=samples, title='test', filename='res.png')

# Coins challenge 4
# Two coins are placed heads on the table. We throw the first coin and if it lands tails, we also throw the second coin. Program a quantum simulation of that scenario. Provide quantum circuit and histogram of counts of measurement outcomes.

psi = tensor(heads, heads)
psif = cH2*H1*psi
conf, P = prepareMeasurements(N, psif)
measurements = simulateMeasurements(conf, P, samples)
unique, counts = np.unique(measurements, return_counts=True)

histogram(unique, counts, N, nsamples=samples, title='test', filename='res.png')

# Coins challenge 5
# Two coins are placed heads on the table. We throw the first coin and if it lands heads, we also throw the second coin. Program a quantum simulation of that scenario. Provide quantum circuit and histogram of counts of measurement outcomes.

psi = tensor(heads, heads)
psif = cH0*H1*psi
conf, P = prepareMeasurements(N, psif)
measurements = simulateMeasurements(conf, P, samples)
unique, counts = np.unique(measurements, return_counts=True)

histogram(unique, counts, N, nsamples=samples, title='test', filename='res.png')
