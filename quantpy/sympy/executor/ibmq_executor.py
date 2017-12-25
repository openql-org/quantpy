# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""

Todo:
* Sometimes the final result needs to be expanded, we should do this by hand.
"""

import sympy
import qiskit

#from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor
from _base_quantum_executor import *


class IBMQExecutor(BaseQuantumExecutor):
    def __init__(self, quantum_program=None, api_key=None, backend='local_qasm_simulator', shots=1024):
        super().__init__()
        if quantum_program is None:
            quantum_program = qiskit.QuantumProgram()
        self.qp = quantum_program
        if api_key:
            qp.set_api(api_key, 'https://quantumexperience.ng.bluemix.net/api')
        self.backend = backend
        self.shots = shots

    def execute(self, circuit, **options):
        qasm = sympy_to_qasm(circuit)
        name = self.qp.load_qasm_text(qasm)
        qobj = self.qp.compile(name, backend=self.backend, shots=self.shots)
        cnt = self.qp.run(qobj).get_counts(name)
        self.qp.destroy_circuit(name)
        for reg in list(self.qp.get_quantum_register_names()):
            self.qp.destroy_quantum_register(reg)
        for reg in list(self.qp.get_classical_register_names()):
            self.qp.destroy_classical_register(reg)
        return cnt


def sympy_to_qasm(sympy_expr):
    qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n'
    assert isinstance(sympy_expr, sympy.mul.Mul), 'This type of equation is not supported now.'
    qubit = sympy_expr.args[-1]
    assert isinstance(qubit, sympy.physics.quantum.qubit.Qubit), 'Not a qubit.'
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
            assert False, '{} is not a gate or is a not suported gate.'.format(repr(gate))
    for i in range(len(qubit)):
        qasm += 'measure qr[{0}] -> cr[{0}];\n'.format(i)
    return qasm
