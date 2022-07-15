from ProcessSet import *
from FCFS import FCFS
from SJF import SJF
from RR import RR
#TODO finish this
from SRT import SRT
#TODO finish this
from Stats import Stats
import sys

def main():
        num_procs= int(sys.argv[1])
        seed_no = int(sys.argv[2])
        lambda_ = float(sys.argv[3])
        upp_bound = int(sys.argv[4])
        cont_switch = int(sys.argv[5])
        alpha = float(sys.argv[6])
        t_slice  = int(sys.argv[7])
        
        processes = ProcessSet(num_procs,lambda_,seed_no, upp_bound)
        processes.generate()
        arr_time, CPU_bursts, IO_bursts, no_bursts = processes.print_()

        tau_inits = [processes.get_tau() for i in range(num_procs)]

        #FCFS(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch)
        #SJF(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch, alpha, tau_inits)
        SRT(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch, alpha, tau_inits)
        #RR(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch, t_slice)
        #Stats(output1, output2, output3, output4)
        Stats()

if __name__ == "__main__":
    main()