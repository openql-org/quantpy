# -* coding:utf-8 -*-
"""definition of BaseQuantumExecutor class
"""
from abc import abstractmethod

import sympy
import quantpy.sympy.gate_extension

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

    @abstractmethod
    def experiment(self, circuit, shots, **options):
        """Execute circuit ``shots`` times and return the result.
        @return: dict {Qubit -> int} or {str -> int} like [{'0001': 104}, {..}..]
        """
        pass

    def to_qasm(self, sympy_expr, **options):
        """QuantumExecutor classes' commom method.
        Transform SymPy expression to OpenQASM format descriptions.

        @return qasm format string.
        """
        with_measure = options.get('with_measure', False)
        includes = options.get('includes', ['qelib1.inc'])
        qasm = 'OPENQASM 2.0;\n'
        for f in includes:
            qasm += 'include "{0}";\n'.format(f)
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
            elif isinstance(gate, sympy.physics.quantum.gate.CGate):
                if isinstance(gate.args[1], sympy.physics.quantum.gate.IdentityGate):
                    continue
                t = gate.args[1].args[0]
                if isinstance(gate.args[1], sympy.physics.quantum.gate.XGate):
                    qasm += 'cx qr[{}], qr[{}];\n'.format(tuple(gate.args[0])[0], t)
                elif isinstance(gate.args[1], sympy.physics.quantum.gate.YGate):
                    qasm += 'sdg qr[{}];\n'.format(t)
                    qasm += 'cx qr[{}], qr[{}];\n'.format(tuple(gate.args[0])[0], t)
                    qasm += 's qr[{}];\n'.format(t)
                elif isinstance(gate.args[1], sympy.physics.quantum.gate.ZGate):
                    qasm += 'h qr[{}];\n'.format(t)
                    qasm += 'cx qr[{}], qr[{}];\n'.format(tuple(gate.args[0])[0], t)
                    qasm += 'h qr[{}];\n'.format(t)
                elif isinstance(gate, sympy.physics.quantum.gate.HadamardGate):
                    qasm += 'sdg qr[{}];\n'.format(t)
                    qasm += 'h qr[{}];\n'.format(t)
                    qasm += 'tdg qr[{}];\n'.format(t)
                    qasm += 'cx qr[{}], qr[{}];\n'.format(tuple(gate.args[0])[0], t)
                    qasm += 't qr[{}];\n'.format(t)
                    qasm += 'h qr[{}];\n'.format(t)
                    qasm += 's qr[{}];\n'.format(t)
                elif isinstance(gate.args[1], sympy.physics.quantum.gate.PhaseGate):
                    c = tuple(gate.args[0])[0]
                    qasm += 't qr[{}];\n'.format(t)
                    qasm += 'cx qr[{}], qr[{}];\n'.format(c, t)
                    qasm += 'tdg qr[{}];\n'.format(t)
                    qasm += 'cx qr[{}], qr[{}];\n'.format(c, t)
                    qasm += 't qr[{}];\n'.format(c)
                elif isinstance(gate.args[1], sympy.physics.quantum.gate.TGate):
                    c = tuple(gate.args[0])[0]
                    qasm += 'cu1(pi/4) qr[{}], qr[{}];\n'.format(c, t)
                elif isinstance(gate.args[1], quantpy.sympy.Rk):
                    c = tuple(gate.args[0])[0]
                    r = gate.args[1]
                    k = r.k
                    qasm += 'cu1(pi/{}) qr[{}], qr[{}];\n'.format(k, c, t)
                else:
                    assert False, '{} it is not a gate operator, nor is a supported operator'.format(repr(gate))
            else:
                assert False, '{} it is not a gate operator, nor is a supported operator'.format(repr(gate))
        if with_measure:
            for i in range(len(qubit)):
                qasm += 'measure qr[{0}] -> cr[{0}];\n'.format(i)
        return qasm
