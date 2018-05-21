from sympy import cos, exp, expand, I, Matrix, pi, S, sin, sqrt, Sum, symbols
from sympy.physics.quantum.gate import H, X, Y, Z, CNOT, SWAP, CGateS
from sympy.physics.quantum.gate import IdentityGate as _I
from sympy.physics.quantum.gate import UGate as U
from sympy.physics.quantum.qubit import Qubit

from sympy.physics.quantum.qapply import qapply as sympy_qapply
from quantpy.sympy.qapply import qapply
from quantpy.sympy.gate_extension import *

def test_gate_extension_Rx():
    print(Rx((0,),0))
    print(Rx((0,),pi/4))
    print(Rx((0,),pi/2))
    print(Rx((0,),pi))

def test_gate_extension_Ry():
    print(Ry((0,),0))
    print(Ry((0,),pi/4))
    print(Ry((0,),pi/2))
    print(Ry((0,),pi))

def test_gate_extension_Rz():
    print(Rz((0,),0))
    print(Rz((0,),pi/4))
    print(Rz((0,),pi/2))
    print(Rz((0,),pi))

def test_gate_extension_Rk():
    for k in range(5):
        c = Rk(0,k)
        assert qapply(c) == sympy_qapply(c)
        c = RkGate(0,k)
        assert qapply(c) == sympy_qapply(c)

def test_gate_extension_Mz():
    c = Mz(0)
    assert qapply(c) == sympy_qapply(c)

def test_gate_extension_Mx():
    c = Mx(0)
    assert qapply(c) == sympy_qapply(c)
