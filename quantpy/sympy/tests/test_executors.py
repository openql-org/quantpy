import pytest

from sympy.physics.quantum.gate import H
from sympy.physics.quantum.qubit import Qubit
from quantpy.sympy.qapply import qapply
from quantpy.sympy.executor.classical_simulation_executor import ClassicalSimulationExecutor
from quantpy.sympy.executor.sympy_executor import SymPyExecutor
from quantpy.sympy.executor.ibmq_executor import IBMQExecutor


def test_executors():
    c = H(2)*H(1)*H(0)*Qubit('000')
    for executor in (SymPyExecutor(), ClassicalSimulationExecutor(), IBMQExecutor()):
        result = qapply(c, executor=executor)
        # TODO : can we check the result?
        print(result)
        print(result.__class__)


@pytest.mark.skip(reason="this is an example rather than real test. please note this can take long time and there's no job monitoring implemented.")
def test_ibmq_real_device():
    # code mostly from qiskit's "getting started"
    # https://qiskit.org/documentation/getting_started_with_qiskit_terra.html#running-circuits-on-real-devices
    from qiskit import IBMQ
    from qiskit.providers.ibmq import least_busy
    IBMQ.load_accounts()
    real_device = IBMQ.backends(filters=lambda x: not x.configuration().simulator)
    backend = least_busy(real_device)
    print("The best backend is " + backend.name())

    c = H(0)*Qubit('0')
    # XXX : this may takes long time and no feedback of job status yet
    result = qapply(c, executor=IBMQExecutor(backend=backend, shots=1024, qiskit_options={'max_credits': 3}))
    print(result)
    print(result.__class__)
