# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""

Todo:
* Sometimes the final result needs to be expanded, we should do this by hand.
"""

from quantpy.sympy._quantumexecutor as BaseQuantumExecutor

class IBMQExecutor(BaseQuantumExecutor):
    # def __init__(self, quantum_program=None, api_key=None, backend='local_qasm_simulator', shots=1024):
    #     super().__init__()
    #     if quantum_program is None:
    #         quantum_program = qiskit.QuantumProgram()
    #     self.qp = quantum_program
    #     if api_key:
    #         qp.set_api(api_key, 'https://quantumexperience.ng.bluemix.net/api')
    #     self.backend = backend
    #     self.shots = shots

    def execute(circuit, **options):
        """
        """
        qasm = to_qasm(circuit)
        
        api = IBMQuantumExperience("token", config)
        device = 'simulator'
        shots = 1024
        
        api.run_experiment(qasm,
                          device,
                          shots,
                          name='My First Experiment',
                          timeout=60)
     
    # def execute(self, circuit, **options):
    #     qasm = sympy_to_qasm(circuit)
    #     name = self.qp.load_qasm_text(qasm)
    #     qobj = self.qp.compile(name, backend=self.backend, shots=self.shots)
    #     return self.qp.run(qobj).get_counts(name)

    def to_qasm(sympy_expr):
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
