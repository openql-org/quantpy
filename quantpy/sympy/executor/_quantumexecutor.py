# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""Base class for quantum executor

"""
from abc import abstractmethod

import sympy


class BaseQuantumExecutor:

    @abstractmethod
    def execute(self, circuit, **options):
        return None

    def to_qasm(self, sympy_expr):
        """
        """
        qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n'
        assert isinstance(sympy_expr, sympy.mul.Mul), 'Sorry. Now, supported U*U*U*Qubit format'
        qubit = sympy_expr.args[-1]
        assert isinstance(qubit, sympy.physics.quantum.qubit.Qubit), 'Sorry. Now, supported U*U*U*Qubit format'
        qasm += 'qreg qr[{0}];\ncreg cr[{0}];\n'.format(len(qubit))
        for i,qb in enumerate(reversed(qubit.args)):
            if isinstance(qb, sympy.numbers.One):
                qasm += 'x qr[{}];\n'.format(i)
        for gate in reversed(sympy_expr.args[:-1]):
            if isinstance(gate, sympy.physics.quantum.gate.IdentityGate):
                continue
            elif isinstance(gate, sympy.physics.quantum.gate.HadamardGate):
                qasm += 'h qr[{}];\n'.format(int(gate.args[0]))
            elif isinstance(gate, sympy.physics.quantum.gate.XGate):
                qasm += 'x qr[{}];\n'.format(int(gate.args[0]))
            elif isinstance(gate, sympy.physics.quantum.gate.YGate):
                qasm += 'y qr[{}];\n'.format(int(gate.args[0]))
            elif isinstance(gate, sympy.physics.quantum.gate.ZGate):
                qasm += 'z qr[{}];\n'.format(int(gate.args[0]))
            elif isinstance(gate, sympy.physics.quantum.gate.PhaseGate):
                qasm += 's qr[{}];\n'.format(int(gate.args[0]))
            elif isinstance(gate, sympy.physics.quantum.gate.TGate):
                qasm += 't qr[{}];\n'.format(int(gate.args[0]))
            elif isinstance(gate, sympy.physics.quantum.gate.CNotGate):
                qasm += 'cx qr[{}], qr[{}];\n'.format(int(gate.args[0]), int(gate.args[1]))
            elif isinstance(gate, sympy.physics.quantum.gate.SwapGate):
                qasm += 'cx qr[{}], qr[{}];\n'.format(int(gate.args[0]), int(gate.args[1]))
                qasm += 'cx qr[{}], qr[{}];\n'.format(int(gate.args[1]), int(gate.args[0]))
                qasm += 'cx qr[{}], qr[{}];\n'.format(int(gate.args[0]), int(gate.args[1]))
            else:
                assert False, '{}はゲートじゃないか、対応してないゲートです'.format(repr(gate))
        for i in range(len(qubit)):
            qasm += 'measure qr[{0}] -> cr[{0}];\n'.format(i)
        return qasm
        

