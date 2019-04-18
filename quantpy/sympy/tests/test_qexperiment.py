from sympy.physics.quantum.gate import H, X, Y, Z, CNOT, SWAP, CGateS
from sympy.physics.quantum.gate import IdentityGate as _I
from sympy.physics.quantum.gate import UGate as U
from sympy.physics.quantum.qubit import Qubit

from sympy.physics.quantum.qapply import qapply as sympy_qapply
from quantpy.sympy.qapply import qexperiment

from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor
from quantpy.sympy.executor.sympy_executor import SymPyExecutor
from quantpy.sympy.executor.ibmq_executor import IBMQExecutor
from quantpy.sympy.executor.classical_simulation_executor import ClassicalSimulationExecutor


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


def test_qexperiment_sympy_with_symbols():
    import sympy as sp
    a, b = sp.symbols('alpha, beta') 
    psi = a*Qubit('00') + b*Qubit('11')
    executor = SymPyExecutor()
    result = qexperiment(X(0) * psi, executor=executor)
    norm = sp.Abs(a)**2 + sp.Abs(b)**2
    assert result == {Qubit('01'): 1024 * a*a.conjugate() / norm,
                      Qubit('10'): 1024 * b*b.conjugate() / norm}


def test_qexperiment_sympy_value1():
    c = H(2)*H(1)*H(0)*Qubit('000')
    executor = SymPyExecutor()
    result = qexperiment(c, 1024, executor)
    assert result == {
            Qubit('000'): 128,
            Qubit('001'): 128,
            Qubit('010'): 128,
            Qubit('011'): 128,
            Qubit('100'): 128,
            Qubit('101'): 128,
            Qubit('110'): 128,
            Qubit('111'): 128,
            }


def test_qexperiment_ibmq():
    c = H(2)*H(1)*H(0)*Qubit('000')
    result = qexperiment(c, executor=IBMQExecutor())
    assert len(result) == 8


def step_sequence(num):
    """
    dummy "radom" method used for testing.
    This yields list [0, 1/n, 2/n...], 
    so you can easily estimate the number of result from the count
    """
    return (i / num for i in range(num))

def test_qexperiment_numpy():
    c = H(2)*H(1)*H(0)*Qubit('000')
    executor = ClassicalSimulationExecutor()
    result = qexperiment(c, 1024, executor, random=step_sequence)
    assert result == {
            Qubit('000'): 128,
            Qubit('001'): 128,
            Qubit('010'): 128,
            Qubit('011'): 128,
            Qubit('100'): 128,
            Qubit('101'): 128,
            Qubit('110'): 128,
            Qubit('111'): 128,
            }

def test_qexperiment_numpy_random():
    c = H(2)*H(1)*H(0)*Qubit('000')
    executor = ClassicalSimulationExecutor()
    result = qexperiment(c, 612, executor)
    assert 612 == sum((x for x in result.values()))
