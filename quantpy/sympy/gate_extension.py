"""Gate Extension
"""

from sympy.core.compatibility import is_sequence
from sympy import cos, exp, expand, I, Matrix, pi, S, sin, sqrt, Sum, symbols
from sympy.external import import_module
from sympy.physics.quantum.qexpr import QuantumError, QExpr
from sympy.physics.quantum.gate import Gate, UGate, OneQubitGate
from sympy.physics.quantum.gate import _validate_targets_controls
from sympy.physics.quantum.qft import RkGate, Rk
# from sympy.physics.quantum.circuitplot import Mz, Mx

from sympy import Expr, Matrix, exp, I, pi, Integer, Symbol
from sympy.functions import sqrt

__all__ = [
    'Mz',
    'Mx',
    'Rx',
    'Ry',
    'Rz',
    'RkGate',
    'Rk',
]

class Rx(UGate):
    """Rx(theta) gate.
       = Exp{-i*theta*XGate/2}
    """
    gate_name='Rx'
    gate_name_latex=u'Rx'

    #-------------------------------------------------------------------------
    # Initialization
    #-------------------------------------------------------------------------

    @classmethod
    def _eval_args(cls, args):
        targets = args[0]
        theta = args[1]
        mat = Matrix([[cos(theta/2), -I*sin(theta/2)], [-I*sin(theta/2), cos(theta/2)]])
        return UGate._eval_args([targets, mat])

class Ry(UGate):
    """Ry(theta) gate.
       = Exp{-i*theta*ZGate/2}
    """
    gate_name='Ry'
    gate_name_latex=u'Ry'

    #-------------------------------------------------------------------------
    # Initialization
    #-------------------------------------------------------------------------

    @classmethod
    def _eval_args(cls, args):
        targets = args[0]
        theta = args[1]
        mat = Matrix([[cos(theta/2), -sin(theta/2)], [sin(theta/2), cos(theta/2)]])
        return UGate._eval_args([targets, mat])

class Rz(UGate):
    """Rz(theta) gate.
       = Exp{-i*theta*ZGate/2}
    """
    gate_name='Rz'
    gate_name_latex=u'Rz'

    #-------------------------------------------------------------------------
    # Initialization
    #-------------------------------------------------------------------------

    @classmethod
    def _eval_args(cls, args):
        targets = args[0]
        theta = args[1]
        mat = Matrix([[exp(-I*theta/2), 0], [0, exp(I*theta/2)]])
        return UGate._eval_args([targets, mat])

class Mz(OneQubitGate):
    """Mock-up of a z measurement gate.

    This is in circuitplot rather than gate.py because it's not a real
    gate, it just draws one.
    """
    measurement = True
    gate_name='Mz'
    gate_name_latex=u'M_z'

    def __new__(cls, *args):
        args = cls._eval_args(args)
        inst = Expr.__new__(cls, *args)
        inst.hilbert_space = cls._eval_hilbert_space(args)
        return inst
    
    @classmethod
    def _eval_args(cls, args):
        # Fall back to this, because Gate._eval_args assumes that args is
        # all targets and can't contain duplicates.
        return QExpr._eval_args(args)
    
    @property
    def gate_name_plot(self):
        return self.gate_name_latex

class Mx(OneQubitGate):
    """Mock-up of an x measurement gate.

    This is in circuitplot rather than gate.py because it's not a real
    gate, it just draws one.
    """
    measurement = True
    gate_name='Mx'
    gate_name_latex=u'M_x'

    def __new__(cls, *args):
        args = cls._eval_args(args)
        inst = Expr.__new__(cls, *args)
        inst.hilbert_space = cls._eval_hilbert_space(args)
        return inst
    
    @classmethod
    def _eval_args(cls, args):
        # Fall back to this, because Gate._eval_args assumes that args is
        # all targets and can't contain duplicates.
        return QExpr._eval_args(args)
    
    @property
    def gate_name_plot(self):
        return self.gate_name_latex

