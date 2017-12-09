from sympy.physics.quantum.qapply import qapply as sympy_qapply

from quantpy.sympy.executor._quantumexecutor import BaseQuantumExecutor


class SymPyExecutor(BaseQuantumExecutor):
    def execute(self, circuit, **options):
        return sympy_qapply(circuit, **options)
