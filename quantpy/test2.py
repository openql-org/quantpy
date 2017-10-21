import numpy as np
import qubo

#params are temperature, Gamma, trotter number, qubo matrix, number of trials
mat = np.array([[0,1,1,1,1],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]])
qubo.getMat(mat)
