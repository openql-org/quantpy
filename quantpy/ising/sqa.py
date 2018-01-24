# -*- coding:utf-8 -*-
"""Utilities of Simulated [Quantum] Annealing.
"""
from numpy import *

#run sqa algorithm with params
def run(kT,Ginit,m,mat,rep):
    """run simulated QA.

    @param kT
    @param Ginit
    @param m
    @param mat
    @param rep
    @return array([qarr,Earr])
    """
    h = mat[0]
    J = mat[1]
    c = mat[2]
    N = len(h)
    tau = 0.99
    Gfin = 0.01
    qarr = []
    Earr = []

    # simulated quantum annealing simulator using quantum monte carlo & metropolis

    for j in range(rep):
        G = Ginit

        q = []
        for i in range(m):
            q.append(random.choice([-1,1],N))

        while G > Gfin:
            for i in range(N*m):
                x = random.randint(N)
                y = random.randint(m)
                dE = (2*q[y][x]*(h[x]+q[y][(N+x-1)%N]*J[x][(N+x-1)%N]+q[y][(x+1)%N]*J[x][(x+1)%N]))*1.0/m
                dE += -q[y][x]*(q[(m+y-1)%m][x]+q[(y+1)%m][x])*log(tanh(G/kT/m))*1.0/kT
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

    return(array([qarr,Earr]))
