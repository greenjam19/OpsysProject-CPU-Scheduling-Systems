# CSCI 4210 - Simulation Project

This project is a simulation of an operating system. The focus is on processes that are assumed to be resident in memory, waiting to use the CPU.

## Conceptual Design

A **process** is defined as program in execution. Processes are in one of three states:

* **RUNNING**: actively using the CPU and executing instructions
* **READY**: ready to use CPU, meaning ready to execute a CPU burst
* **WAITING**: blocked on I/O or some other event

<p align="center">
    <img style="border-radius: 20px" src="./img/conceptual_design.svg" alt="Conceptual Design">
</p>

## First-come-first-served (FCFS)

The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready queue, waiting to use the CPU.

## Shorterst job first (SJF)

In SJF, processes are stored in the ready queue in order of priority based on their anticipated CPU burst times. More specifically, the process with the shortest CPU burst time will be selected as the next process executed by the CPU.

## Shortest remaining time (SRT)

The SRT algorithm is a preemptive version of the SJF algorithm. In SRT, when a process arrives, as it enters the ready queue, if it has a predicted CPU burst time that is less than the remaining predicted time of the currently running process, a preemption occurs. When such a preemption occurs, the currently running process is added back to the ready queue.

## Round robin (RR)

The RR algorithm is essentially the FCFS algorithm with time slice *t*<sub>*slice*</sub>. Each process is given a *t*<sub>*slice*</sub> amount of time to complete its CPU burst. If the time slice expires, the process is preempted and added to the end of the ready queue.

If a process completes its CPU burst before a time slice expiration, the next process on the ready queue is immediately context-switched in to use the CPU.

## Getting Started

### Dependencies

* Python 3.8

### Usage

Run the `project.py` with the following command line arguments after it:

1. (**int**) for the number of processes
2. (**int**) that represents the *seed* for the pseudo-RNG
3. (**float**) used for exponential distribution
4. (**int**) that represents upper bound for valid pseudo-random numbers
5. (**int**) for the time it takes to perform a context switch (in ms)
6. (**float**) a constant used for calculating *τ* for SJR and SRT
7. (**int**) for the time slice value (in ms) used in RR

Example usage:
```python3 project.py 2 19 0.01 4096 4 0.5 64```

After running, a file named `simout.txt` will be created that contains statistics for each simulated algorithm.
An example of this would be:
<p align="center">
    <img style="border-radius: 20px" src="./img/output.svg" alt="Conceptual Design">
</p>



## Authors

* Jamarri Green (greenj19)
* Shane Stoll (stolls)
* Noah Cussatti (cussan)
