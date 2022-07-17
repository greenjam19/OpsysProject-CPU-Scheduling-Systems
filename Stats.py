def Stats(sys_cont_switches, sys_avg_CPU_burst_time, sys_avg_wait_times, sys_CPU_util,sys_num_preemps,sys_avg_turnaround_times):
    #! statistics related to the 4 scheduling systems
    #sched system names
    sys_names = ["FCFS","SJF","SRT","RR"]
    #sched system CPU util
    #sched system preemption amounts
    sys_preempts = [0,0] + sys_num_preemps
    with open('simout.txt', 'w') as f:
        for i in range(4):
            f.writelines(["Algorithm ",sys_names[i],"\n"])
            f.writelines(["-- average CPU burst time: ",str(sys_avg_CPU_burst_time)," ms\n"])
            f.writelines(["-- average wait time: ",str(format(sys_avg_wait_times[i], ".3f"))," ms\n"])
            f.writelines(["-- average turnaround time: ",str(sys_avg_turnaround_times[i])," ms\n"])
            f.writelines(["-- total number of context switches: ",str(sys_cont_switches[i]),"\n"])
            f.writelines(["-- total number of preemptions: ",str(sys_preempts[i]),"\n"])
            f.writelines(["-- CPU utilization: ",str(sys_CPU_util[i]),"%\n"])
