from numpy import *

def run(N,kT,G,m,h,J,c,rep):

	tau = 0.9
	Gfin = 0.01
	qarr = []
	Earr = []

	# simulated quantum annealing simulator using quantum monte carlo & metropolis

	for j in range(rep):
		q = []
		for i in range(N):
			q.append(random.choice([-1,1],N))

		while G > Gfin:
			for i in range(N*m):
				x = random.randint(N)
				y = random.randint(m)
				dE = (2*q[y][x]*(h[x]+q[y][(N+x-1)%N]*J[x][(N+x-1)%N]+q[y][(x+1)%N]*J[x][(x+1)%N]))/m
				dE += q[y][x]*(q[(m+y-1)%m][x]+q[(y+1)%m][x])*log(1/tanh(G/kT/m))/kT
				if exp(-dE/kT)>random.rand():
					q[y][x] = -q[y][x]
			G*=tau

		E = 0
		for a in range(N):
			E += h[a]*q[0][a]
			for b in range(a+1,N):
				E += J[a][b]*q[0][a]*q[0][b]

		qarr.append(q)
		Earr.append(E+c)

	print(array([qarr,Earr]))
