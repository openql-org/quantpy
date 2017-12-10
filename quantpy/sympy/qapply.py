# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""Logic for applying operators to states.

Todo:
* Sometimes the final result needs to be expanded, we should do this by hand.
"""

from .executor.sympy_executor import SymPyExecutor

def qapply(circuit, **options):
    """
    """
    executor = options.get('executor', SymPyExecutor())
    return executor.execute(circuit, **options)
