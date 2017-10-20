from numpy import *

N = 20
kT = 0.02
G = 5
m = 10 
jij = 1
q = []

for i in range(m):
	q.append(random.choice([-1,1],N))

while G>0.02:
	for j in range(N*m):
		x = random.randint(N)
		y = random.randint(m)
		dE = (jij*2*q[y][x]*(q[y][(N+x-1)%N]+q[y][(x+1)%N]))/m
		dE += q[y][x]*(q[(m+y-1)%m][x]+q[(y+1)%m][x])*log(1/tanh(G/kT/m))/kT
		if dE<0 or exp(-dE/kT)>random.rand():
			q[y][x] = -q[y][x]
	G*=0.99
