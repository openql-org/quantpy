from sympy.physics.quantum.gate import H, X, Y, Z, CNOT, SWAP, CGateS
from sympy.physics.quantum.gate import IdentityGate as _I
from sympy.physics.quantum.gate import UGate as U
from sympy.physics.quantum.qubit import Qubit

from sympy.physics.quantum.qapply import qapply as sympy_qapply
from quantpy.sympy.qapply import qapply

from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor
class MockExecutor(BaseQuantumExecutor):
    def execute(self, circuit, **options):
        """This method calls sympy.physics.quantum.qapply transparently.
        """
        print(circuit)
        return sympy_qapply(circuit, **options)
    

def test_qapply_default_one_qubit_unitary_oprator_using_default_executor():
    c = H(2)*H(1)*H(0)*Qubit('000')
    print(qapply(c))
    assert qapply(c) == sympy_qapply(c)
    c = H(2)*H(1)*H(0)*Qubit('111')
    print(qapply(c))
    assert qapply(c) == sympy_qapply(c)

def test_qapply_default_two_qubit_unitary_oprator_using_default_executor():
    c = CNOT(1,0)*H(1)*H(0)*Qubit('11')
    assert qapply(c) == sympy_qapply(c)

def test_qapply_default_two_qubit_unitary_oprator_using_test_executor():
    c = H(0)*H(1)*Qubit('00')
    assert qapply(c, executor=MockExecutor()) == sympy_qapply(c)
    assert qapply(c, executor=MockExecutor()) == qapply(c)

