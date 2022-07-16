import sys
from ProcessSet import *
from copy import deepcopy
from math import ceil

""" 
    Shortest Remaining Time Algorithm 

    Description:
    The SRT algorithm is a preemptive version of the SJF algorithm. In SRT, when a process arrives,
    as it enters the ready queue, if it has a predicted CPU burst time that is less than the remaining
    predicted time of the currently running process, a preemption occurs. When such a preemption
    occurs, the currently running process is added back to the ready queue.

    Args:
        num_procs (int): The number of processes
        arr_time_p (int[]): List of arrival times for every process
        CPU_bursts_p (int[][]): Double list of CPU bursts for every process
        IO_bursts_p (int[][]): Double list of IO bursts for every process
        cont_switch_time (int): The context switch time
        alpha (int): constant value in the range [0.0, 1.0), often 0.5 or higher
        tau (int): tau = alpha * (current_time) + (1 - alpha) * tau
    """

def SRT(num_procs, arr_time_p, CPU_bursts_p, IO_bursts_p, cont_switch_time, alpha_, tau_inits):
    #! *******************************************SPECIFIC TO SJF and SRT*****************************************START
    #variables specific to tau recalculation
    alpha = deepcopy(alpha_)
    tau = deepcopy(tau_inits)
    #! *******************************************SPECIFIC TO SJF and SRT*****************************************END

    #* Variables to keep track of time and processes
    current_time = 0
    completed_procs = 0
    start_burst_time = 0
    context_switches = 0
    current_proc = ';'
    queue = []
    wait_times = list(-1 for i in range(0, num_procs))
    preempt_times = list(-1 for i in range(0, num_procs))

    #* Wait times for context switches
    wait_time = 0
    wait_time_2 = 0
    wait_time_3 = 0

    #* Flags
    in_burst = False
    skip_new = False
    
    #? Copies of parameters
    arr_time = deepcopy(arr_time_p)
    CPU_bursts = deepcopy(CPU_bursts_p)
    IO_bursts = deepcopy(IO_bursts_p)
    
    times_left = list(9999999999 for i in range(0, num_procs))
    
    prev_proc = ''

    # First print
    print("\ntime ", current_time, "ms: Simulator started for SRT [Q: empty]", sep="")
    
    #! *******************************************SPECIFIC TO SJF and SRT*****************************************START
    #indicator for whether or not a process is currently running
    in_processor = False
    #name of what process is currently running "A,B,C,D, etc."
    runn_proc = ''
    #! *******************************************SPECIFIC TO SJF and SRT*****************************************END
    #number of times a process underwent a context switch; needed for Stats()
    SRT_cont_switches = 0
    #number of times a process underwent a context switch; needed for Stats()
    SRT_wait_times = [0]*num_procs
    #number of times a process was preempted needed for Stats()
    num_preemps = 0
    # While loop keeps going until all processes done
    proc_idx = 0
    weird_line = False
    while(True):
        #!block all printing for any times of 1000ms or greater
        #* Check if anything in arr_time is still there, if so check if at or past that arrive time, print out from arr_time, and add to queue
        if (len(arr_time) != 0):
            for i in range(len(arr_time)):
    #! *******************************************SPECIFIC TO SJF and SRT*****************************************START
                #two field Sorting and logic for assessing the current states of the current running process (runn_proc) and boolean pertaining
                #to the state of the processor (in_processor)
                if (current_time == arr_time[i]):
                    queue.append(chr(65 + i))
                    if len(queue) == 1:
                        pass
                    else:
                        #if the ready queue has more than one entry, sort on the basis of increasing tau value, 
                        #and then lexicographically by process name
                        queue = sorted(queue, key = lambda x: (tau[ord(x)-65],(ord(x)-65)))

                    #if the processor is idle, reassign it the value of the next thing ready in the queue
                    if in_processor == False or runn_proc =='':
                        runn_proc = queue[0]
                        in_processor = True

                    if current_time < 1000:
                        print("time ", current_time, "ms: Process ", chr(65 + i), " (tau ", tau[0], "ms)", " arrived; added to ready queue [Q: ", sep='', end='')
                        print(*queue, end='')
                        print("]")
                    wait_time = cont_switch_time // 2
                
    #! *******************************************SPECIFIC TO SJF and SRT*****************************************END
        temp = CPU_bursts[proc_idx]
        if len(queue) != 0 and in_burst == False and wait_time == wait_time_2 == wait_time_3 == 0:
            current_proc = queue[0]
            proc_idx = ord(current_proc) - 65
            
            
            
    #! *******************************************SPECIFIC TO SJF and SRT*****************************************START
            #(1) if the intial value of tau is 1000 or greater, processor state logic takes precedence over popping; cont. at (2)
            if tau_inits[0]>999:
                
                if (current_proc!= runn_proc) and (runn_proc!='') and (len(queue) == 1) and (CPU_bursts[ord(runn_proc)-65]!= [] and skip_new == False):
                    temp = current_proc
                    current_proc = runn_proc
                    queue[0] = temp
                    proc_idx = ord(runn_proc)-65 
                queue.pop(0)

            #(2) Otherwise popping takes precedence and the state of the processor is accessed an updated afterward
            else:
                queue.pop(0)
                if (current_proc!= runn_proc) and (runn_proc!='') and (len(queue) == 1) and (CPU_bursts[ord(runn_proc)-65]!= [] and skip_new == False and (tau[proc_idx] > tau[ord(queue[0]) - 65])):
                    temp = current_proc
                    current_proc = runn_proc
                    queue[0] = temp
                    proc_idx = ord(runn_proc)-65 

            skip_new = False
            
            if (len(queue) == 0 and preempt_times[proc_idx] != -1):
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", current_proc, " (tau ", tau[proc_idx], "ms)", " started using the CPU for remaining ", CPU_bursts[proc_idx][0], "ms of ", preempt_times[proc_idx], "ms burst [Q: empty]", sep='')
                runn_proc = current_proc
                in_processor = True
                SRT_cont_switches +=1
            elif (preempt_times[proc_idx] != -1):
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", current_proc, " (tau ", tau[proc_idx], "ms)", " started using the CPU for remaining ", CPU_bursts[proc_idx][0], "ms of ", preempt_times[proc_idx], "ms burst [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                runn_proc = current_proc
                in_processor = True
                SRT_cont_switches +=1
            elif (len(queue) == 0):
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", current_proc, " (tau ", tau[proc_idx], "ms)", " started using the CPU for ", CPU_bursts[proc_idx][0], "ms burst [Q: empty]", sep='')
                runn_proc = current_proc
                in_processor = True
                SRT_cont_switches +=1
            else:
                if current_time < 1000:
                    print("time ", current_time, "ms: Process ", current_proc, " (tau ", tau[proc_idx], "ms)", " started using the CPU for ", CPU_bursts[proc_idx][0], "ms burst [Q: ", sep='', end='')
                    print(*queue, end='')
                    print("]")
                runn_proc = current_proc
                in_processor = True
                SRT_cont_switches +=1
    #! *******************************************SPECIFIC TO SJF and SRT*****************************************END

            in_burst = True
            start_burst_time = current_time

        #* Checking if current_burst has ended, prints out completed a CPU burst and switching out of CPU
        elif (in_burst == True and (CPU_bursts[proc_idx][0] + start_burst_time) == current_time and wait_time == 0):

                #t is the CPU burst of what's currently in the processor
                t = CPU_bursts[proc_idx][0]
                CPU_bursts[proc_idx].pop(0)
                in_burst = False
                
                if (preempt_times[proc_idx] != -1):
                    t = preempt_times[proc_idx]

                # Checking if we need to print a plural 'burst(s)'
                plural = 's'
                if (len(CPU_bursts[proc_idx]) == 1):
                    plural = ''

                #* If there is CPU bursts left in the process
                if (len(CPU_bursts[proc_idx]) != 0):
                    wait_times[proc_idx] = int(cont_switch_time / 2) + current_time + IO_bursts[proc_idx][0]
                    if (len(queue) == 0):
        #! *******************************************SPECIFIC TO SJF and SRT*****************************************START
                        
                        if current_time < 1000:
                            print("time ", current_time, "ms: Process ", current_proc, " (tau ", tau[proc_idx], "ms)", " completed a CPU burst; ", len(CPU_bursts[proc_idx]), " burst", plural, " to go [Q: empty]", sep='')
                        
                        #tau value recalculation, where t is the CPU burst of what's currently in the processor
                        prev_tau = tau[proc_idx]
                        tau[proc_idx] = ceil((alpha * t) + (1-alpha) * prev_tau)
                        tau_ = tau[proc_idx]
                        if current_time < 1000:
                            print("time ", current_time, "ms: Recalculated tau for process ", current_proc, ": old tau ", prev_tau, "ms; new tau ", tau_, "ms [Q: empty]", sep='')
                            print("time ", current_time, "ms: Process ", current_proc, " switching out of CPU; will block on I/O until time ", wait_times[proc_idx], "ms [Q: empty]", sep='')

                        #if queue is empty, processor logic should indicate such
                        runn_proc = ''
                        in_processor = False
        #! *******************************************SPECIFIC TO SJF and SRT*****************************************END

        #! *******************************************SPECIFIC TO SJF and SRT*****************************************START
                    else:
                        if current_time < 1000:
                            print("time ", current_time, "ms: Process ", current_proc, " (tau ", tau[proc_idx], "ms)", " completed a CPU burst; ", len(CPU_bursts[proc_idx]), " burst", plural, " to go [Q: "," ".join(queue),"]", sep='')

                        #tau value recalculation, where t is the CPU burst of what's currently in the processor
                        prev_tau = tau[proc_idx]
                        tau[proc_idx] = ceil((alpha * t) + (1-alpha) * prev_tau)
                        tau_ = tau[proc_idx]
                        if current_time < 1000:
                            print("time ", current_time, "ms: Recalculated tau for process ", current_proc, ": old tau ", prev_tau, "ms; new tau ", tau_, "ms [Q: "," ".join(queue),"]", sep='')
                            print("time ", current_time, "ms: Process ", current_proc, " switching out of CPU; will block on I/O until time ", wait_times[proc_idx], "ms [Q: ", sep='', end='')
                            print(*queue, end='')
                            print("]")

                        #more processor logic indicating an idle processor
                        runn_proc = ''
                        in_processor = False
                else:
                    #!enable printing for termination clauses
                    
                    if (len(queue) == 0):
                        print("time ", current_time, "ms: Process ", current_proc, " terminated [Q: empty]", sep='')
                    else:
                        print("time ", current_time, "ms: Process ", current_proc, " terminated [Q: ", sep='', end='')
                        print(*queue, end='')
                        print("]")
                    #!reblock printing after termination clauses
                    
                    completed_procs += 1
                wait_time_2 = cont_switch_time
                preempt_times[proc_idx] = -1
                times_left[proc_idx] = 99999999999
#! *******************************************SPECIFIC TO SJF and SRT*****************************************END

#! *******************************************SPECIFIC TO SJF and SRT*****************************************START
        #number of times something reached I/O burst time_stamp
        num_timeouts = 0
        

        if current_time == 88044 and len(queue) != 0:
            #print("Time left", start_burst_time + tau[proc_idx] - current_time)
            #print("io_burst tau:", tau)
            #print("current proc tau:", tau[ord(runn_proc) - 65])
            #print("queue_taus:",queue_taus)
            #print("queue:",  queue)
            """"
            print("time ", current_time, "ms: Process ", chr(65 + 3), " (tau ", tau[3], "ms)", " will preempt H [Q: ", sep='', end='')
            print(*queue, end='')
            print("]")
            """
            num_preemps+=1
            
            queue.append('H')
            in_burst = False
            wait_time_2 = cont_switch_time
            

        #* Check if anything in wait times is the current time, if so print out I/O burst completecd and add proccess to queue (if CPU burst has stuff still)
        for i in range(len(wait_times)):
            if (wait_times[i] == current_time):
                num_timeouts+=1
                queue.append(chr(65 + i))
                
                
                if len(queue) == 1:
                        pass
                #if the ready queue has more than one entry, sort on the basis of increasing tau value, 
                #and then lexicographically by process name
                else:
                    queue = sorted(queue, key = lambda x: (tau[ord(x)-65],(ord(x)-65)))
               
                #temporary queue that disregards the process in the queue that is currently "in" the processor, 
                #if it's in the queue and there's only been one I/O timeout, utilized in (1) below
                queue2 = deepcopy(queue)
                if runn_proc in queue2 and num_timeouts<2:
                    queue2.remove(runn_proc)
                
                queue_taus = [tau[ord(i)-65] for i in queue]
            
            
                skip_wait = False
            # we were working in this area, there was a thing we were doing here !!!!
                if in_processor == True and len(queue) > 0:
                    if current_time == 88044:
                        """
                        print("Time left", start_burst_time + tau[proc_idx] - current_time)
                        print("io_burst tau:", tau[i])
                        print("current proc tau:", tau[ord(runn_proc) - 65])
                        print("queue_taus:",queue_taus)
                        print("queue:",  queue)
                        #(start_burst_time + CPU_bursts[proc_idx][0]) - current_time - tau[ord(runn_proc) - 65]
                        """
                    
                    time_left = start_burst_time + tau[proc_idx] - current_time
                    if (preempt_times[proc_idx] != -1):
                        time_left = start_burst_time + tau[proc_idx] - current_time - (preempt_times[proc_idx] - CPU_bursts[proc_idx][0])
                        
                    times_left[proc_idx] = time_left
        
                    if (tau[i] < time_left):
                        #? time 952ms: Process E (tau 40ms) completed I/O; preempting F [Q: E G A]
                        if current_time < 1000:
                            print("time ", current_time, "ms: Process ", chr(65 + i), " (tau ", tau[i], "ms)", " completed I/O; preempting ",runn_proc," [Q: ", sep='', end='')
                            print(*queue2, end='')
                            print("]")
                        num_preemps+=1
                        if (preempt_times[proc_idx] == -1):
                            preempt_times[proc_idx] = CPU_bursts[proc_idx][0]
                        CPU_bursts[proc_idx][0] = CPU_bursts[proc_idx][0] - (current_time - start_burst_time)
                        queue[0] = runn_proc
                        queue.insert(0, chr(65 + i))
                        queue_taus.insert(1, tau[proc_idx])
                        in_burst = False
                        wait_time_2 = cont_switch_time
                        skip_new = True
                        prev_proc = runn_proc
                        
                    elif (in_burst == False and len(queue) > 1 and (wait_time_2 == 1 or (wait_time_3 < (cont_switch_time - 2) and wait_time_3 > 0))):
                        temp = queue[0]
                        queue.pop(0)
                        if current_time < 1000:
                            print("time ", current_time, "ms: Process ", chr(65 + i), " (tau ", tau[i], "ms)", " completed I/O; added to ready queue [Q: ", sep='', end='')
                            print(*queue, end='')
                            print("]")
                        skip_new = True
                        skip_wait = True
                        queue.insert(0, temp)

                    else:
                        if (len(queue) > 1 and prev_proc in queue):
                            if (times_left[ord(prev_proc) - 65] < tau[i] and queue.index(prev_proc) > queue.index(chr(65 + i))):
                                queue.pop(queue.index(prev_proc))
                                queue.insert(0, prev_proc)
                        if current_time < 1000:
                            print("time ", current_time, "ms: Process ", chr(65 + i), " (tau ", tau[i], "ms)", " completed I/O; added to ready queue [Q: ", sep='', end='')
                            print(*queue, end='')
                            print("]")
                
                #if (tau[ord(runn_proc) - 65] > tau[ord(queue[0]) - 65])
                #========(1)=========

                    
                elif (in_burst == False and len(queue) > 1 and (wait_time_2 == 1 or (wait_time_3 < (cont_switch_time - 2) and wait_time_3 > 0))):
                    if (queue[0] != chr(65 + i)):
                        #print(queue)
                        temp = queue[0]
                        queue.pop(0)
                        if current_time < 1000:
                            print("time ", current_time, "ms: Process ", chr(65 + i), " (tau ", tau[i], "ms)", " completed I/O; added to ready queue [Q: ", sep='', end='')
                            print(*queue, end='')
                            print("]")
                        skip_new = True
                        skip_wait = True
                        queue.insert(0, temp)
                    else:
                        temp = queue[1]
                        queue.pop(1)
                        if current_time < 1000:
                            print("time ", current_time, "ms: Process ", chr(65 + i), " (tau ", tau[i], "ms)", " completed I/O; added to ready queue [Q: ", sep='', end='')
                            print(*queue, end='')
                            print("]")
                        skip_new = True
                        skip_wait = True
                        queue.insert(0, temp)
                    
                
                else:
                    if current_time < 1000:
                        print("time ", current_time, "ms: Process ", chr(65 + i), " (tau ", tau[i], "ms)", " completed I/O; added to ready queue [Q: ", sep='', end='')
                        print(*queue2, end='')
                        print("]")

                
                #if the queue has one value and the processor is empty, make runn_proc that new value (in queue2 not queue since queue "could")
                #have the prev runn_proc at index 0, which would cause redundant reassignment
                if len(queue)== 1 and runn_proc == '' and in_processor == False:
                    runn_proc = queue2[0]
                    in_processor = True    
 #! *******************************************SPECIFIC TO SJF and SRT*****************************************END

                wait_times[i] = -1
                IO_bursts[i].pop(0)
                if wait_time_3 == 0 and skip_wait == False:
                    wait_time_3 = int(cont_switch_time / 2)
               
        # Checking if every proccess is completed, then exits the loop
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

        #Increment wait_times corresponding to what's in queue
        for i in range (len(queue)):
            SRT_wait_times[ord(queue[i])-65]+=1
        
    # Final print statement
    #!enable printing for Simulator ending clause
    print("time ", current_time, "ms: Simulator ended for SRT [Q: empty]", sep='')

    avg = (sum(SRT_wait_times) - (cont_switch_time//2)*(SRT_cont_switches+num_preemps))/(sum([len(CPU_bursts_p[i]) for i in range(num_procs)]))
    SRT_CPU_util = math.ceil(sum([sum(x) for x in CPU_bursts_p])*100000/current_time)/1000
    avg = math.ceil(avg*1000)/1000
    """"""
    avg_turnaround =  (sum(SRT_wait_times) + (cont_switch_time/2)*SRT_cont_switches-2*num_preemps)/(sum([len(CPU_bursts_p[i]) for i in range(num_procs)])) + sum([sum(x) for x in CPU_bursts_p])/(sum([len(CPU_bursts_p[i]) for i in range(num_procs)]))
    avg_turnaround = math.ceil(avg_turnaround*1000)/1000
        #Turnaround time for a single process = total context switch time + (number of bursts) * cpu burst time + wait time 

    return SRT_cont_switches, avg , SRT_CPU_util, num_preemps, avg_turnaround

def main():
    #? Testing code
        num_procs, seed_no, lambda_, upp_bound, cont_switch, alpha, t_slice = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
        processes = ProcessSet(num_procs,lambda_,seed_no, upp_bound)
        processes.generate()
        arr_time, CPU_bursts, IO_bursts, no_bursts = processes.print_()
        tau_inits = [processes.get_tau() for i in range(num_procs)]
        SRT(num_procs, arr_time, CPU_bursts, IO_bursts, cont_switch, alpha, tau_inits)

#if __name__ == "__main__":
    