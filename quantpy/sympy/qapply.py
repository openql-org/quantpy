# -*- coding:utf-8 -*-
"""Logic for applying operators to states.
"""

from quantpy.sympy.executor.sympy_executor import SymPyExecutor

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
