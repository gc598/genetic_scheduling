# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:53:00 2020

@author: Gabriel
"""
import schedule as sc
import copy
import random


"""
removes the given task from the given schedule.updates machines consequently
"""
def remove_task_from_timetable(sch,task):
    job = sch.job_list[task.job_id]
    print("removing job ",str(job))
    try:
        sch.timetable.remove(task)
    except ValueError as err:
        pass
    machines = sch.machines[task.mac_id]
    for machine in machines:
        if (task.start_time,task.end_time,task) in machine.timetable:
            machine.timetable.remove((task.start_time,task.end_time,task))
            return task
    return None

def remove_job_from_timetable(sch,job):
    for task in job.list_tasks:
        remove_task_from_timetable(sch,task)
    


def place_task_timetable(sch,task):
    """
    returns (True,None) if there is an available machine to execute the task
    returns (False,task) if there is no available machine, in which case task will be evicted from the machine
        and will have to be replaced on the schedule later
    """
    sch.timetable.append(task)
    index = sch.machine_i_idle_interval(task.mac_id,task.start_time,task.end_time)
    if index==-1:
        print("not available",task.start_time,task.end_time,"task",str(task),"from job",str(task.job_id))
        return
    machine_to_operate = sch.machines[task.mac_id][index]
    machine_to_operate.timetable.append(task)
    
    
    


def randomly_place_job_timetable(job,sch):
    if not job:
        return
    print(len(sch.timetable))
    max_time = sch.max_time
    tasks_added_so_far = []
    
    current_task = job.list_tasks[0]
    start_time = random.randint(current_task.earliest_start_time,max_time-current_task.duration)
    current_task.start_time = start_time
    current_task.end_time = current_task.start_time + current_task.duration
    if current_task not in sch.timetable:
        place_task_timetable(sch,current_task)
    tasks_added_so_far.append(current_task)
    
    for i in range(1,len(job.list_tasks)):
        current_task = job.list_tasks[i]
        prev_task = job.list_tasks[i-1]
        max_separation_duration = job.max_separation_durations[i] #max time between end of i-1 and start of i
        start_time = random.randint(prev_task.end_time,prev_task.end_time+random.randint(0,max_separation_duration))
        current_task.start_time = start_time
        current_task.end_time = current_task.start_time + current_task.duration
        flag = 0
        if current_task not in sch.timetable:
            flag=place_task_timetable(sch,current_task)
        tasks_added_so_far.append(current_task)
        #if it's not possible to fit this job in the schedule, we restart the function
        if(current_task.end_time > max_time or flag==-1):
            remove_job_from_timetable(sch,job)
            print("impossible: restart")    
            randomly_place_job_timetable(job,sch)
                  
            
        

def generate_random_schedules(pop_size,job_list):
    sch = None
    schedules = []
    for i in range(pop_size):
        sch = sc.Schedule([],job_list)
        print(sch)
        #we keep looping while all the jobs have not been scheduled
        for j in range(len(job_list)):
            """
            given the fact that operations in a job must be carried out within 1H of one another, we'll
            process them jointly
            """
            job = job_list[j]
            randomly_place_job_timetable(job,sch)
        schedules.append(sch)
            
    return schedules

