from abc import abstractmethod,ABCMeta

class BaseSimulator(metaclass=ABCMeta):
    def __init__(self):
        self.basis_gates = None

    @abstractmethod
    def initialize(self,n):
        pass

    @abstractmethod
    def apply(self,gate,target,control=None,theta=None,param=None,update=True):
        pass

    def can_simulate_gate(self, gate):
        return gate in (self.basis_gates + ["U"] + ["measure"])
