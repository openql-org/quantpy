#!/usr/bin/env bash
site=`python -c "import os; print(os.path.dirname(os.__file__))"`/site-packages
cp -r ${site}/sympy/physics/quantum/tests/* ./quantpy/sympy/tests/sympy/physics/quantum/
sed -i '.old' 's/^from sympy.physics.quantum.qapply import qapply$/from quantpy.sympy.qapply import qapply/' ./quantpy/sympy/tests/sympy/physics/quantum/*.py
rm ./quantpy/sympy/tests/sympy/physics/quantum/*.old