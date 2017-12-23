# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""

Todo:
* Sometimes the final result needs to be expanded, we should do this by hand.
"""

import qiskit
import numpy as np

from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor


class ClassicalSimulationExecutor(BaseQuantumExecutor):

    def __init__(self):
        self.simulator = None

    def execute(self, circuit, **options):
        """
        """
        qasm = self.to_qasm(circuit)
        json = qiskit.compile(qasm, format='json')
        self.simulate(json)
        return None

    def simulate(self, circuitJson):
        numQubit = circuitJson["header"]["number_of_qubits"]
        sim = self.simulator
        if "number_of_clbits" in circuitJson["header"].keys():
            numBit = circuitJson["header"]["number_of_clbits"]
            clbitsArray = np.zeros(numBit)

        for operation in circuitJson["operations"]:

            gateOps = operation["name"]

            if not self.simulator.can_siumlate_gate(gateOps):
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

            if "clbits" in operation.keys():
                measureTargets = operation["clbits"]

            if "params" in operation.keys():
                params = operation["params"]

            if (gateOps in ["x", "y", "z", "h", "s", "t", "cx", "cz", "m0", "m1", "CX"]):
                if (len(gateTargets) == 1):
                    sim.apply(gateOps, gateTargets[0], theta=params[0])
                elif (len(gateTargets) == 2):
                    sim.apply(gateOps, gateTargets[0], gateTargets[1], theta=params[0])
            elif (gateOps in ["xrot", "yrot", "zrot", "xxrot"]):
                if (len(gateTargets) == 1):
                    self.sim.apply(self.mapper[gateOps], gateTargets[0], theta=params[0])
                elif (len(gateTargets) == 2):
                    self.sim.apply(self.mapper[gateOps], gateTargets[0], gateTargets[1], theta=params[0])
            elif (gateOps in ["measure"]):
                trace = sim.trace()
                prob = sim.apply("M0", gateTargets[0], update=False) / trace
                if (np.random.rand() < prob):
                    sim.update()
                    clbitsArray[measureTargets[0]] = 0
                else:
                    sim.apply("M1", gateTargets[0])
                    clbitsArray[measureTargets[0]] = 1
                sim.normalize()

            elif (gateOps in ["U"]):
                sim.apply("U", gateTargets[0], param=params, theta=params)

            else:
                print(" !!! {} is not supported !!!".format(gateOps))
                print(operation)

        pass
