import numpy as np

import random

from qutip import basis, rand_ket # states
from qutip import rx, ry, rz # unitary
from qutip import sigmax, sigmay, sigmaz
from qutip import expect # measurement

from plotting import nicebars

# single qubit states
# |0>
ket0 = basis(2, 0)

# |1>
ket1 = basis(2, 1)

# |+>
ketp = (1/np.sqrt(2))*(ket0 + ket1)

# |->
ketm = (1/np.sqrt(2))*(ket0 - ket1)

# |+i>
ketip = (1/np.sqrt(2))*(ket0 + 1j*ket1)

# |-i>
ketim = (1/np.sqrt(2))*(ket0 - 1j*ket1)

# pick a measurement basis


def experiment(ket, M, psi0, psi1, rs, ro):
    phi = np.random.uniform(-np.pi/2, np.pi/2, 1)[0]
    theta = np.random.uniform(0, 2*np.pi, 1)[0]

    rots = rs(phi)
    roto = ro(theta)

    # measure
    p = np.abs(expect(M, ket))**2
    if p > 0.5:
        ket_init = psi0
    else:
        ket_init = psi1

    # perform orthogonal perturbation
    ket_init = rots*ket_init

    # perform perturbation around the measurement axis
    ket_init = roto*ket_init

    # get fidelity
    fid = abs(ket_init.overlap(ket))**2

    return fid

var1 = (sigmax(), ketp, ketm, rz, rx)
var2 = (sigmay(), ketip, ketim, rx, ry)
var3 = (sigmaz(), ket0, ket1, rx, rz)
variants = [var1, var2, var3]

values = []
labels = []
nsamples = [10, 20, 40, 80, 160]

for n in nsamples:
    smm = 0
    for i in range(n):
        ket = rand_ket(2)
        M, psip, psim, rs, ro = random.choice(variants)
        fid =  experiment(ket, M, psip, psim, rs, ro)
        smm += fid
    avg = smm/n
    values.append(avg)
    labels.append(str(n))

nicebars(values, labels, maxval=1, axhline=(2/3), axhline_text='2/3', title='classical bound of teleportation', filename='result.png')
