#####################################--80 CHARACTERS--##########################
'''This python code was completed in accordance with my CS 3360 course at Texas 
    State University taught by Professor Dr. Kechang Yang. Please see my report 
    on this coding assignment to learn more about my approach and steps I took 
    to implement the approach.'''

import random
import math
from collections import deque

# Exponential random number generator. 
# Copied from my Programming Assignment 1.
def exponential_random(lmbda):
    U = random.random() # Generates uniform random number
    return -math.log(1-U) / lmbda

# Event class to represent arrival and departure events
class Event:
    def __init__(self, event_time, event_type, process_id):
        self.event_time = event_time
        self.event_type = event_type # Arrival or Departure
        self.process_id = process_id

# Event Queue: sorted linked list
class EventQueue:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        # Insert event into the list sorted by event_time
        self.events.append(event)
        self.events.sort(key=lambda x: x.event_time)

    def pop_event(self):
        # pop the next event
        return self.events.pop(0)
    
    def is_empty(self):
        return len(self.events) == 0

# First-Come First-Serve function
def simulate_fcfs(arrival_rate, avg_service_time, num_processes=10000):
    event_queue = EventQueue()
    clock = 0.0  # Simulation clock
    processes_completed = 0
    ready_queue = deque()
    cpu_busy = False

    # Performance metrics
    total_turnaround_time = 0.0
    total_waiting_time = 0.0
    total_processes_in_queue = 0.0
    total_service_time = 0.0
    cpu_utilization_time = 0.0

    # Schedule the first arrival
    first_arrival_time = exponential_random(arrival_rate)
    event_queue.add_event(Event(first_arrival_time, 'arrival', 1))

    while processes_completed < num_processes:
        if event_queue.is_empty():
            break

        # Get the next event
        current_event = event_queue.pop_event()
        clock = current_event.event_time

        if current_event.event_type == 'arrival':
            # Handle process arrival
            if not cpu_busy:
                # CPU is idle, start service immediately
                service_time = exponential_random(1 / avg_service_time)
                departure_time = clock + service_time
                event_queue.add_event(Event(departure_time, 'departure', current_event.process_id))
                cpu_busy = True
                cpu_utilization_time += service_time
                total_service_time += service_time
            else:
                # Add process to the Ready Queue
                ready_queue.append(current_event.process_id)
                total_processes_in_queue += len(ready_queue)

            # Schedule the next arrival
            next_arrival_time = clock + exponential_random(arrival_rate)
            event_queue.add_event(Event(next_arrival_time, 'arrival', current_event.process_id + 1))

        elif current_event.event_type == 'departure':
            # Handle process departure
            processes_completed += 1
            turnaround_time = clock - first_arrival_time  # Time from arrival to departure
            total_turnaround_time += turnaround_time

            if ready_queue:
                # Start servicing the next process in the queue
                next_process_id = ready_queue.popleft()
                service_time = exponential_random(1 / avg_service_time)
                departure_time = clock + service_time
                event_queue.add_event(Event(departure_time, 'departure', next_process_id))
                cpu_utilization_time += service_time
                total_service_time += service_time
            else:
                # CPU becomes idle
                cpu_busy = False

    # Calculate performance metrics
    avg_turnaround_time = total_turnaround_time / num_processes if num_processes > 0 else 0
    avg_cpu_utilization = cpu_utilization_time / clock if clock > 0 else 0
    avg_processes_in_queue = total_processes_in_queue / processes_completed if processes_completed > 0 else 0
    throughput = processes_completed / clock if clock > 0 else 0

    return {
        'avg_turnaround_time': avg_turnaround_time,
        'throughput': throughput,
        'cpu_utilization': avg_cpu_utilization,
        'avg_processes_in_queue': avg_processes_in_queue
    }


# Main simulation run
def run_simulations():
    avg_service_time = 0.04  # Fixed avg service time
    results = []

    # Print table header for readability
    print(f"{'λ':<5} {'Avg Turnaround Time (s)':<25} {'Throughput (processes/s)':<30} {'CPU Utilization (%)':<25} {'Avg Ready Queue Size':<20}")
    print("-" * 110)

    for arrival_rate in range(10, 31):  # Simulate for λ = 10 -> 30
        metrics = simulate_fcfs(arrival_rate, avg_service_time)
        results.append((arrival_rate, metrics))

        # Print formatted results
        print(f"{arrival_rate:<5} "
              f"{metrics.get('avg_turnaround_time', 0):<25.4f} "
              f"{metrics.get('throughput', 0):<30.4f} "
              f"{metrics.get('cpu_utilization', 0) * 100:<25.2f} "
              f"{metrics.get('avg_processes_in_queue', 0):<20.4f}")

    return results

# Run the simulations
run_simulations()
