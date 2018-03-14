# -*- coding:utf-8 -*-

import textwrap
from sympy.physics.quantum.gate import H, X, Y, Z, CNOT, SWAP, CPHASE, CGate, CGateS
from sympy.physics.quantum.gate import IdentityGate, UGate
from sympy.physics.quantum.qubit import Qubit, QubitBra
from quantpy.sympy.executor._base_quantum_executor import BaseQuantumExecutor

def test_new_instanse():
    executor = BaseQuantumExecutor()
    assert executor != None

def test_execute():
    executor = BaseQuantumExecutor()
    c = H(0)*Qubit('0')
    assert executor.execute(c) == None

def test_to_qasm_with_no_options():
    executor = BaseQuantumExecutor()
    c = H(0)*Qubit('0')
    qasm = executor.to_qasm(c)
    assert qasm.strip() == textwrap.dedent('''
        OPENQASM 2.0;
        include "qelib1.inc";
        qreg qr[1];
        creg cr[1];
        h qr[0];
        ''').strip()

def test_to_qasm_with_includes():
    executor = BaseQuantumExecutor()
    c = H(0)*Qubit('0')
    qasm = executor.to_qasm(c,includes=['qelib2.inc','qelib3.inc'])
    assert qasm.strip() == textwrap.dedent('''
        OPENQASM 2.0;
        include "qelib2.inc";
        include "qelib3.inc";
        qreg qr[1];
        creg cr[1];
        h qr[0];
        ''').strip()
