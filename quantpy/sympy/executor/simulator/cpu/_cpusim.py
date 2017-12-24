
"""
class of quantum circuit simulator
"""

import numpy as np

from quantpy.sympy.executor.local.simulator._base_simulator import BaseSimulator


class CpuSimulator(BaseSimulator):
    def __init__(self,n,verbose=False):
        """
        @param n : number of qubit
        @param verbose : output verbose comments for debug (default: false)
        @return None
        """
        super.__init__()
        self.n = n
        self.dim = 2**n
        self.state = np.zeros(self.dim,dtype=np.complex128)
        self.state[0]=1.
        self.nstate = np.zeros_like(self.state)
        self.verbose = verbose
        self.currentTrace = None
        self.indices = np.arange(self.dim,dtype=np.uint32)

    def apply(self,gate,target,control=None,theta=None,param=None,update=True):
        """
        apply quantum gate to the qubit(s)

        @param gate : string or cupy kernel of applying gate
        @param target : target qubit index or indices
        @param control : control qubit index or indices (default: empty list)
        @param theta : rotation angle, used in rotation gate (default: None)
        @param theta : rotation angle, used in rotation gate (default: None)
        @param params : description of unitary operation (default: empty list)
        @update : The calculated state is placed in buffer-state. If update is Ture, swap current state with buffer after calculation. (default: True)
        """
        if target not in [list,np.ndarray]:
            target = [target]
        if control not in [list,np.ndarray]:
            control = [control]
        gate = gate.upper()

        if(gate.upper() =="X"):
            mask = 1<<target[0]
            self.nstate = self.state[self.indices^mask]
        elif(gate.upper() == "Z"):
            mask = 1<<target[0]
            self.nstate = self.state * ((self.indices & mask == 0)*2-1)
        elif(gate.upper() == "Y"):
            mask = 1<<target[0]
            self.nstate = (self.state * ((self.indices & mask == 0)*2-1) * 1j)[self.indices^mask]
        elif(gate.upper() == "H"):
            mask = 1<<target[0]
            self.nstate = (self.state * ((self.indices & mask == 0)*2-1) + self.state[self.indices^mask])/np.sqrt(2.)
        elif(gate.upper() == "S"):
            mask = 1<<target[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask != 0] *= 1j
        elif(gate.upper() == "T"):
            mask = 1<<target[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask != 0] *= (1+1j)/np.sqrt(2.)
        elif(gate.upper() == "M0"):
            mask = 1<<target[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask != 0] = 0.
        elif(gate.upper() == "M1"):
            mask = 1<<target[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask == 0] = 0.
        elif(gate.upper() == "CX"):
            mask1 = 1<<target[0]
            mask2 = 1<<control[0]
            self.nstate = np.copy(self.state)
            self.nstate[self.indices & mask1 != 0] = self.nstate[ self.indices[self.indices & mask1 != 0] ^ mask2 ]
        elif(gate.upper() == "CZ"):
            mask1 = 1<<target[0]
            mask2 = 1<<control[0]
            self.nstate = (self.state *   (1-np.logical_and( (self.indices & mask1 != 0) , (self.indices & mask2 != 0))*2)   )
        elif(gate.upper() == "U"):
            mask = 1<<target[0]
            ind1 = np.where(self.indices & mask == 0)
            ind2 = np.where(self.indices & mask != 0)
            self.nstate = np.copy(self.state)
            if(len(param)==3):
                u0 = np.exp(-1j*(param[1]+param[2])/2.) * np.cos(param[0]/2.)
                u1 = -np.exp(-1j*(param[1]-param[2])/2.) * np.sin(param[0]/2.)
                u2 = np.exp(1j*(param[1]-param[2])/2.) * np.sin(param[0]/2.)
                u3 = np.exp(1j*(param[1]+param[2])/2.) * np.cos(param[0]/2.)
                self.nstate[ind1] = u0 * self.state[ind1] + u1 * self.state[ind2]
                self.nstate[ind2] = u2 * self.state[ind1] + u3 * self.state[ind2]
            else:
                self.nstate[ind1] = param[0] * self.state[ind1] + param[1] * self.state[ind2]
                self.nstate[ind2] = param[2] * self.state[ind1] + param[3] * self.state[ind2]

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
            val = np.sum(self.state * np.conj(self.state))
            self.currentTrace = val
            return np.real(val)

    def normalize(self,eps=1e-16):
        """
        normalize quantum state
        @eps : if trace is smaller than eps, raise error for avoiding Nan (default: 1e-16)
        """
        if(self.currentTrace is None):
            self.trace()
        valtrace = np.real(self.currentTrace)
        if(valtrace<eps):
            raise ValueError("Trace is too small : {}".format(valtrace))
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

if __name__ == "__main__":
    cs = CpuSimulator(4)
    cs.apply("h",0)
    print(cs)
    #cs.apply("cx",1,0)
    #cs.apply("U",0,param=[np.pi/2,0,0])
    cs.apply("U",0,param=[np.pi/2,0,0])
    #cs.normalize()
    #cs.apply("z",0)
    print(cs)
    cs.apply("U",0,param=[np.pi/2,0,0])
    print(cs)
    cs.apply("U",0,param=[np.pi/2,0,0])
    print(cs)
