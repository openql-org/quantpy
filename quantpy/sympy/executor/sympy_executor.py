# -*- coding:utf-8 -*-
"""definition of SymPyExdecutor class
"""
from sympy.physics.quantum.qapply import qapply as sympy_qapply
from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor

class SymPyExecutor(BaseQuantumExecutor):
    """SymPyExecutor Class for transparently executing sympy's qapply.
    """
    def __init__(self):
        """Initial method.
        """
        super().__init__()

    def execute(self, circuit, **options):
        """This method calls sympy.physics.quantum.qapply transparently.
        """
        return sympy_qapply(circuit, **options)
