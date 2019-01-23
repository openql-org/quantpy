# -*- coding:utf-8 -*-
"""definition of IBMQExecutor class
"""

import qiskit
from qiskit import BasicAer

from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor


class IBMQExecutor(BaseQuantumExecutor):
    """IBMQExecutor Class
    """
    def __init__(self, **options):
        """ Initial method.
            If you use the real devices, you should prepare credentials and the
            backend before calling this method.

            options : dict
                A dict of key/value pairs that determine how the operator actions
                are carried out.

                The following options are valid:

                * ``quantum_program``: qiskit.QuantumProgram instanse
                  (default: None).
                * ``backend``: QISKit's backend name
                  (default: 'local_qasm_simulator').
                * ``shots``: shots using QISKit's execute function
                  (default: 1024).
                * ``qiskit_options`` : dict of additional parameters
                  for qiskit's ``execute`` method.
                  (for example, ``{"max_credits":3}``)
        """
        super().__init__()
        backend = options.get('backend', BasicAer.get_backend('qasm_simulator'))
        shots = options.get('shots', 1024)
        self.backend = backend
        self.shots = shots
        self.extra_args = options.get('qiskit_options', {})

    def execute(self, circuit, **options):
        """
                The following options are valid:

                * ``with_measure``: qapply with measure flag
                  (default: True).
        """
        with_measure = options.get('with_measure', True)
        qasm = self.to_qasm(circuit, with_measure=with_measure)
        quantum_circuit = qiskit.QuantumCircuit.from_qasm_str(qasm)
        try:
            from qiskit import execute
            job = execute(quantum_circuit, backend=self.backend, shots=self.shots, **self.extra_args)
            return job.result().get_counts()
        except qiskit.QiskitError as ex:
            print("error:", ex.args)
            return
