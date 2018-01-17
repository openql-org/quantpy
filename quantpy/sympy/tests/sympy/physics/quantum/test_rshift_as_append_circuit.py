from sympy.physics.quantum.gate import H, X
from sympy.physics.quantum.qubit import Qubit

from quantpy.sympy.expr_extension import sympy_expr_add_operators


def test_single_rshift_as_append_circuit():
    sympy_expr_add_operators()
    h = H(0)
    x = X(0)
    assert ( h >> x) == x * h
    assert (x >> h) == h * x


def test_qubit_rshift_as_input_to_circuit():
    sympy_expr_add_operators()
    q = Qubit(0)
    h = H(0)
    assert (q >> h) == h * q
    assert (h >> q) == q * h

def test_combine_operator_and_qubit_with_rshifts_to_make_circuit():
    sympy_expr_add_operators()
    q = Qubit(0)
    h = H(0)
    x = X(0)
    t = q >> h
    print(t)
    t2 = t >> x
    assert (q >> h >> x) == x * h * q
