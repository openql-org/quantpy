from abc import abstractmethod


class BaseSimulator:
    def __init__(self):
        self.basis_gates = ["x", "y", "z", "h", "s", "t", "cx", "cz", "m0", "m1"]

    @abstractmethod
    def apply(self,gate,target,control=None,theta=None,param=None,update=True):
        pass

    def can_simulate_gate(self, gate):
        return gate in self.basis_gates