import numpy as np

from qutip import basis, sigmax, sigmaz, expect, mesolve, qobj_list_evaluate

from plotting import plotTimeEvolution

tau = 32

psim = (1/np.sqrt(2))*(basis(2, 0) - basis(2, 1))

H0 = sigmax()
Hf = sigmaz()

H = [[H0, lambda t, args: (1.-t/tau)], [Hf, lambda t, args: t/tau]]

psi0 = psim

def measurement(t, psi):
    m1 = np.abs(psi.overlap(psim))**2
    m2 = np.abs(psi.overlap(basis(2, 1)))**2
    H_t = qobj_list_evaluate(H, t, {})
    m3 = expect(H_t, psi)
    return [m1, m2, m3]


times, dt = np.linspace(0., tau, 50, retstep=True)
result = mesolve(H, psi0, times, e_ops=measurement)

M = np.array(result.expect).T
ms0 = M[0]
ms1 = M[1]
ms2 = M[2]

spectrum = np.array([qobj_list_evaluate(H, t, {}).eigenenergies() for t in times]).T

gs = spectrum[0]
ex = spectrum[1]

fidelities = [
    (ms0, r'$<-|\psi_t>$'),
    (ms1, r'$<1|\psi_t>$')
]

energies = [
    (ms2, r'$<\psi_t|H_t|\psi_t>$'),
    (gs, 'gs'),
    (ex, 'ex')
]

plotTimeEvolution(times, fidelities, energies, 'AQC1', filename='res.png')
