# -*- coding: utf-8 -*-
from quantpy import sqa, qubo
import numpy as np

#params are number of qubits, temperature, Gamma, trotter number, qubo matrix, number of trials
def test_qubo_sqa():
  mat = np.array([[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]])
  sqa.run(4,0.02,3,3,qubo.geth(4,mat),qubo.getj(4,mat),qubo.getc(4,mat),10)
