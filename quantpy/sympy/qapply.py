# -*- coding:utf-8 -*-
"""Logic for applying operators to states.
"""

__all__ = ['qapply', 'qexperiment']

from quantpy.sympy.executor.sympy_executor import SymPyExecutor
from sympy.physics.quantum.qubit import Qubit

def qapply(circuit, **options):
    """Apply quantum operators to quantum states in a quantum expression.
    The interpretation of the arguments circuit and option depends on the implementation of QuantumExecutor.

    @param circuit: Expr
        Symbol description expression that can be handled with SymPy 
        showing quantum operator and quantum state.
        Analyze the operation order of the quantum operator, and apply them to the quantum state.
        
    @param options: dict
        It is a key/value pairs to indicate a parameter to decide how to work.

        The following options are valid:

        * ``executor``: Specify the Executor instance for executing qapply.
                        The default is SymPyExecutor().

    @return executor.execute()
    """
    executor = options.get('executor', SymPyExecutor())
    return executor.execute(circuit, **options)


def qexperiment(circuit, shots=1024, executor=SymPyExecutor(), **options):
    """Apply quantum operators to quantum states and execute a measurement.
    This is mostly equivalent to sympy code ``measure_all(qapply(circuit))``,
    but this returns the occurrence count of each state instead of probability.

    @param circuit: Expr
        Symbol description expression that can be handled with SymPy
        showing quantum operator and quantum state.
        Analyze the operation order of the quantum operator, and apply them to the quantum state.
        Please note that most backend doesn't accept sympy Symbols.

    @param slots: int
        Repeat count of the measurement executed.

    @param executor: executor object
        The executor used for this experiment.

    @param options: dict
        The extra parameters passed to executor.

    @return : dict {Qubit -> int}
        dict of each Qubit and the number of the count observed.
        States not observed may be omitted.
        For example, ``{Qubit(0): 513, Qubit(1): 511}`` or ``{Qubit(1):1024}``
    """
    _result = executor.experiment(circuit, shots, **options)
    # make sure the return is Sympy Qubit
    result = {}
    for k, v in _result.items():
        if not isinstance(k, Qubit):
            result[Qubit(k)] = v
        else:
            result[k] = v
    return result
