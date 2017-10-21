import numpy as np
import qubo

#params are temperature, Gamma, trotter number, qubo matrix, number of trials
mat = np.array([[-32,4,4,4,4],[4,-32,4,4,4],[4,4,-32,4,4],[4,4,4,-32,4],[4,4,4,4,-32]])
print(qubo.getMat(mat))
