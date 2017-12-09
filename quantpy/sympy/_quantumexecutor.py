# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""Base class for quantum executor

"""

from sympy.physics.quantum.qapply import qapply

class BaseQuantumExecutor:

    def execute(self, circuit, **options):
        pass

    def to_qasm(self, circuit):
        pass
        
class SymPyExecutor(BaseQuantumExecutor):
    def execute(self, circuit, options):
        qapply(circuit, options)

