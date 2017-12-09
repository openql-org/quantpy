# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""

Todo:
* Sometimes the final result needs to be expanded, we should do this by hand.
"""
from quantpy.sympy._quantumexecutor as BaseQuantumExecutor

class GPUExecutor(BaseQuantumExecutor):
    def execute(circuit, **options):
    """
    """
        qasm = to_qasm(circuit)
        json = qiskit.compile(qasm, format='json')

