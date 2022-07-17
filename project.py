import functools
from ProcessSet import *
from FCFS import FCFS
from SJF import SJF
from RR import RR
from SRT import SRT
from Stats import *
import sys
print = functools.partial(print, flush=True)

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
def main():
        if len(sys.argv)<8:
                stats()
                sys.stderr.write("ERROR: Invalid arguments\n")
                sys.exit(2)
        elif not sys.argv[1].isdigit() or not sys.argv[2].isdigit() or not isfloat(sys.argv[3]) \
        or not sys.argv[4].isdigit() or not sys.argv[5].isdigit() or not isfloat(sys.argv[6]) \
        or not sys.argv[7].isdigit():
                stats()
                sys.stderr.write("ERROR: Invalid arguments\n")
                sys.exit(2)

        num_procs= int(sys.argv[1])
        seed_no = int(sys.argv[2])
        lambda_ = float(sys.argv[3])
        upp_bound = int(sys.argv[4])
        cont_switch = int(sys.argv[5])
        alpha = float(sys.argv[6])
        t_slice  = int(sys.argv[7])

        invalid_vals = num_procs<1 or num_procs>26 or seed_no < 0 or lambda_ <= 0 or upp_bound < 0 or cont_switch % 2 != 0 or cont_switch <= 0 or alpha < 0 or t_slice<0
        if invalid_vals:
                stats()
                sys.stderr.write("ERROR: Invalid argument\n")
                sys.exit(2)
        
        processes = ProcessSet(num_procs,lambda_,seed_no, upp_bound)
        processes.generate()
        arr_time, CPU_bursts, IO_bursts, no_bursts = processes.print_()
        tau_inits = [processes.get_tau() for i in range(num_procs)]
        sys_avg_CPU_burst_time = processes.get_avg_Burst_time()

        try: 
                FCFS_cont_switches,FCFS_avg_wait_time, FCFS_CPU_util, FCFS_avg_turnaround               = FCFS(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch)
                SJF_cont_switches, SJF_avg_wait_time, SJF_CPU_util, SJF_avg_turnaround                  = SJF(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch, alpha, tau_inits)
                SRT_cont_switches, SRT_avg_wait_time, SRT_CPU_util, SRT_num_preemps, SRT_avg_turnaround = SRT(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch, alpha, tau_inits)
                RR_cont_switches, RR_avg_wait_time, RR_CPU_util, RR_num_preemps, RR_avg_turnaround      = RR(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch, t_slice)
        except:
                stats()
                sys.exit(1)

        sys_cont_switches = [FCFS_cont_switches,SJF_cont_switches,SRT_cont_switches,RR_cont_switches]
        sys_avg_wait_times = [FCFS_avg_wait_time,SJF_avg_wait_time,SRT_avg_wait_time,RR_avg_wait_time]
        sys_CPU_util = [FCFS_CPU_util,SJF_CPU_util,SRT_CPU_util,RR_CPU_util]
        sys_num_preemps = [SRT_num_preemps,RR_num_preemps]
        sys_avg_turnaround_times = [FCFS_avg_turnaround ,SJF_avg_turnaround ,SRT_avg_turnaround ,RR_avg_turnaround ]
        Stats(sys_cont_switches,sys_avg_CPU_burst_time,sys_avg_wait_times,sys_CPU_util,sys_num_preemps,sys_avg_turnaround_times)

if __name__ == "__main__":
    main()