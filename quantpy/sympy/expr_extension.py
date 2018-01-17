from sympy import Expr


def _expr_rshift_as_multiplication_of_reverse_order(lhs, rhs):
    return rhs * lhs


def sympy_expr_add_operators():
    Expr.__rshift__ = _expr_rshift_as_multiplication_of_reverse_order
