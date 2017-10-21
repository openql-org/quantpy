import numpy as np
import qubo
import sqa

#params are temperature, Gamma, trotter number, qubo matrix, number of trials
mat = np.array([[-32,4,4,4,4,4,4,4],[4,-32,4,4,4,4,4,4],[4,4,-32,4,4,4,4,4],[4,4,4,-32,4,4,4,4],[4,4,4,4,-32,4,4,4],[4,4,4,4,4,-32,4,4],[4,4,4,4,4,4,-32,4],[4,4,4,4,4,4,4,-32]])
sqa.run(0.02,5,4,qubo.getMat(mat),10)
