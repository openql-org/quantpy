# -*- coding:utf-8 -*-

__all__ = []

# The following pattern is used below for importing sub-modules:
#
# 1. "from foo import *".  This imports all the names from foo.__all__ into
#    this module. But, this does not put those names into the __all__ of
#    this module. This enables "from quantpy.sympy import State" to
#    work.
# 2. "import foo; __all__.extend(foo.__all__)". This adds all the names in
#    foo.__all__ to the __all__ of this module. The names in __all__
#    determine which names are imported when
#    "from quantpy.sympy import *" is done.

#from .qapply import __all__ as qap_all
#from .qapply import *
#__all__.extend(qap_all)

#from . import _quantumexecutor
#from ._quantumexecutor import *
#__all__.extend(_quantumexecutor.__all__)
