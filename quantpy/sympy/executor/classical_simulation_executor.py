# -*- coding:utf-8 -*- 
"""definition of ClassicalSimulationExecutor class
"""

from collections import defaultdict
import numpy as np
import sympy

from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor
from quantpy.sympy.executor.simulator.numpy_simulator import NumpySimulator
import quantpy.sympy

def _default_random_sequence(num):
    import random
    return (random.random() for _ in range(num))

class ClassicalSimulationExecutor(BaseQuantumExecutor):

    def __init__(self):
        super().__init__()
        self.simulator = None

    def execute(self, circuit, **options):
        self.simulator = NumpySimulator()
        qubit = circuit.args[-1]
        assert isinstance(qubit, sympy.physics.quantum.qubit.Qubit), 'Sorry. Now, U*U*U*Qubit format is only supported'

        self.simulator.initialize(qubit.dimension)

        # set initial qubit value
        for i, qb in enumerate(reversed(qubit.args)):
            if isinstance(qb, sympy.numbers.One):
                self.simulator.apply('x', i)

        # main loop
        GATE_TO_STR = {
                sympy.physics.quantum.gate.HadamardGate: 'h',
                sympy.physics.quantum.gate.XGate: 'x',
                sympy.physics.quantum.gate.YGate: 'y',
                sympy.physics.quantum.gate.ZGate: 'z',
                sympy.physics.quantum.gate.PhaseGate: 's',
                sympy.physics.quantum.gate.TGate: 't',
                }
        for gate in reversed(circuit.args[:-1]):
            if isinstance(gate, sympy.physics.quantum.gate.IdentityGate):
                continue

            if type(gate) in GATE_TO_STR:
                # gate without parameters
                self.simulator.apply(GATE_TO_STR[type(gate)], int(gate.args[0]))

            elif isinstance(gate, sympy.physics.quantum.gate.CNotGate):
                self.simulator.apply('cx', int(gate.args[0]), int(gate.args[1]))

            elif isinstance(gate, sympy.physics.quantum.gate.SwapGate):
                self.simulator.apply('cx', int(gate.args[0]), int(gate.args[1]))
                self.simulator.apply('cx', int(gate.args[1]), int(gate.args[0]))
                self.simulator.apply('cx', int(gate.args[0]), int(gate.args[1]))

            elif isinstance(gate, sympy.physics.quantum.gate.CGate):
                control = tuple(gate.args[0])[0]
                target_gate = gate.args[1] 

                if isinstance(target_gate, sympy.physics.quantum.gate.IdentityGate):
                    continue

                if type(target_gate) in GATE_TO_STR:
                    # C-"simple" gate
                    self.simulator.apply(GATE_TO_STR[type(target_gate)],
                                         int(target_gate.args[0]), control=control)

                elif isinstance(target_gate, quantpy.sympy.Rk):
                    k = gate.args[1].k
                    self.simulator.apply('u', int(target_gate.args[0]), param=(1, float(k/2), float(k/2)))
                else:
                    assert False, '{} it is not a gate operator, nor is a supported operator'.format(repr(gate))
            else:
                assert False, '{} it is not a gate operator, nor is a supported operator'.format(repr(gate))

        return self.simulator.to_coefficients()

    def getStateStr(self):
        """
        Return string representation of the current quantum state
        @return string representation of the current quantum state
        """
        return str(self.simulator)

    def experiment(self, circuit, shots=1024, random=_default_random_sequence):
        states = self.execute(circuit)
        # create a cumulative probability that monotonically increases
        probabilities = []
        sum = 0.0
        for qubit, amplitude in states.items():
            sum += abs(amplitude) ** 2
            probabilities.append((qubit,sum))
        print(probabilities)
        # collect measurement results
        result = defaultdict(int)
        for r in random(shots):
            for qubit, probability in probabilities:
                if r < probability:
                    result[qubit] += 1
                    break
        return result
