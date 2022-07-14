import sys
import math
from ProcessSet import ProcessSet
from fcfs import FCFS
from sjf import SJF
from rr import RR

def main():
    if (len(sys.argv) != 8):
        print("ERROR: Insufficient number of arguments")
        return 1

    numProc = int(sys.argv[1])
    seed_no = int(sys.argv[2])
    lambda_ = float(sys.argv[3])
    upp_bound = int(sys.argv[4])
    cont_switch = int(sys.argv[5])
    alpha = float(sys.argv[6])
    t_slice = int(sys.argv[7])

    processes = ProcessSet(numProc, lambda_, seed_no, upp_bound)
    processes.generate()
    arr_times, CPU_bursts, IO_bursts, no_bursts = processes.print_()
    
    # numProc, arr_times, CPU_bursts, IO_bursts, no_bursts, cont_switch
    FCFS(numProc, arr_times, CPU_bursts, IO_bursts, cont_switch)
    # insert SJF here
    tau_inits = [processes.get_tau() for i in range(numProc)]
    SJF(numProc, arr_times, CPU_bursts, IO_bursts, cont_switch, alpha, tau_inits)
    # 
    # insert SRT here
    # SRT(numProc, arr_times, CPU_bursts, IO_bursts, cont_switch, alpha, tau_inits)
    # 
    # insert RR here
    RR(numProc, arr_times, CPU_bursts, IO_bursts, cont_switch, t_slice)

    # Write file writing code for averages

if __name__ == "__main__":
    main()