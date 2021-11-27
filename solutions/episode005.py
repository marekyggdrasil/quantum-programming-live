import numpy as np

from qutip import basis, sigmax, mesolve, tensor, sigmay, sigmaz, qeye

from plotting import plotTimeEvolution

resolution = 50

# challenge 1(a)

def getFid(t, psi):
    fid0 = np.abs(psi.overlap(basis(2, 0)))**2
    fid1 = np.abs(psi.overlap(basis(2, 1)))**2
    return [fid0, fid1]

times, dt = np.linspace(0., np.pi/2, 50, retstep=True)

psi0 = basis(2, 0)
H = sigmax()
result = mesolve(H, psi0, times, e_ops=getFid)

M = np.array(result.expect)
fid0 = M.T[0]
fid1 = M.T[1]

fidelities = [(fid0, r'$|<\psi_t|0>|^2$'), (fid1, r'$|<\psi_t|1>|^2$')]
potentials = [(np.ones(resolution), r'$\sigma^g$')]

plotTimeEvolution(times, fidelities, potentials, '', marks=[], filename='res.png')

# challenge 1(b)

def getFid(t, psi):
    fid0 = np.abs(psi.overlap(basis(2, 0)))**2
    fid1 = np.abs(psi.overlap(basis(2, 1)))**2
    return [fid0, fid1]

times, dt = np.linspace(0., np.pi, resolution, retstep=True)

a = np.pi
b= np.pi/2

f = lambda t, args: (np.pi/2)*np.exp(-a*(t-b)**2)

psi0 = basis(2, 0)
H = [[sigmax(), f]]
result = mesolve(H, psi0, times, e_ops=getFid)

M = np.array(result.expect)
fid0 = M.T[0]
fid1 = M.T[1]

fidelities = [(fid0, r'$|<\psi_t|0>|^2$'), (fid1, r'$|<\psi_t|1>|^2$')]
potentials = [(f(times, {}), r'$\sigma^g$')]

plotTimeEvolution(times, fidelities, potentials, '', marks=[np.pi/2], filename='res.png')

# Two coins are placed heads on the table. We throw the first coin and if it lands tails, we also throw the second coin. Program a quantum simulation of that scenario. Provide quantum circuit and histogram of counts of measurement outcomes.


def getFid(t, psi):
    fid00 = np.abs(psi.overlap(tensor(basis(2, 0), basis(2, 0))))**2
    fid01 = np.abs(psi.overlap(tensor(basis(2, 0), basis(2, 1))))**2
    fid10 = np.abs(psi.overlap(tensor(basis(2, 1), basis(2, 0))))**2
    fid11 = np.abs(psi.overlap(tensor(basis(2, 1), basis(2, 1))))**2
    return [fid00, fid01, fid10, fid11]

times, dt = np.linspace(0., 2*np.pi, resolution, retstep=True)

a = np.pi

f1 = lambda t, args: (np.pi/4)*np.exp(-a*(t-np.pi/2)**2)
f2 = lambda t, args: (np.pi/4)*np.exp(-a*(t-3*np.pi/2)**2)

psi0 = tensor(basis(2, 0), basis(2, 0))

Hsy = tensor(sigmay(), qeye(2))
Hcc = (1/2)*(tensor(1+sigmaz(), qeye(2))+tensor(1-sigmaz(), sigmay()))

H = [[Hsy, f1], [Hcc, f2]]
result = mesolve(H, psi0, times, e_ops=getFid)

M = np.array(result.expect)
fid00 = M.T[0]
fid01 = M.T[1]
fid10 = M.T[2]
fid11 = M.T[3]

fidelities = [
    (fid00, r'$|<\psi_t|00>|^2$'),
    (fid01, r'$|<\psi_t|01>|^2$'),
    (fid10, r'$|<\psi_t|10>|^2$'),
    (fid11, r'$|<\psi_t|11>|^2$')]
potentials = [(f1(times, {}), r'$H_y$'), (f2(times, {}), r'$H_c$')]

plotTimeEvolution(times, fidelities, potentials, '', marks=[np.pi/2, 3*np.pi/2], filename='res.png')
