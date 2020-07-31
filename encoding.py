# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:53:00 2020

@author: Gabriel
"""
import schedule as sc
import copy
import random


def place_task_timetable(sch,task):
    """
    returns (True,None) if there is an available machine to execute the task
    returns (False,task) if there is no available machine, in which case task will be evicted from the machine
        and will have to be replaced on the schedule later
    """
    sch.append(task)
    machine = task.mac_id
    index = sch.machine_i_idle_interval(task.start_time,task.end_time)
    if index==-1:
        return -1
    
    


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
    sch.timetable.append(current_task)
    tasks_added_so_far.append(current_task)
    
    for i in range(1,len(job.list_tasks)):
        current_task = job.list_tasks[i]
        prev_task = job.list_tasks[i-1]
        start_time = random.randint(prev_task.end_time,prev_task.end_time+random.randint(0,10))
        current_task.start_time = start_time
        current_task.end_time = current_task.start_time + current_task.duration
        sch.timetable.append(current_task)
        tasks_added_so_far.append(current_task)
        #if it's not possible to fit this job in the schedule, we restart the function
        if(current_task.end_time > max_time):
            for task in tasks_added_so_far:
                sch.timetable.remove(task)
            print("impossible: restart")    
            randomly_place_job_timetable(job,sch)
                  
            
        

def generate_random_schedules(pop_size,job_list):
    sch = None
    schedules = []
    for i in range(pop_size):
        sch = sc.Schedule([])
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

