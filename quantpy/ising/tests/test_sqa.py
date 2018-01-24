# -*- coding:utf-8 -*-

"""
"""
from quantpy.ising import sqa, qubo
import numpy as np

#params are temperature, Gamma, trotter number, qubo matrix, number of trials
def test_qubo_sqa():
    mat = np.array([[-32,4,4,4,4,4,4,4],[4,-32,4,4,4,4,4,4],[4,4,-32,4,4,4,4,4],[4,4,4,-32,4,4,4,4],[4,4,4,4,-32,4,4,4],[4,4,4,4,4,-32,4,4],[4,4,4,4,4,4,-32,4],[4,4,4,4,4,4,4,-32]])
    arr = sqa.run(0.02,5,4,qubo.getMat(mat),10)
    print(arr)
    for j in range(8):
        for i in range(4):
            assert all([a == b for a, b in zip(arr[0][j][i], [1,1,1,1,1,1,1,1])])
