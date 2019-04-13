# -*- coding:utf-8 -*-
"""definition of SymPyExdecutor class
"""
from sympy.physics.quantum.qapply import qapply as sympy_qapply
from ._base_quantum_executor import BaseQuantumExecutor
from collections import defaultdict

class SymPyExecutor(BaseQuantumExecutor):
    """SymPyExecutor Class for transparently executing sympy's qapply.
    """
    def __init__(self):
        """Initial method.
        """
        super().__init__()
        self.random_sequence = self.__class__._default_random_sequence

    def execute(self, circuit, **options):
        """This method calls sympy.physics.quantum.qapply transparently.
        """
        return sympy_qapply(circuit, **options)

    def experiment(self, circuit, shots, **options):
        """This method calls sympy.physics.quantum.qapply, then count numbers of bits observed.
        """
        from sympy.physics.quantum.qubit import measure_all
        import sympy
        # calculate probability from the result of ``qapply``
        probabilities = measure_all(sympy_qapply(circuit, **options))
        # make list of tuples (``qubit str``, ``probability``) as (Qubit('0000'), 0.125), (Qubit('0001'), 0.25)..
        result = defaultdict(int)
        for qubit, probability in probabilities:
            result[qubit] = sympy.simplify(probability * shots)
        return result

    @staticmethod
    def _default_random_sequence(num):
        import random
        return (random.random() for _ in range(num))

    @staticmethod
    def step_sequence(num):
        """
        dummy "radom" method used for testing.
        This yields list [0, 1/n, 2/n...], 
        so you can easily estimate the number of result from shot
        """
        return (i / num for i in range(num))
