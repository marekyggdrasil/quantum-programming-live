import numpy as np

from qutip import basis, tensor
from qutip import sigmax, sigmay, sigmaz, qeye

ket0 = basis(2, 0) # bald guy
ket1 = basis(2, 1) # ninja

ketp = (1/np.sqrt(2))*(ket0+ket1)

assert np.abs(ket1.overlap(sigmay()*ket0))**2 == 1

sqrtX = (1./np.sqrt(2))+(1./np.sqrt(2))*sigmax()

assert sqrtX*basis(2, 0) == ketp

# (|1><1| (tensor) SX) + (|0><0| (tensor) I)
cnot = tensor([ket1*ket1.dag(), sigmax()])
cnot += tensor([ket0*ket0.dag(), qeye(2)])

ket00 = tensor([ket0, ket0])
ket10 = tensor([ket1, ket0])
ket11 = tensor([ket1, ket1])

assert np.abs(ket00.overlap(cnot*ket00))**2 == 1
assert np.abs(ket11.overlap(cnot*ket10))**2 == 1
