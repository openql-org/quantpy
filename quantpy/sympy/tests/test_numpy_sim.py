import time
import pytest
import functools

from sympy import simplify
from sympy.physics.quantum.gate import H, X, Y, Z, IdentityGate, PhaseGate, TGate, CNotGate, SwapGate, CGate
from sympy.physics.quantum.qubit import Qubit, QubitBra
from sympy.physics.quantum.qapply import qapply as sympy_qapply
from quantpy.sympy import Rk

from sympy.physics.quantum.qft import RkGate
from quantpy.sympy.qapply import qapply
from quantpy.sympy.executor.classical_simulation_executor import ClassicalSimulationExecutor

#from sympy.physics.quantum.qapply import qapply

ERR = 1e-9
def normalize(values):
    e = None
    for c in values:
        if abs(c) < ERR:
            continue
        e = c.conjugate() / abs(c)
    else:
        return True
    return [ e * c for c in coefficient]


def same_state(state_numpy, state_sympy):
    # fix global phase
    n = normalize([ state_numpy.get('{:02b}'.format(x), 0) for x in range(4)])
    s = normalize([ sympy_qapply(QubitBra('{:02b}'.format(x)) * state_sympy).doit() for x in range(4) ])
    for i in range(4):
        if abs(n - s) > ERR:
            return False
    return True


@pytest.mark.parametrize("gate", [
    IdentityGate(0),
    H(0),
    X(0),
    Y(0),
    Z(0),
    PhaseGate(0),
    TGate(0),
    CNotGate(0, 1),
    CGate((0,), IdentityGate(1)),
    CGate((0,), H(1)),
    CGate((0,), X(1)),
    CGate((0,), Y(1)),
    CGate((0,), Z(1)),
    CGate((0,), PhaseGate(1)),
    CGate((0,), TGate(1)),
    ])
def test_numpy_simulator(gate):
    for bits in ['00', '01', '10', '11']:
        circuit = gate * Qubit(bits)
        executor = ClassicalSimulationExecutor()
        assert same_state(qapply(circuit, executor=executor), sympy_qapply(circuit)), "failed {} * Qubit({})".format(gate, bits)

def test_rk():
    for bits in ['00', '01', '10', '11']:
        circuit_quantpy = CGate((0,), Rk(1, 4)) * Qubit(bits)
        circuit_sympy = CGate((0,), RkGate(1, 4)) * Qubit(bits)
        executor = ClassicalSimulationExecutor()
        assert same_state(qapply(circuit_quantpy, executor=executor), sympy_qapply(circuit_sympy)), "failed Rk * Qubit({})".format(bits)
