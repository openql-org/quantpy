from numpy import *

def run(N,kT,G,m,qubo,rep):

	tau = 0.9
	Gfin = 0.01
	h = []
	J = [[0] * N for i in range(N)]
	qarr = []

	# qubo to ising hamiltonian 
	for j in range(N):
		Jsum = 0

		for i in range(j+1,N):
			r = qubo[j][i]
			J[j][i] = r/4
			J[i][j] = r/4
			Jsum += r 
		h.append(qubo[j][0]/2 + Jsum)


	# simulated quantum annealing simulator using quantum monte carlo & metropolis

	for j in range(rep):
		q = []

		for i in range(m):
			q.append(random.choice([-1,1],N))

		while G>Gfin:
			for i in range(N*m):
				x = random.randint(N)
				y = random.randint(m)
				dE = (2*q[y][x]*(h[x]+q[y][(N+x-1)%N]*J[x][(N+x-1)%N]+q[y][(x+1)%N]*J[x][(x+1)%N]))/m
				dE += q[y][x]*(q[(m+y-1)%m][x]+q[(y+1)%m][x])*log(1/tanh(G/kT/m))/kT
				if exp(-dE/kT)>random.rand():
					q[y][x] = -q[y][x]
			G*=tau

		qarr.append(q)
	print(qarr)
