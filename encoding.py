# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:53:00 2020

@author: Gabriel
"""

"""
File mostly dedicated to functions 'encoding' schedules into genomes. This means that we will make them
usable by a genetic algorithm, whil repecting the constraints, and the dual resource nature of this 
scheduling problem.
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
    
    #removes task from machine's timetable
    machines = sch.machines[task.mac_id]
    for machine in machines:
        if task in machine.timetable:
            machine.timetable.remove(task)
            
        
    #removes task from analyst's timetable
    for index in range(len(task.analysts_indices)):
        analyst = sch.analysts[index]
        if task in analyst.timetable:
            analyst.timetable.remove(task)
        

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
    
    #add the task to the machine's timetable
    index = sch.machine_i_idle_interval(task.mac_id,task.start_time,task.end_time)
    if index==-1:
        print("not available mac",task.start_time,task.end_time,"task",str(task),"from job",str(task.job_id))
        return False
    machine_to_operate = sch.machines[task.mac_id][index]
    machine_to_operate.timetable.append(task)
    
    #add the task to the analyst's timetable
    index = sch.analyst_idle_task(task)
    if index==-1:
        print("not available an",task.start_time,task.end_time,"task",str(task),"from job",str(task.job_id))
        return False
    appointed_analyst = sch.analysts[index]
    appointed_analyst.timetable.append(task)
    return True
    
    
def place_job_timetable(sch,job):
    """
    place jobs on the timetable, whse tasks have already known starting times and duration times.
    returns True if successfully added, False if it couild not be added.
    """      
    if not job:
        return
    
    max_time = sch.max_time
    
    for i in range(0,len(job.list_tasks)):
        current_task = job.list_tasks[i]
        start_time = current_task.start_time    
        if current_task not in sch.timetable:
            flag=place_task_timetable(sch,current_task)
        #if it's not possible to fit this job in the schedule, return false
        if(current_task.end_time > max_time or not flag):
            remove_job_from_timetable(sch,job)
            print("impossible: abort")    
            return False
    sch.order_by_start_time()
    return True
    


def randomly_place_job_timetable(job,sch):
    """
    This function assigns random random working times to the tasks in the different jobs before placing 
    them on the timetable.
    """
    if not job:
        return
    print(len(sch.timetable))
    max_time = sch.max_time
    tasks_added_so_far = []
    
    """
    first, place the first job in the schedule, as it has no previous task, therefore does not have
    specific constraint regarding how long it must be executed after the previous task
    """
    
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
        #if it's not possible to fit this job in the schedule, we restart the function
        if(current_task.end_time > max_time or flag==-1):
            remove_job_from_timetable(sch,job)
            print("impossible: restart")    
            randomly_place_job_timetable(job,sch)
    sch.order_by_start_time()
                  
            
        


def generate_random_schedules(pop_size,job_list):
    sch = None
    schedules = []
    for i in range(pop_size):
        sch = sc.Schedule([],copy.deepcopy(job_list),[])
        print(sch)
        #we keep looping while all the jobs have not been scheduled
        for j in range(len(sch.job_list)):
            """
            given the fact that operations in a job must be carried out within 1H of one another, we'll
            process them jointly
            """
            job = sch.job_list[j]
            randomly_place_job_timetable(job,sch)
        schedules.append(sch)
            
    return schedules

        
        
    
    
    
    

