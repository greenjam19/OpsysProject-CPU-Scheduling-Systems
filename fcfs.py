from concurrent.futures import process
import math
from multiprocessing.dummy import current_process
import sys
from tracemalloc import start
from ProcessSet import *


def FCFS(numProc, arr_time_p, CPU_bursts_p, IO_bursts_p, no_bursts_p, cont_switch_time):
    current_time = 0
    completed_procs = 0
    wait_time = 0
    wait_time_2 = 0
    wait_time_3 = 0
    add_time = True
    
    arr_time = arr_time_p
    CPU_bursts = CPU_bursts_p
    IO_bursts = IO_bursts_p
    no_bursts = no_bursts_p
    
    in_burst = False
    
    current_proc = ';'
    
    start_burst_time = 0
    
    context_switches = 0
    
    queue = []
    
    wait_times = list(-1 for i in range(0, numProc))
    
    proc_idx = 0
    
    print("time ", current_time, "ms: Simulator started for FCFS [Q: empty]", sep="")
    
    while (True):
        #* Check if anything in arr_time is still there, if so check if at or past that arrive time, print out and pop from arr_time, and add to queue
        if (len(arr_time) != 0):
            for i in range(len(arr_time)):
                if (current_time == arr_time[i]):
                    queue.append(chr(65 + i))
                    print("time ", current_time, "ms: Process ", chr(65 + i), " arrived; added to ready queue [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                    wait_time = int(cont_switch_time / 2)

        #* 
        if (len(queue) != 0 and in_burst == False and wait_time == 0 and wait_time_2 == 0 and wait_time_3 == 0):
            current_proc = queue[0]
            proc_idx = ord(current_proc) - 65
            queue.pop(0)
            if (len(queue) == 0):
                print("time ", current_time, "ms: Process ", current_proc, " started using the CPU for ", CPU_bursts[proc_idx][0], "ms burst [Q: empty]", sep='')
                
            else:
                print("time ", current_time, "ms: Process ", current_proc, " started using the CPU for ", CPU_bursts[proc_idx][0], "ms burst [Q: ", sep='', end='')
                print(*queue, end='')
                print("]")
            in_burst = True
            start_burst_time = current_time

        #* Checking if current_burst has ended, prints out completed and switches out of CPU
        elif (in_burst == True and (CPU_bursts[proc_idx][0] + start_burst_time) == current_time and wait_time == 0):
            CPU_bursts[proc_idx].pop(0)
            in_burst = False
            
            #? Checking if we need to print a plural 'burst(s)'
            plural = 's'
            if (len(CPU_bursts[proc_idx]) == 1):
                plural = ''

            
            if (len(CPU_bursts[proc_idx]) != 0):
                wait_times[proc_idx] = int(cont_switch_time / 2) + current_time + IO_bursts[proc_idx][0]
                if (len(queue) == 0):
                    print("time ", current_time, "ms: Process ", current_proc, " completed a CPU burst; ", len(CPU_bursts[proc_idx]), " burst", plural, " to go [Q: empty]", sep='')
                    print("time ", current_time, "ms: Process ", current_proc, " switching out of CPU; will block on I/O until time ", wait_times[proc_idx], "ms [Q: empty]", sep='')
                else:
                    print("time ", current_time, "ms: Process ", current_proc, " completed a CPU burst; ", len(CPU_bursts[proc_idx]), " burst", plural, " to go [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                    print("time ", current_time, "ms: Process ", current_proc, " switching out of CPU; will block on I/O until time ", wait_times[proc_idx], "ms [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
            
            else:
                if (len(queue) == 0):
                    print("time ", current_time, "ms: Process ", current_proc, " terminated [Q: empty]", sep='')
                else:
                    print("time ", current_time, "ms: Process ", current_proc, " terminated [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                completed_procs += 1
            
            wait_time_2 = cont_switch_time
            

        #* Check if anything in wait times is the current time, if so print out I/O burst completecd and add proccess to queue (if CPU burst has stuff still)
        for i in range(len(wait_times)):
            if (wait_times[i] == current_time):
                queue.append(chr(65 + i))
                print("time ", current_time, "ms: Process ", chr(65 + i), " completed I/O; added to ready queue [Q: ", sep='', end='')
                print(*queue, end='')
                print("]")
                wait_times[i] = -1
                #current_time += int(cont_switch_time / 2)
                #add_time = False
                IO_bursts[i].pop(0)
                wait_time_3 = int(cont_switch_time / 2)
                
        if (completed_procs == numProc):
            current_time += int(cont_switch_time / 2)
            break

        if (wait_time != 0):
            wait_time -= 1
        
        if (wait_time_2 != 0):
            wait_time_2 -= 1

        if (wait_time_3 != 0):
            wait_time_3 -= 1

        if (add_time == True):
            current_time += 1
        else:
            add_time = True
    
    
    print("time ", current_time, "ms: Simulator ended for FCFS [Q: empty]", sep='')
    
    
    
def main():
    print("Main start:")

    numProc, seed_no, lambda_, upp_bound, cont_switch, alpha, t_slice  = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
    processes = ProcessSet(numProc,lambda_,seed_no, upp_bound)
    processes.generate()
    arr_time, CPU_bursts, IO_bursts, no_bursts = processes.print_()
    
    FCFS(numProc, arr_time, CPU_bursts, IO_bursts, no_bursts, cont_switch)

if __name__ == "__main__":
    main()