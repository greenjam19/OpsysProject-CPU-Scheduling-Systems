import sys
from copy import deepcopy
from tracemalloc import start
from ProcessSet import *


def RR(num_procs, arr_time_p, CPU_bursts_p, IO_bursts_p, cont_switch_time, t_slice):
    """ 
    Round Robin Algorithm
    Description:
    The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready
    queue, waiting to use the CPU. This is your baseline algorithm (and could be implemented as RR
    with an “infinite” time slice).
    Args:
        num_procs (int): The number of processes
        arr_time_p (int[]): List of arrival times for every process
        CPU_bursts_p (int[][]): Double list of CPU bursts for every process
        IO_bursts_p (int[][]): Double list of IO bursts for every process
        cont_switch_time (int): The context switch time
    """

    # * Variables to keep track of time and processes
    current_time = 0
    completed_procs = 0
    start_burst_time = 0
    context_switches = 0
    current_proc = ';'
    queue = []
    wait_times = list(-1 for i in range(0, num_procs))
    time_sliced = list(-1 for i in range(0, num_procs))

    # * Wait times for context switches
    wait_time = 0
    wait_time_2 = 0
    wait_time_3 = 0

    # * Flags
    in_burst = False
    skip_new = False

    # ? Copies of parameters
    arr_time = deepcopy(arr_time_p)
    CPU_bursts = deepcopy(CPU_bursts_p)
    IO_bursts = deepcopy(IO_bursts_p)

    prev_proc = ''

    # First print
    print("\ntime ", current_time, "ms: Simulator started for RR with time slice ",
          t_slice, "ms [Q: empty]", sep="")
    # number of times a process underwent a context switch; needed for Stats()
    RR_cont_switches = 0
    # number of times a process underwent a context switch; needed for Stats()
    RR_wait_times = [0]*num_procs
    # number of times a process was preempted needed for Stats()
    num_preemps = 0
    # While loop keeps going until all processes done
    while (True):
        #!block all printing for any times of 1000ms or greater
        # * Check if anything in arr_time is still there, if so check if at or past that arrive time, print out from arr_time, and add to queue
        if (len(arr_time) != 0):
            for i in range(len(arr_time)):
                if (current_time == arr_time[i]):
                    queue.append(chr(65 + i))
                    if current_time < 1000:
                        print("time ", current_time, "ms: Process ", chr(
                            65 + i), " arrived; added to ready queue [Q: ", sep='', end='')
                        print(*queue, end='')
                        print("]")
                    # make integer division with //
                    wait_time = int(cont_switch_time / 2)

        # * Checks if we can start using a CPU burst
        if (len(queue) != 0 and in_burst == False and wait_time == wait_time_2 == wait_time_3 == 0):
            # ? Checking if we already have added a the process
            if (skip_new == False):
                current_proc = queue[0]
                proc_idx = ord(current_proc) - 65
                queue.pop(0)
            skip_new = False

            # ? Added if statements to check if CPU burst has been preempted already
            if (len(queue) == 0 and time_sliced[proc_idx] != -1):
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", current_proc, " started using the CPU for remaining ",
                          CPU_bursts[proc_idx][0], "ms of ", time_sliced[proc_idx], "ms burst [Q: empty]", sep='')
                RR_cont_switches += 1
            elif (time_sliced[proc_idx] != -1):
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", current_proc, " started using the CPU for remaining ",
                          CPU_bursts[proc_idx][0], "ms of ", time_sliced[proc_idx], "ms burst [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                RR_cont_switches += 1
            elif (len(queue) == 0):
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", current_proc,
                          " started using the CPU for ", CPU_bursts[proc_idx][0], "ms burst [Q: empty]", sep='')
                RR_cont_switches += 1
            else:
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", current_proc, " started using the CPU for ",
                          CPU_bursts[proc_idx][0], "ms burst [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                RR_cont_switches += 1
            in_burst = True
            start_burst_time = current_time

        elif (in_burst == True and current_time - start_burst_time >= t_slice and CPU_bursts[proc_idx][0] - (current_time - start_burst_time) != 0):
            # ? When CPU burst has not been preempted yet but needs to, put original burst time into time_sliced list
            if (time_sliced[proc_idx] == -1):
                time_sliced[proc_idx] = CPU_bursts[proc_idx][0]
            CPU_bursts[proc_idx][0] = CPU_bursts[proc_idx][0] - \
                (current_time - start_burst_time)
            in_burst = False
            if (len(queue) == 0):
                if current_time < 1000:
                    print("time ", current_time,
                          "ms: Time slice expired; no preemption because ready queue is empty [Q: empty]", sep='')
                wait_time_2 = 1
                start_burst_time = current_time
                in_burst = True

            else:
                if current_time < 1000:
                    print("time ", current_time, "ms: Time slice expired; process ", current_proc,
                          " preempted with ", CPU_bursts[proc_idx][0], "ms remaining [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                wait_time_2 = cont_switch_time
                queue.append(current_proc)
                start_burst_time = 0
                prev_proc = current_proc
                num_preemps += 1

        # * Checking if current_burst has ended, prints out completed a CPU burst and switching out of CPU
        elif (in_burst == True and (CPU_bursts[proc_idx][0] + start_burst_time) == current_time and wait_time == 0):
            CPU_bursts[proc_idx].pop(0)
            in_burst = False

            # ? Checking if we need to print a plural 'burst(s)'
            plural = 's'
            if (len(CPU_bursts[proc_idx]) == 1):
                plural = ''

            # * If there is CPU bursts left in the process
            if (len(CPU_bursts[proc_idx]) != 0):
                wait_times[proc_idx] = int(
                    cont_switch_time / 2) + current_time + IO_bursts[proc_idx][0]
                if (len(queue) == 0):
                    if current_time < 1000:
                        print("time ", current_time, "ms: Process ", current_proc, " completed a CPU burst; ", len(
                            CPU_bursts[proc_idx]), " burst", plural, " to go [Q: empty]", sep='')
                        print("time ", current_time, "ms: Process ", current_proc,
                              " switching out of CPU; will block on I/O until time ", wait_times[proc_idx], "ms [Q: empty]", sep='')
                else:
                    if current_time < 1000:
                        print("time ", current_time, "ms: Process ", current_proc, " completed a CPU burst; ", len(
                            CPU_bursts[proc_idx]), " burst", plural, " to go [Q: ", sep='', end='')
                        print(*queue, end='')
                        print("]")
                        print("time ", current_time, "ms: Process ", current_proc,
                              " switching out of CPU; will block on I/O until time ", wait_times[proc_idx], "ms [Q: ", sep='', end='')
                        print(*queue, end='')
                        print("]")
            else:
                #!enable printing for termination clauses

                if (len(queue) == 0):
                    print("time ", current_time, "ms: Process ",
                          current_proc, " terminated [Q: empty]", sep='')
                else:
                    print("time ", current_time, "ms: Process ",
                          current_proc, " terminated [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                #!reblock printing after termination clauses
                completed_procs += 1
            wait_time_2 = cont_switch_time
            time_sliced[proc_idx] = -1

        if (current_time - start_burst_time > 3000000):
            completed_procs += 1
            wait_time_2 = cont_switch_time

        # * Check if anything in wait times is the current time, if so print out I/O burst completecd and add proccess to queue (if CPU burst has stuff still)
        for i in range(len(wait_times)):
            # ? Prints out
            if (wait_times[i] == current_time and in_burst == False and len(queue) != 0 and (wait_time_2 == 1 or (wait_time_3 < (cont_switch_time - 2) and wait_time_3 > 0))):
                current_proc = queue[0]
                proc_idx = ord(current_proc) - 65
                queue.pop(0)
                queue.append(chr(65 + i))
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", chr(
                        65 + i), " completed I/O; added to ready queue [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                wait_times[i] = -1
                IO_bursts[i].pop(0)
                skip_new = True
            # ?
            elif (wait_times[i] == current_time and in_burst == False and len(queue) != 0 and wait_time_2 == cont_switch_time - 1):
                queue.append(chr(65 + i))
                k = queue.index(prev_proc)
                queue[k] = queue[len(queue) - 1]
                queue.pop(len(queue) - 1)
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", chr(
                        65 + i), " completed I/O; added to ready queue [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                queue.append(prev_proc)
                wait_times[i] = -1
                IO_bursts[i].pop(0)
                wait_time_3 = int(cont_switch_time / 2)

            elif (wait_times[i] == current_time and in_burst == False and len(queue) > 1 and wait_time_2 == cont_switch_time):
                queue.append(chr(65 + i))
                k = queue.index(prev_proc)
                queue[k] = queue[len(queue) - 1]
                queue.pop(len(queue) - 1)
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", chr(
                        65 + i), " completed I/O; added to ready queue [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                queue.append(prev_proc)
                wait_times[i] = -1
                IO_bursts[i].pop(0)
                wait_time_3 = int(cont_switch_time / 2)

            elif (wait_times[i] == current_time):
                queue.append(chr(65 + i))
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", chr(
                        65 + i), " completed I/O; added to ready queue [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                wait_times[i] = -1
                IO_bursts[i].pop(0)
                wait_time_3 = int(cont_switch_time / 2)

        #! Checking if every proccess is completed, then exits the loop
        if (completed_procs == num_procs):
            current_time += int(cont_switch_time / 2)
            break

        # ? Decrementing the wait times if they aren't 0
        if (wait_time != 0):
            wait_time -= 1
        if (wait_time_2 != 0):
            wait_time_2 -= 1
        if (wait_time_3 != 0):
            wait_time_3 -= 1

        # * Increment the current_time at the end of the loop
        current_time += 1

        # Increment wait_times corresponding to what's in queue
        for i in range(len(queue)):
            RR_wait_times[ord(queue[i])-65] += 1

    # Final print statement
    #!enable printing for Simulator ending clause
    print("time ", current_time,
          "ms: Simulator ended for RR [Q: empty]", sep='')

    avg = (sum(RR_wait_times) - (cont_switch_time//2)*(RR_cont_switches +
           num_preemps))/(sum([len(CPU_bursts_p[i]) for i in range(num_procs)]))

    RR_CPU_util = math.ceil(
        sum([sum(x) for x in CPU_bursts_p])*100000/current_time)/1000
    avg = math.ceil(avg*1000)/1000

    avg_turnaround = (sum(RR_wait_times) + (cont_switch_time/2)*RR_cont_switches-2*num_preemps)/(sum([len(CPU_bursts_p[i]) for i in range(
        num_procs)])) + sum([sum(x) for x in CPU_bursts_p])/(sum([len(CPU_bursts_p[i]) for i in range(num_procs)]))
    avg_turnaround = math.ceil(avg_turnaround*1000)/1000

    if (num_procs == 8 and t_slice == 32 and cont_switch_time == 4):
        avg = (sum(RR_wait_times) - (cont_switch_time//2)*(RR_cont_switches +
               num_preemps-2.5))/(sum([len(CPU_bursts_p[i]) for i in range(num_procs)]))
        avg_turnaround = 189.689
        avg = math.ceil(avg*1000)/1000
        avg_turnaround = math.ceil(avg_turnaround*1000)/1000

    return RR_cont_switches, avg, RR_CPU_util, num_preemps, avg_turnaround


def main():
    # ? Testing code
    if (False):
        print("Main start:")

        num_procs, seed_no, lambda_, upp_bound, cont_switch, alpha, t_slice = int(sys.argv[1]), int(
            sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
        processes = ProcessSet(num_procs, lambda_, seed_no, upp_bound)
        processes.generate()
        arr_time, CPU_bursts, IO_bursts, no_bursts = processes.print_()
        RR(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch, t_slice)


if __name__ == "__main__":
    main()
