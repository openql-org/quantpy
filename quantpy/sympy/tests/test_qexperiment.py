from sympy.physics.quantum.gate import H, X, Y, Z, CNOT, SWAP, CGateS
from sympy.physics.quantum.gate import IdentityGate as _I
from sympy.physics.quantum.gate import UGate as U
from sympy.physics.quantum.qubit import Qubit

from sympy.physics.quantum.qapply import qapply as sympy_qapply
from quantpy.sympy.qapply import qexperiment

from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor
from quantpy.sympy.executor.sympy_executor import SymPyExecutor


class MockExecutor(BaseQuantumExecutor):
    def experiment(self, circuit, shots, **options):
        self.circuit = circuit
        self.shots = shots
        self.options = options
        return {'0': shots}
    

def test_qexperiment_parameters():
    """
    checks if all parameters are properly passed to executors
    """
    executor = MockExecutor()
    c = Qubit('0')
    result = qexperiment(c, 987654321, executor, test='dummy', otherparameters=1234)

    assert executor.circuit is c
    assert executor.shots is 987654321
    assert executor.options == {'test': 'dummy', 'otherparameters':1234}


def test_qexperiment_default():
    c = H(2)*H(1)*H(0)*Qubit('000')
    result = qexperiment(c)
    # total should be same as shots
    assert sum((v for v in result.values())) == 1024
    # probability that misses one state in 1024 is less than 10^-60
    assert len(result) == 8


def test_qexperiment_sympy_value1():
    c = H(2)*H(1)*H(0)*Qubit('000')
    executor = SymPyExecutor()
    # prepare "random numbers" for test
    executor.random_sequence = SymPyExecutor.step_sequence
    result = qexperiment(c, 1024, executor)
    assert result == {
            '000': 128,
            '001': 128,
            '010': 128,
            '011': 128,
            '100': 128,
            '101': 128,
            '110': 128,
            '111': 128,
            }

