
"""
Class for simulation of unitary universal quantum circuits.
Use numpy-native functions for simulation
"""

import numpy as np

from quantpy.sympy.executor.simulator._base_simulator import BaseSimulator

class NumpySimulator(BaseSimulator):

    def __init__(self,verbose=False):
        """
        @param verbose : output verbose comments for debug (default: false)
        @return None
        """
        super().__init__()
        self.verbose = verbose
        self.currentTrace = None
        self.basis_gates = ["x","z","y","h","s","t","cx","cz","m0","m1"]

    def initialize(self,n):
        self.n = n
        self.dim = 2**n
        self.state = np.zeros(self.dim,dtype=np.complex128)
        self.state[0]=1.
        self.nstate = np.zeros_like(self.state)
        self.indices = np.arange(self.dim,dtype=np.uint32)

    def apply(self,gate,target,control=None,theta=None,param=None,update=True):
        """
        apply quantum gate to the qubit(s)

        @param gate : string or cupy kernel of applying gate
        @param target : target qubit index or indices
        @param control : control qubit index or indices (default: empty list)
        @param theta : rotation angle, used in rotation gate (default: None)
        @param params : description of unitary operation (default: empty list)
        @update : The calculated state is placed in buffer-state. If update is Ture, swap current state with buffer after calculation. (default: True)
        """
        if not hasattr(target,"__iter__"):
            target = [target]
        if not hasattr(control,"__iter__"):
            control = [control]
        gate = gate.lower()

        if(gate =="x"):
            mask = 1<<target[0]
            self.nstate = self.state[self.indices^mask]
        elif(gate == "z"):
            mask = 1<<target[0]
            self.nstate = self.state * ((self.indices & mask == 0)*2-1)
        elif(gate == "y"):
            mask = 1<<target[0]
            self.nstate = (self.state * ((self.indices & mask == 0)*2-1) * 1j)[self.indices^mask]
        elif(gate == "h"):
            mask = 1<<target[0]
            self.nstate = (self.state * ((self.indices & mask == 0)*2-1) + self.state[self.indices^mask])/np.sqrt(2.)
        elif(gate == "s"):
            mask = 1<<target[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask != 0] *= 1j
        elif(gate == "t"):
            mask = 1<<target[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask != 0] *= (1+1j)/np.sqrt(2.)
        elif(gate == "m0"):
            mask = 1<<target[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask != 0] = 0.
        elif(gate == "m1"):
            mask = 1<<target[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask == 0] = 0.
        elif(gate == "cx"):
            mask1 = 1<<target[0]
            mask2 = 1<<control[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask1 != 0] = self.nstate[ self.indices[self.indices & mask1 != 0] ^ mask2 ]
        elif(gate == "cz"):
            mask1 = 1<<target[0]
            mask2 = 1<<control[0]
            self.nstate = (self.state *   (1-np.logical_and( (self.indices & mask1 != 0) , (self.indices & mask2 != 0))*2)   )
        elif(gate == "u"):
            mask = 1<<target[0]
            ind1 = np.where(self.indices & mask == 0)
            ind2 = np.where(self.indices & mask != 0)
            self.nstate = np.copy(self.state)

            assert(len(param)==3)
            u0 = np.exp(-1j*(param[1]+param[2])/2.) * np.cos(param[0]/2.)
            u1 = -np.exp(-1j*(param[1]-param[2])/2.) * np.sin(param[0]/2.)
            u2 = np.exp(1j*(param[1]-param[2])/2.) * np.sin(param[0]/2.)
            u3 = np.exp(1j*(param[1]+param[2])/2.) * np.cos(param[0]/2.)
            self.nstate[ind1] = u0 * self.state[ind1] + u1 * self.state[ind2]
            self.nstate[ind2] = u2 * self.state[ind1] + u3 * self.state[ind2]

        else:
            raise Exception("not implemented {}".format())

        if(update):
            self.update()
        else:
            return self.trace(buffer=True)

    def update(self):
        """
        swap buffer-state with the current state
        """
        self.state,self.nstate = self.nstate,self.state
        self.currentTrace = None

    def trace(self,buffer=False):
        """
        take trace of the quantum state
        @buffer : calculate trace of buffer-state (default: False)
        """
        if(self.verbose): print("Calculate trace")
        if(buffer):
            return np.real(np.sum(self.nstate * np.conj(self.nstate)))
        else:
            val = np.real(np.sum(self.state * np.conj(self.state)))
            self.currentTrace = val
            return np.real(val)

    def normalize(self,eps=1e-16):
        """
        normalize quantum state
        @eps : if trace is smaller than eps, raise error for avoiding Nan (default: 1e-16)
        """
        if(self.currentTrace is None):
            self.trace()
        valtrace = self.currentTrace
        if(valtrace<eps):
            raise ValueError("Try to normalize zero-trace state : {}".format(valtrace))
        self.state/=np.sqrt(self.currentTrace)
        if(self.verbose): print("Normalize")

    def asnumpy(self):
        """
        recieve quantum state as numpy matrix.
        Do nothing in numpy
        """
        return self.state

    def __str__(self,eps=1e-10):
        """
        overload string function
        return bra-ket representation of current quantum state (very slow when n is large)
        @eps : ignore amplitude smaller than eps when we convert state to str
        """
        fst = True
        ret = ""
        for ind in range(self.dim):
            val = self.state[ind]
            if(abs(val)<eps):
                continue
            else:
                if(fst):
                    fst = False
                else:
                    ret += " + "
                ret += str(val) + "|" + format(ind,"b").zfill(self.n)[::-1]+ ">"
        return ret

    def __bound(self,ind):
        return (0<=ind and ind<self.n)
