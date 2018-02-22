from sympy import Expr
"""Add the feature of the expression that can be reversed multiply order.
"""

def _expr_rshift_as_multiplication_of_reverse_order(lhs, rhs):
    """The multiply express will reverse order.
    """
    return rhs * lhs

def sympy_expr_add_operators():
    """oprators of the Expr instanse will be overrided by Local functions.
    """
    sympy_expr_add_rshift()

def sympy_expr_remove_rshift():
    """remove __rshift__ attribute of the Expr instanse 
    """
    if hasattr(Expr, '__rshift__'):
        del Expr.__rshift__

def sympy_expr_add_rshift():
    """__rshift__ of the Expr instanse will be overrided by Local function expr_rshift_as_multiplication_of_reverse_order.
    """
    Expr.__rshift__ = _expr_rshift_as_multiplication_of_reverse_order

def sympy_expr_toggle_rshift():
    """toggle __rshift__ attribute of the Expr instanse.
    """
    if hasattr(Expr, '__rshift__'):
        sympy_expr_remove_rshift()
    else:
        sympy_expr_add_rshift()
