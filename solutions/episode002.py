import numpy as np

from qutip import basis, tensor

# Pauli operator
from qutip import sigmax, sigmay, sigmaz, qeye

ket0 = basis(2, 0) # bald guy state
ket1 = basis(2, 1) # ninja guy state

# <0|Z|0> = 1
assert ket0.overlap(sigmaz()*ket0) == 1

# <1|Z|1> = -1
assert ket1.overlap(sigmaz()*ket1) == -1

# <0|X|0> = 0
assert ket0.overlap(sigmax()*ket0) == 0

# <1|Y|0> == 1
assert ket1.overlap(sigmax()*ket0) == 1

ketp = (1/np.sqrt(2))*(ket0+ket1)
sqrtX = 1/np.sqrt(2)+(1/np.sqrt(2))*sigmax()

# sqrtX|0> == |+>
assert sqrtX*ket0 == ketp

# CNOT|00> = |00>
# CNOT|01> = |01>
# CNOT|10> = |11>
# CNOT|11> = |10>

# |0><0|(tensor)I + |1><1|(tensor)X
cnot = tensor(ket0*ket0.dag(), qeye(2)) + tensor(ket1*ket1.dag(), sigmax())

ket00 = tensor(ket0, ket0)
ket01 = tensor(ket0, ket1)
ket10 = tensor(ket1, ket0)
ket11 = tensor(ket1, ket1)

assert cnot*ket00 == ket00
assert cnot*ket01 == ket01
assert cnot*ket10 == ket11
assert cnot*ket11 == ket10

print('cowabunga!')
