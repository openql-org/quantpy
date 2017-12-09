# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""Logic for applying operators to states.

Usage:
quantpy.qapply(circuit, executor=RegettiExecutor())
quantpy.qapply(circuit, executor=IBMQExecutor())
quantpy.qapply(circuit, executor=SymPyExecutor())

Todo:
* Sometimes the final result needs to be expanded, we should do this by hand.
"""

from ._quantumexecutor import *

def qapply(circuit, **options):
    """
    """
    executor = SymPyExecutor
    # executor = options.get['executor']
    executor.execute(circuit, options)
