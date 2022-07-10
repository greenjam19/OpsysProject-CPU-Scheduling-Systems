import sys
from ProcessSet import *

def FCFS(num_procs, arr_time_p, CPU_bursts_p, IO_bursts_p, cont_switch_time):
    """ 
    First Come First Serve Algorithm

    Args:
        num_procs (int): The number of processes
        arr_time_p (int[]): List of arrival times for every process
        CPU_bursts_p (int[][]): Double list of CPU bursts for every process
        IO_bursts_p (int[][]): Double list of IO bursts for every process
        cont_switch_time (int): The context switch time
    """

    #* Variables to keep track of time and processes
    current_time = 0
    completed_procs = 0
    start_burst_time = 0
    context_switches = 0
    current_proc = ';'
    queue = []
    wait_times = list(-1 for i in range(0, num_procs))

    #* Wait times for context switches
    wait_time = 0
    wait_time_2 = 0
    wait_time_3 = 0

    #* Flags
    in_burst = False
    
    #? Copies of parameters
    arr_time = arr_time_p
    CPU_bursts = CPU_bursts_p
    IO_bursts = IO_bursts_p

    # First print
    print("\ntime ", current_time, "ms: Simulator started for FCFS [Q: empty]", sep="")

    # While loop keeps going until all processes done
    while (True):
        #* Check if anything in arr_time is still there, if so check if at or past that arrive time, print out from arr_time, and add to queue
        if (len(arr_time) != 0):
            for i in range(len(arr_time)):
                if (current_time == arr_time[i]):
                    queue.append(chr(65 + i))
                    print("time ", current_time, "ms: Process ", chr(65 + i), " arrived; added to ready queue [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                    # make integer division with //
                    wait_time = int(cont_switch_time / 2)

        #* Checks if we can start using a CPU burst
        if (len(queue) != 0 and in_burst == False and wait_time == wait_time_2 == wait_time_3 == 0):
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

        #* Checking if current_burst has ended, prints out completed a CPU burst and switching out of CPU
        elif (in_burst == True and (CPU_bursts[proc_idx][0] + start_burst_time) == current_time and wait_time == 0):
            CPU_bursts[proc_idx].pop(0)
            in_burst = False

            #? Checking if we need to print a plural 'burst(s)'
            plural = 's'
            if (len(CPU_bursts[proc_idx]) == 1):
                plural = ''

            #* If there is CPU bursts left in the process
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
                IO_bursts[i].pop(0)
                wait_time_3 = int(cont_switch_time / 2)

        #! Checking if every proccess is completed, then exits the loop
        if (completed_procs == num_procs):
            current_time += int(cont_switch_time / 2)
            break

        #? Decrementing the wait times if they aren't 0
        if (wait_time != 0):
            wait_time -= 1
        if (wait_time_2 != 0):
            wait_time_2 -= 1
        if (wait_time_3 != 0):
            wait_time_3 -= 1

        #* Increment the current_time at the end of the loop
        current_time += 1
        

    # Final print statement
    print("time ", current_time, "ms: Simulator ended for FCFS [Q: empty]", sep='')

def main():
    #? Testing code
    if (False):
        print("Main start:")

        num_procs, seed_no, lambda_, upp_bound, cont_switch, alpha, t_slice  = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
        processes = ProcessSet(num_procs,lambda_,seed_no, upp_bound)
        processes.generate()
        arr_time, CPU_bursts, IO_bursts, no_bursts = processes.print_()
        FCFS(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch)

if __name__ == "__main__":
    main()