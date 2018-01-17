# -*- coding:utf-8 -*-

from quantpy.ising import qubo
import numpy as np

#params are temperature, Gamma, trotter number, qubo matrix, number of trials
def test_qubo():
    mat = np.array([[-32,4,4,4,4],[4,-32,4,4,4],[4,4,-32,4,4],[4,4,4,-32,4],[4,4,4,4,-32]])
    assert all([a == b for a, b in zip(qubo.getMat(mat) ,
                [[0.0, 0.0, 0.0, 0.0, 0.0], 
                [[0, 1.0, 1.0, 1.0, 1.0],
                 [1.0, 0, 1.0, 1.0, 1.0],
                 [1.0, 1.0, 0, 1.0, 1.0],
                 [1.0, 1.0, 1.0, 0, 1.0],
                 [1.0, 1.0, 1.0, 1.0, 0]],
                -70.0])
              ])
