# -*- coding:utf-8 -*-
"""definition of BaseQuantumExecutor class
"""
from abc import abstractmethod

import sympy
from qiskit.qasm._qasmparser import QasmParser

class BaseQuantumExecutor:
    """BaseQuantumExecutor Class
    """
    def __init__(self):
        """Initial method. No implements.  
        """
        pass

    @abstractmethod
    def execute(self, circuit, **options):
        """Abstract method.
        @return: None
        """
        return None

    def to_qasm(self, sympy_expr):
        """QuantumExecutor classes' commom method.
        Transform SymPy expression to OpenQASM format descriptions.

        @return qasm format string.
        """
        qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n'
        assert isinstance(sympy_expr, sympy.mul.Mul), 'Sorry. Now, supported U*U*U*Qubit format'
        qubit = sympy_expr.args[-1]
        assert isinstance(qubit, sympy.physics.quantum.qubit.Qubit), 'Sorry. Now, supported U*U*U*Qubit format'
        qasm += 'qreg qr[{0}];\ncreg cr[{0}];\n'.format(len(qubit))
        for i, qb in enumerate(reversed(qubit.args)):
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
                assert False, '{} it is not a gate operator, nor is a supported operator'.format(repr(gate))
        for i in range(len(qubit)):
            qasm += 'measure qr[{0}] -> cr[{0}];\n'.format(i)
        return qasm
