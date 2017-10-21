import numpy as np
import qubo
import sqa

#params are number of qubits, temperature, Gamma, trotter number, qubo matrix, number of trials
mat = np.array([[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]])
sqa.run(0.02,5,3,qubo.geth(mat),qubo.getj(mat),qubo.getc(mat),10)
