import sys
import math
from ProcessSet import Rand48, ProcessSet
from fcfs import FCFS

def main():
    numProc = int(sys.argv[1])
    seed_no = int(sys.argv[2])
    lambda_ = float(sys.argv[3])
    upp_bound = int(sys.argv[4])
    cont_switch = int(sys.argv[5])
    alpha = float(sys.argv[6])
    t_slice = int(sys.argv[7])

    processes = ProcessSet(numProc,lambda_,seed_no, upp_bound)
    processes.generate()
    arr_times, CPU_bursts, IO_bursts, no_bursts = processes.print_()
    
    FCFS(numProc, arr_times, CPU_bursts, IO_bursts, no_bursts, cont_switch)
    # insert SJF here
    # insert SRT here
    # insert RR here

    # Write file writing code for averages

if __name__ == "__main__":
    main()