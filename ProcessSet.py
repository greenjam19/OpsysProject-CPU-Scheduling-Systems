import math
import sys
class Rand48(object):
    def __init__(self, seed):
        self.n = seed
    def seed(self, seed):
        self.n = seed
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    def drand(self):
        return self.next() / 2**48
    def lrand(self):
        return self.next() >> 17
    def mrand(self):
        n = self.next() >> 16
        if n & (1 << 31):
            n -= 1 << 32
        return n  

class ProcessSet(object):
   
    def __init__(self, numProc, lambda_, seed_no, upp_bound):
        #number of processes
        self.numProc = numProc
        
        #argv[3]: lambda
        self.lambda_= lambda_
        
        #specific random seed number 
        self.rand = Rand48(seed_no)
        
        #upper bound for numbers generated by
        #get_exp()
        self.upp_bound = upp_bound
        
        #seed declaration
        self.rand.srand(seed_no)
        
        #initial guess of CPU bursts times
        self.tau = int(1/self.lambda_)
    
    # the "next_exp()" function required in the pdf 
    #computes the -log of the next random number in 
    #the current seed divided by the given lambda
    def get_exp(self):
        val = -math.log(self.rand.drand())/self.lambda_
        while val>self.upp_bound:
            val = -math.log(self.rand.drand())/self.lambda_
        return val
    
    #generates the arrival times, CPU, and I/O burst times 
    #of each individual process dictated by numProc
    def generate(self):
        #arrival times for ea. process
        self.arr_time = []
        
        #2d list of CPU burst times for ea. process
        self.CPU_bursts = [[] for i in range(self.numProc)]
        
        #2d list of I/O burst times for ea. process
        self.IO_bursts = [[] for i in range(self.numProc)]
        
        #list of the respective amounts of CPU bursts for 
        #each process
        self.no_bursts = []
        for i in range(self.numProc):
            self.arr_time.append(math.floor(self.get_exp()))
            self.no_bursts.append(math.ceil(self.rand.drand()*100))
            for j in range (self.no_bursts[i]-1):
                self.CPU_bursts[i].append(math.ceil(self.get_exp()))
                self.IO_bursts[i].append(math.ceil(self.get_exp())*10)
            self.CPU_bursts[i].append(math.ceil(self.get_exp()))
            
    def print_(self):
        # print process CPU and I/O times in correct format
        for i in range(self.numProc):
            print("Process ",chr(65+i),": arrival time ",self.arr_time[i],"ms; tau ",self.tau,"ms; ", self.no_bursts[i]," CPU bursts:",sep="")
            
            for j in range(self.no_bursts[i]-1):
                print("--> CPU burst ", self.CPU_bursts[i][j],"ms --> I/O burst ",self.IO_bursts[i][j],"ms",sep="")
                
            print("--> CPU burst ", self.CPU_bursts[i][self.no_bursts[i]-1],"ms",sep="")
            
        return self.arr_time, self.CPU_bursts, self.IO_bursts, self.no_bursts
    
    def get_tau(self):
        return self.tau

    def set_tau(self, val):
        self.tau = val

if __name__ == "__main__":
    "Tester code"
    numProc, seed_no, lambda_, upp_bound, cont_switch, alpha, t_slice  = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
    
    processes = ProcessSet(numProc,lambda_,seed_no, upp_bound)
    processes.generate()
    arr_times, CPU_bursts, IO_bursts, no_bursts = processes.print_()
    print("list of arrival times:",arr_times)
    print("lists of CPU bursts:",CPU_bursts)
    print("lists of I/O bursts:",IO_bursts)
    print("list of amounts of CPU bursts:",no_bursts)