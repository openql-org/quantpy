# -*- coding:utf-8 -*- 
"""definition of ClassicalSimulationExecutor class
"""

import numpy as np
from qiskit import QuantumCircuit, transpiler
from qiskit.qasm import Qasm
from qiskit.providers.builtinsimulators import QasmSimulatorPy
from qiskit.converters import circuits_to_qobj
from qiskit.qobj import qobj_to_dict

from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor
from quantpy.sympy.executor.simulator.numpy_simulator import NumpySimulator


class ClassicalSimulationExecutor(BaseQuantumExecutor):

    def __init__(self):
        super().__init__()
        self.simulator = None


    def execute(self, circuit, **options):
        """
        Execute sympy-circuit with classical simulator
        We use numpy simulator as default
        @param circuit sympy object to simulate
        """
        qasm = self.to_qasm(circuit)
        self.simulator = NumpySimulator()
        basis_gates_str = (",".join(self.simulator.basis_gates)).lower()
        # the following one-line compilation ignores basis_gates, and returnes "u2" for "h".
        quantum_circuit = QuantumCircuit.from_qasm_str(qasm)
        circuit = transpiler.transpile(quantum_circuit, basis_gates=basis_gates_str, backend=QasmSimulatorPy())
        qobj = circuits_to_qobj(circuit, QasmSimulatorPy())
        json = qobj_to_dict(qobj)["experiments"][0]
        self.simulate(json)
        return str(self.simulator)

    def simulate(self, circuitJson):
        """
        Simulate qasm script with json format
        @param circuitJson qasm in json format
        """

        sim = self.simulator

        numQubit = circuitJson["header"]["n_qubits"]
        sim.initialize(numQubit)

        if "clbit_labels" in circuitJson["header"].keys():
            numBit = len(circuitJson["header"]["clbit_labels"])
            clbitsArray = np.zeros(numBit)

        for operation in circuitJson["instructions"]:

            gateOps = operation["name"]

            if not self.simulator.can_simulate_gate(gateOps):
                print(" !!! {} is not supported !!!".format(gateOps))
                print(operation)
                continue

            gateTargets = operation["qubits"]

            if "conditional" in operation.keys():
                condition = operation["conditional"]
                condVal = int(condition["val"], 0)
                condMask = int(condition["mask"], 0)
                flag = True
                for ind in range(numBit):
                    if ((condMask >> ind) % 2 == 1):
                        flag = flag and (condVal % 2 == clbitsArray[ind])
                        condVal //= 2
                if (not flag):
                    continue

            if "memory" in operation.keys():
                measureTargets = operation["memory"]

            if "params" in operation.keys():
                params = operation["params"]

            # unparameterized gates
            if (gateOps in ["x", "y", "z", "h", "s", "t", "cx", "cz", "CX"]):
                if (len(gateTargets) == 1):
                    sim.apply(gateOps, target = gateTargets[0])
                elif (len(gateTargets) == 2):
                    sim.apply(gateOps, target = gateTargets[0], control = gateTargets[1])
                else:
                    raise ValueError("Too many target qubits")

            # measurement
            elif (gateOps in ["measure"]):
                trace = sim.trace()
                prob = sim.apply("M0", target = gateTargets[0], update=False) / trace
                if (np.random.rand() < prob):
                    sim.update()
                    clbitsArray[measureTargets[0]] = 0
                else:
                    sim.apply("M1", target = gateTargets[0])
                    clbitsArray[measureTargets[0]] = 1
                sim.normalize()

            # generic unitary operation
            elif (gateOps in ["U"]):
                sim.apply("U", target = gateTargets[0], param = params)

            else:
                raise ValueError("Op:{} is contained in basis gates, but not supported in simulator".format(operation))

    def getStateStr(self):
        """
        Return string representation of the current quantum state
        @return string representation of the current quantum state
        """
        return str(self.simulator)
