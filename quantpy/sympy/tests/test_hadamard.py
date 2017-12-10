import time

from sympy.physics.quantum.gate import H
from sympy.physics.quantum.qubit import Qubit

from quantpy.sympy.qapply import qapply


#from sympy.physics.quantum.qapply import qapply

def test_hadamard_loop():
    lp = 1  # loop size
    ms = 5
    me = 5
    for n in range(ms, me+1):
        ts = 2.6      # target second
        lc = lp       # loop counter
        ss = 0.0      # sum sec
        for l in range(lc):
            # print(n)
            p = '0' * n
            # print(p)
            q = Qubit(p)
            # print(q)
            h = H(0) 
            for i in range(1,n):
                h = H(i) * h
            print(h)
            start = time.time()
            r = qapply(h * q)
            elapsed_time = time.time() - start
            ss += elapsed_time
            print(r)
            print ("elapsed_time:\t{0},\t{1} [sec]".format(n,elapsed_time))
        print("average:\t{0}x{1},\t{2} [sec]".format(n, lc, ss/lc))
        assert ss/lc < ts
