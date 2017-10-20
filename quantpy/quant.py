from numpy import *

def run(N,kT,G,Gfinish,m,J,h,tau):
	q = []

	for i in range(m):
		q.append(random.choice([-1,1],N))

	while G>Gfinish:
		for j in range(N*m):
			x = random.randint(N)
			y = random.randint(m)
			dE = (2*q[y][x]*(h[x]+q[y][(N+x-1)%N]*J[x][(N+x-1)%N]+q[y][(x+1)%N]*J[x][(x+1)%N]))/m
			dE += q[y][x]*(q[(m+y-1)%m][x]+q[(y+1)%m][x])*log(1/tanh(G/kT/m))/kT
			if exp(-dE/kT)>random.rand():
				q[y][x] = -q[y][x]
		G*=tau

	print(q)
