from sympy import Expr
"""Add the feature of the expression that can be reversed multiply order.
"""

def _expr_rshift_as_multiplication_of_reverse_order(lhs, rhs):
    """The multiply express will reverse order.
    """
    return rhs * lhs


def sympy_expr_add_operators():
    """__rshift__ of the Expr instanse will be overrided by Local function expr_rshift_as_multiplication_of_reverse_order.
    """
    Expr.__rshift__ = _expr_rshift_as_multiplication_of_reverse_order
