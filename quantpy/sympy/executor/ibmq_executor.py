# -*- coding:utf-8 -*-
"""definition of IBMQExecutor class
"""

import sympy
import qiskit

from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor

class IBMQExecutor(BaseQuantumExecutor):
    """IBMQExecutor Class
    """
    def __init__(self, **options):
        """ Initial method.

            options : dict
                A dict of key/value pairs that determine how the operator actions
                are carried out.

                The following options are valid:

                * ``quantum_program``: qiskit.QuantumProgram instanse
                  (default: None).
                * ``api_key``: set your api_key if you get api_key
                  (default: None).
                * ``backend``: QISKit's backend name
                  (default: 'local_qasm_simulator').
                * ``backend``: shots using QISKit's execute function
                  (default: 1024).
        """
        super().__init__()
        quantum_program = options.get('quantum_program', None)
        if quantum_program is None:
            quantum_program = qiskit.QuantumProgram()
        backend = options.get('backend', 'local_qasm_simulator')
        shots = options.get('shots', 1024)
        api_key = options.get('api_key', None)

        self.backend = backend
        self.shots = shots
        self.qp = quantum_program
        if api_key:
            self.qp.set_api(api_key, 'https://quantumexperience.ng.bluemix.net/api')

    def execute(self, circuit, **options):
        """
                The following options are valid:

                * ``with_measure``: qapply with measure flag
                  (default: True).
        """
        with_measure = options.get('with_measure', True)
        qasm = self.to_qasm(circuit, with_measure)
        name = self.qp.load_qasm_text(qasm)
        try: 
            qobj = self.qp.compile(name, backend=self.backend, shots=self.shots)
            cnt = self.qp.run(qobj).get_counts(name)
            self.qp.destroy_circuit(name)
            for reg in list(self.qp.get_quantum_register_names()):
                self.qp.destroy_quantum_register(reg)
            for reg in list(self.qp.get_classical_register_names()):
                self.qp.destroy_classical_register(reg)
            return cnt
        except qiskit._resulterror.ResultError as ex:
            print("error:", ex.args)
            return
