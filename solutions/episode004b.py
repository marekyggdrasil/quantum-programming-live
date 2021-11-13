import numpy as np

import itertools

from qutip import rand_ket, basis, tensor # states
from qutip import snot, cnot, rx, rz # unitary
from qutip import qeye

from plotting import plotTeleportationOutcomes

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

# create random state
psi = rand_ket(2)

# initiate the circuit |psi>(x)|00>
psi0 = tensor(psi, basis(2, 0), basis(2, 0))

# perform the circuit
psi1 = snot(N=3, target=1)*psi0
psi2 = cnot(N=3, control=1, target=2)*psi1
psi3 = cnot(N=3, control=0, target=1)*psi2
psi4 = snot(N=3, target=0)*psi3

# simulate the measurement
confs = list(itertools.product([0, 1], repeat=2))

# projection operators
Ps = []
for m1, m2 in confs:
    P = tensor([basis(2, m1).proj(), basis(2, m2).proj(), qeye(2)])
    Ps.append(P)

# apply the classical corrections
psi_proj = []
for P in Ps:
    psi_p = (P*psi4).unit()
    psi_proj.append(psi_p)

# classical correction
X = rx(np.pi, N=3, target=2)
Z = rz(np.pi, N=3, target=2)

psi_corr = [
    psi_proj[0],
    X*psi_proj[1],
    Z*psi_proj[2],
    Z*X*psi_proj[3]
]

# produce the reference states
psi_ref = []
for m1, m2 in confs:
    psi_ = tensor(basis(2, m1), basis(2, m2), psi)
    psi_ref.append(psi_)

# get fidelity
fid = []
fidc = []
for psic, psir in zip(psi_corr, psi_ref):
    f = np.abs(psic.overlap(psir))**2
    fidc.append(f)

for psip, psir in zip(psi_proj, psi_ref):
    f = np.abs(psip.overlap(psir))**2
    fid.append(f)

labels = ['|00>', '|01>', '|10>', '|11>']

# plot the results
title = 'Impact of classical correction on fidelity of teleported state'
filename = 'result.png'
plotTeleportationOutcomes(fid, fidc, labels, title, filename=filename)

