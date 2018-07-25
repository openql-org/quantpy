from sympy.physics.quantum.gate import H, X
from sympy.physics.quantum.qubit import Qubit

from quantpy.sympy.expr_extension import sympy_expr_add_rshift, sympy_expr_remove_rshift, sympy_expr_toggle_rshift
from quantpy.sympy.expr_extension import sympy_expr_add_operators

def test_sympy_expr_add_operators():
    sympy_expr_add_operators()
    assert H(0)>>H(1)>>H(2) == H(2)*H(1)*H(0)

def test_sympy_expr_toggle_rshift():
    sympy_expr_remove_rshift()
    sympy_expr_toggle_rshift()
    assert H(0)>>H(1)>>H(2) == H(2)*H(1)*H(0)
    sympy_expr_toggle_rshift()
    try:
        H(0)>>H(1)>>H(2)
        assert False
    except TypeError as ex:
        assert True

def test_single_rshift_as_append_circuit():
    sympy_expr_add_rshift()
    h = H(0)
    x = X(0)
    assert ( h >> x) == x * h
    assert (x >> h) == h * x

def test_qubit_rshift_as_input_to_circuit():
    sympy_expr_add_rshift()
    q = Qubit(0)
    h = H(0)
    assert (q >> h) == h * q
    assert (h >> q) == q * h

def test_combine_operator_and_qubit_with_rshifts_to_make_circuit():
    sympy_expr_add_rshift()
    q = Qubit(0)
    h = H(0)
    x = X(0)
    assert (q >> h >> x) == x * h * q
