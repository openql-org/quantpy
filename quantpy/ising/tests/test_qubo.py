# -*- coding:utf-8 -*-

from quantpy.ising import qubo
import numpy as np

#params are temperature, Gamma, trotter number, qubo matrix, number of trials
def test_qubo():
    mat = np.array([[-32,4,4,4,4],[4,-32,4,4,4],[4,4,-32,4,4],[4,4,4,-32,4],[4,4,4,4,-32]])
    print(qubo.getMat(mat))
