# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 15:50:39 2022

@author: greenj19
"""
import math
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
    
    def __init__(self, numProc, lambda_, seed_no):
        self.numProc = numProc
        self.lambda_= lambda_
        self.rand = Rand48(seed_no)
        self.rand.srand(19)
        self.tau = int(1/self.lambda_)
        
    def get_exp(self):
        return -math.log(self.rand.drand())/self.lambda_
    
    def generate(self):
        self.arr_time = []
        self.CPU_bursts = [[] for i in range(self.numProc)]
        self.IO_bursts = [[] for i in range(self.numProc)]
        self.no_bursts = []
        for i in range(self.numProc):
            self.arr_time.append(math.floor(self.get_exp()))
            self.no_bursts.append(math.ceil(self.rand.drand()*100))
            for j in range (self.no_bursts[i]-1):
                self.CPU_bursts[i].append(math.ceil(self.get_exp()))
                self.IO_bursts[i].append(math.ceil(self.get_exp())*10)
            self.CPU_bursts[i].append(math.ceil(self.get_exp()))
            
    def print_(self):
        for i in range(self.numProc):
            print("Process ",chr(65+i),": arrival time ",self.arr_time[i],"ms; tau = ",self.tau,"ms; ", self.no_bursts[i]," CPU bursts:",sep="")
            for j in range(self.no_bursts[i]-1):
                print("--> CPU burst ", self.CPU_bursts[i][j],"ms --> I/O burst ",self.IO_bursts[i][j],"ms",sep="")
            print("--> CPU burst ", self.CPU_bursts[i][self.no_bursts[i]-1],"ms",sep="")
            
def main():
    "Tester code"
    processes = ProcessSet(2,0.01,19)
    processes.generate()
    processes.print_()
if __name__ == "__main__":
    main()
            
            
        
        
    








