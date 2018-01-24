# -*- coding:utf-8 -*-
"""definition of IBMQExecutor class
"""

import sympy
import qiskit

from _base_quantum_executor import *

class IBMQExecutor(BaseQuantumExecutor):
    """IBMQExecutor Class
    """
    def __init__(self, quantum_program=None, api_key=None, backend='local_qasm_simulator', shots=1024):
        """Initial method.
        """
        super().__init__()
        if quantum_program is None:
            quantum_program = qiskit.QuantumProgram()
        self.qp = quantum_program
        if api_key:
            qp.set_api(api_key, 'https://quantumexperience.ng.bluemix.net/api')
        self.backend = backend
        self.shots = shots

    def execute(self, circuit, **options):
        """
        """
        qasm = self.to_qasm(circuit)
        name = self.qp.load_qasm_text(qasm)
        qobj = self.qp.compile(name, backend=self.backend, shots=self.shots)
        cnt = self.qp.run(qobj).get_counts(name)
        self.qp.destroy_circuit(name)
        for reg in list(self.qp.get_quantum_register_names()):
            self.qp.destroy_quantum_register(reg)
        for reg in list(self.qp.get_classical_register_names()):
            self.qp.destroy_classical_register(reg)
        return cnt
