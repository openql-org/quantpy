# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""

Todo:
* Sometimes the final result needs to be expanded, we should do this by hand.
"""
import qiskit

from quantpy.sympy.executor._quantumexecutor import BaseQuantumExecutor


class GPUExecutor(BaseQuantumExecutor):
    def execute(self, circuit, **options):
        """
        """
        qasm = self.to_qasm(circuit)
        json = qiskit.compile(qasm, format='json')
        #Todo: feed json to GPU program

        return None
