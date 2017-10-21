import numpy as np
import qubo
import sqa

#params are temperature, Gamma, trotter number, qubo matrix, number of trials
mat = np.array([[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]])
sqa.run(0.02,5,3,qubo.getMat(mat),5)
