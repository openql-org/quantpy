import numpy as np
import sqa

#params are N = number of qubits, kT = temperature, Gamma, trotter number, qubo matrix, number of trial and result
sqa.run(4,0.02,3,3,np.array([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]),10)
