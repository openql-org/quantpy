# -*- coding:utf-8 -*-
# vim:ts=4:sw=4:sts=4:et:ai:ff=unix:fenc=utf-8

"""
"""
from quantpy.ising import sqa, qubo
import numpy as np

#params are temperature, Gamma, trotter number, qubo matrix, number of trials
def test_qubo_sqa():
    mat = np.array([[-32,4,4,4,4,4,4,4],[4,-32,4,4,4,4,4,4],[4,4,-32,4,4,4,4,4],[4,4,4,-32,4,4,4,4],[4,4,4,4,-32,4,4,4],[4,4,4,4,4,-32,4,4],[4,4,4,4,4,4,-32,4],[4,4,4,4,4,4,4,-32]])
    sqa.run(0.02,5,4,qubo.getMat(mat),10)
