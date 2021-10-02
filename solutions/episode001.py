import pytest
import itertools

import numpy as np

from qutip import basis, tensor

# single qubit states
# |0>
ket0 = basis(2, 0)

# |1>
ket1 = basis(2, 1)

# |+>
ketp = (1/np.sqrt(2))*(ket0 + ket1)

# |->
ketm = (1/np.sqrt(2))*(ket0 - ket1)

def test_bra0ket1():
    # <0|1> = 0
    assert ket0.overlap(ket1) == 0

def test_bra0ket0():
    # <0|0>
    assert ket0.overlap(ket0) == 1

def test_multiqubit():
    for (bq1, bq2, kq1, kq2) in itertools.product([0, 1], repeat=4):
        keta = tensor(basis(2, bq1), basis(2, bq2))
        ketb = tensor(basis(2, kq1), basis(2, kq2))
        if bq1 == kq1 and bq2 == kq2:
            assert keta.overlap(ketb) == 1
        else:
            assert keta.overlap(ketb) == 0
