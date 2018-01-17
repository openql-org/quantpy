# -*- coding:utf-8 -*-
"""definition of BaseSimulator class
"""
from abc import abstractmethod,ABCMeta

class BaseSimulator(metaclass=ABCMeta):
    """BaseSimulator Class
    """
    def __init__(self):
        """Initial method. Set basis_gates value is None.
        """
        self.basis_gates = None

    @abstractmethod
    def initialize(self,n):
        """Abstract method. No implements.
        """
        pass

    @abstractmethod
    def apply(self,gate,target,control=None,theta=None,param=None,update=True):
        """Abstract method. No implements.
        """
        pass

    def can_simulate_gate(self, gate):
        """Return True or False whether the parameter `gate` would would be 
        included in  basis_gates + "U" + "measure".
        """
        return gate in (self.basis_gates + ["U"] + ["measure"])
