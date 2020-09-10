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
import database_access as dba
import pandas as pd
import math

"""
removes the given task from the given schedule.updates machines consequently
"""
def remove_task_from_timetable(sch,task):
    #job = sch.job_list[sch.job_dict_id[task.job_id]]
    #print("removing job ",str(job))
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
        #print(current_task,current_task.job_id,current_task.analysts_indices)
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
    #print(len(sch.timetable))
    max_time = sch.max_time
    tasks_added_so_far = []
    
    """
    first, place the first job in the schedule, as it has no previous task, therefore does not have
    specific constraint regarding how long it must be executed after the previous task
    """
    
    current_task = job.list_tasks[0]
    start_time = random.randint(job.earliest_start_time,max_time-current_task.duration)
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
        sch = sc.Schedule([],copy.deepcopy(job_list))
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

##################################################################################################
##################################################################################################
"""
This will be a set a functions to get jobs and tasks from actual data from the database.
We will use queries from data_process_layer .
"""
##################################################################################################
##################################################################################################

def from_pandas_timestamp(tstamp,day_beginning_week):
    """
    

    Parameters
    ----------
    tstamp : pandas Timestamp
        timestamp to translate into a number in the time unit considered by this program
    return a number corresponding to the time unit given in Schedule.py (units of 6 minutes starting 
    at the beginning of the week).
    Therefore in this unit 1H = 10
    We consider that the weel 
    """
    
    time = 24*10*(tstamp.day-day_beginning_week)
    time += 10 * tstamp.hour
    time += int(tstamp.minute/6)
    return time

def from_delta_time(delta):
    days = delta.components.days
    hours = delta.components.hours
    minutes = delta.components.minutes
    return 24*10*days + 10*hours + math.ceil(minutes/6)


def get_zero_time(first_allowed_start_date_tstamp):
    """
    returns a timestamp corresponding to 0 in the programs unit
    first_allowed_start_date_tstamp is a pandas timestamp representing the first
    allowed start date

    """
    ts_min = first_allowed_start_date_tstamp
    ts = pd.Timestamp(year=ts_min.year,month=ts_min.month,day=ts_min.day,
                      hour=0,tz=ts_min.tz)
    return ts
    
def get_max_time(data):
    """
    data is a dataframe containing rows of the same week from tTest in the database
    returns the max time as defined in the object Schedule, ie time after which 
    the schedule stops counting.
    It is defined as 24:00 of the last dueDate's day
    """
    
    min_timeStamp = data["AllowedStartDate"].min()
    max_timeStamp = data["DueDate"].max()
    
    delta = max_timeStamp-min_timeStamp
    
    max_time = from_delta_time(delta)
    return max_time

def create_empty_schedule(week_n):
    
    
    
    """
    TODO:
    
    add reviewers to jobs, after integrating it to the main genetic algorithm

    
    NOTE:
    some NaN values in times for tasks may alter the number of tasks in the jobs
    
    """
    
    connection = dba.sqlalchemy_connection()
    
    """
    We first create the array of jobs that will be returned. Only tests(jobs)
    whose allowedStartDates belong to a certain week (week_n) will be added
    """
    data_tests = dba.get_tests_week(week_n)
    first_allowed_start_date_tstamp = data_tests["AllowedStartDate"].min()

    
    job_dict_id = {}
    # jobs completely processedallows to keep track of which jobs are processed, 
    # meaning all machines and analysts etc. a=have been added to them
    jobs_completely_processed = {}
    for i in data_tests.index:
        dueDate_tstamp = data_tests.loc[i]["DueDate"]
        allowed_start_date = data_tests.loc[i]["AllowedStartDate"]
        zero_time = get_zero_time(first_allowed_start_date_tstamp)
        dueDate = from_delta_time(dueDate_tstamp-zero_time)
        earliest_start_date = from_delta_time(allowed_start_date-zero_time)
        job = sc.Job(list_tasks = [],earliest_start_date=earliest_start_date,
                     due_date = dueDate,job_id=data_tests.loc[i]["ID"])
        job_dict_id.update({job.job_id:job})
        jobs_completely_processed.update({job.job_id:False})
        #print(job.earliest_start_time,job.due_date)
    
    """
    We now get the usable machines for each job. In the database, each machine belongs
    to a certain group.
    We will construct a dictionary of equipments (machines) indexed by their group ids,
    containing arrays of equipment ids (an array contains the equipment ids of all the 
    machine of a given group)?
    This dictionary will be used to construct machine objects corresponding to the usable
    machines for the set of jobs that we are given.
    """

    # for each group id, machines_to_create contains a list of equipment_id
    # corresponding to the machines we'll have to create
    machines_to_create = {}
    # equipments contains all tests of the corresponding week, with, for each test,
    # every group of equipments and every equipment that can run it
    equipments = dba.get_equipment(connection)        
    # data_eq is equipments restricted to the corresponding week (week_n)
    data_eq = equipments[equipments["TestID"].isin(data_tests["ID"])] 
    # test_machine_id contains the usable group id for each test, indexed by test id
    test_machine_id = {}
    for test_id in data_eq["TestID"].drop_duplicates():
        data_current_test = data_eq[data_eq["TestID"]==test_id]       
        gr_id = data_current_test["GroupID"].iloc[0]
        test_machine_id.update({test_id:gr_id})
        if gr_id not in machines_to_create.keys():
            machines_to_create.update({gr_id:[]})
            for j in data_current_test["EquipmentID"].index:
                eq_id = data_current_test["EquipmentID"].loc[j]         
                machines_to_create[gr_id].append(eq_id)
                
    """
    We now build the machines from the dictionary obtained at the last step.
    machines is an array of array as described in schedule.Schedule.
    """
    
    # dict_gr_id matches the group gr_id from the database to the id that will be used
    # by the program (mac_id in schedule.Machine)
    dict_gr_id = {}
    machines = []
    i = 0
    for gr_id in machines_to_create.keys():
        machines.append([])
        dict_gr_id.update({gr_id:i})
        for e_id in machines_to_create[gr_id]:
            new_machine = sc.Machine(timetable=[],mac_id=i,group_id=gr_id,eq_id=e_id)
            machines[i].append(new_machine)
        i += 1
    
    """
    We now build the tasks of each test. To do it we make a dictionary of lists of 
    tasks indexed by the corresponding job ids
    """
    dict_tasks = {}
    tasks = dba.get_tasks(connection)
    data_tasks = tasks[tasks["ID"].isin(data_tests["ID"])]
    for test_id in data_tasks["ID"].drop_duplicates():
        data_current_test = data_tasks[data_tasks["ID"]==test_id]
        # duration is expressed in hours in the database so need to multiply ot by 10
        durations = data_current_test["Time"]
        names = data_current_test["PhaseName"]
        if len(names)==len(durations) and test_id not in dict_tasks.keys():
            list_tasks = []
            for i in range(len(durations)):
                try:
                    dur = math.ceil(durations.iloc[i]*10)
                except ValueError as err:
                    continue
                name = names.iloc[i]
                task = sc.Task(duration=dur,job_id=test_id,task_name=name)
                list_tasks.append(task)
            dict_tasks.update({test_id:list_tasks})
            
    """
    We now build a dictionary of analysts indexed by their test (job). These are the 
    analysts that will potentially carry out the first 6 steps of the test.
    The last step needs to be done by a reviewer.
    """
    dict_analysts = {}
    # lists_analysts is the list of all analysts (userID) that are able to perform
    # a phase (task) of the test
    list_analysts_id= []
    analysts = dba.get_analysts_tests(connection)
    data_an = analysts[analysts["ID"].isin(data_tests["ID"])]
    for test_id in data_an["ID"].drop_duplicates():
        data_current_test = data_an[data_an["ID"]==test_id]
        array_analysts_ids = data_current_test["UserID"].iloc[:].to_numpy().tolist()
        dict_analysts.update({test_id:array_analysts_ids})
        list_analysts_id += array_analysts_ids
    #removes the duplicates of list_analysts_id
    list_analysts_id = list(dict.fromkeys(list_analysts_id))
    
    """
    Build the actual analysts objects
    """
    # dict_user_id matches the indeices used by the database (user_id) to the indices
    # used by the program, as in schedule.Task (analysts_indices)
    dict_user_id = {}
    analysts_obj = []
    i = 0
    for u_id in list_analysts_id:
        dict_user_id.update({u_id:i})
        new_analyst = sc.Analyst(name="Joe",timetable=[],an_id = i,user_id=u_id)
        analysts_obj.append(new_analyst)
        i += 1
        
    
    
    """
    We now build a dictionary of reviewers indexed by their test (job). These are the 
    reviewers that will potentially carry out the last step of the test.
    """       
    dict_reviewers = {}
    # lists_reviewers is the list of all reviewers (userID) that are able to perform
    # a phase (task) of the test
    list_reviewers= []
    reviewers = dba.get_reviewers(connection)
    data_rev = reviewers[reviewers["ID"].isin(data_tests["ID"])]
    for test_id in data_an["ID"].drop_duplicates():
        data_current_test = data_rev[data_rev["ID"]==test_id]
        array_reviewers_ids = data_current_test["UserID"].iloc[:].to_numpy().tolist()
        dict_reviewers.update({test_id:array_reviewers_ids})
        list_reviewers += array_reviewers_ids
    #removes the duplicates of list_reviewers
    list_reviewers = list(dict.fromkeys(list_reviewers))

    """
    We now add the machine group ids to the tasks of the different jobs,
    """
    
    for test_id in dict_tasks.keys():
        for task in dict_tasks[test_id]:
            task.mac_id = dict_gr_id[test_machine_id[test_id]]
            
    """
    We add the analysts to the tasks of the different jobs
    """
    
    for test_id in dict_tasks.keys():
        for task in dict_tasks[test_id]:
            task.analysts_indices = []
            for u_id in dict_analysts[test_id]:
                task.analysts_indices.append(dict_user_id[u_id])
                
    """
    Now add the tasks to the jobs
    """
    list_jobs = []
    
    for job_id in job_dict_id.keys():
        if job_id in test_machine_id.keys() and job_id in dict_tasks.keys() and job_id in dict_analysts.keys() and job_id in dict_reviewers.keys():
            job = job_dict_id[job_id]
            job.list_tasks = dict_tasks[job_id]
            job.update_max_sep_durations()
            list_jobs.append(job)
            job_dict_id.update({job_id:i})
            jobs_completely_processed[job_id] = True
            
    #print([(job.earliest_start_time,job.due_date) for job in list_jobs])
    
    return list_jobs,machines,analysts_obj       
    #return (list_jobs,job_dict_id,machines,dict_analysts,analysts_obj,dict_tasks,schedule)
    
    


#jobs,d_jobs,machines,analysts,analysts_obj,tasks,sch= create_empty_schedule(25)
    
def random_schedules(pop_size,week_n):
    list_jobs,machines,analysts = create_empty_schedule(week_n)
    sch = None
    schedules = []
    for i in range(pop_size):
        print("generating schedule: ",i)
        sch = sc.Schedule(timetable=[],job_list=copy.deepcopy(list_jobs),
                          analysts=copy.deepcopy(analysts),
                          machines=copy.deepcopy(machines))
        list_start_dates = [(job.earliest_start_time,job.due_date) for job in sch.job_list]
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

        
        
    
    
    
    

    
        
        
    
    
    
    

