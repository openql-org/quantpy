import numpy as np
import qubo
import sqa

#params are temperature, Gamma, trotter number, qubo matrix, number of trials
mat = np.array([[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]])
sqa.run(0.02,5,10,qubo.getMat(mat),10)
