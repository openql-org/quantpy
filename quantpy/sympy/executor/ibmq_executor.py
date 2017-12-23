# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""

Todo:
* Sometimes the final result needs to be expanded, we should do this by hand.
"""
from IBMQuantumExperience import IBMQuantumExperience

from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor


class IBMQExecutor(BaseQuantumExecutor):

    def __init__(self):
        self.token = None
        self.backend = 'ibmqx_qasm_simulator'
        self.shots = 1024
        self.api = None

    def execute(self, circuit, **options):
        """
        """
        qasm = self.to_qasm(circuit)
        print(qasm)
        self.api = IBMQuantumExperience(self.token)
        return self.api.run_experiment(qasm,
                          self.backend,
                          self.shots,
                          name='My First Experiment',
                          timeout=60)


