# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:07:51 2020

@author: Gabriel
"""

"""
This file contains all the necessary objects to deal with the genetic selection of schedules, with 
dual resource (machines and analysts) and constraints that will be coded in the creation of the schedules.
A schedule will contain jobs (sample test), themselves composed of different tasks (every action needed
to carry out a sample test).
Machines and analysts are also represented as objects.
Time will be represented discretely as units of 6 minutes, 0 being the start of the week 
(schedules will be computed every week)
"""

import numpy as np
import copy

#the value v at index i indicates that there are v machines of type i
number_machines = [2,3,1,5]
#each analyst is represented by an index for now
analysts = range(15)


class Machine:
    def __init__(self,timetable=None,mac_id=0,group_id=0,eq_id=0):
        """
        timetable: list of tuples indicating activity starting time, end time, and task being executed. 
                any time not within the bounds of a tuple indicates an idle period
        mac_id: id of the machine as defined by the indices of array number_machines
        """
        self.timetable = timetable #
        self.mac_id = mac_id #
        
        """
        The following attributes are from the database organisation.
        
        group_id: id of the group to which the machine belongs
        eq_id : (equipment id): id of this particular equipment
        """
        self.group_id = group_id #
        self.eq_id = eq_id #
        
    
    #returns true if the machine is idle during the given interval
    def is_idle_at_interval(self,start,end):
        if not self.timetable:
            return True
        for task in self.timetable:
            start_active = task.start_time
            end_active = task.end_time
            if (start>start_active and start < end_active) or (end > start_active and end < end_active):
                #print("in fct is_idle_mac",str(start),str(end),str(start_active),str(end_active))
                return False
        return True   
    
    def print_machine(self):
        for task in self.timetable:
            task.print_task()
            
    def copy_essential_machine(self):
        """
        returns a copy of the current analyst, without its timetable (only the 
        fundamental information)
        """
        new_machine = Machine(timetable=[],mac_id=self.mac_id,group_id=self.group_id,
                              eq_id=self.eq_id)
        return new_machine
            
    

class Analyst:
    
    def __init__(self,timetable=None,an_id=0,name = "G",user_id = 0):
        

        """
        

        Parameters
        ----------
        timetable : TYPE, optional
            DESCRIPTION. The default is None.

        timetable will include lunchbreaks and off work time. Those natural off times will be instanciated
        upon creation of an analyst. 
        an_id is the id of the analyst

        Returns
        -------
        None.

        """
        self.name = name #
        self.timetable = timetable #
        self.an_id= an_id #
        
        """
        The following aattributes are from the database, they are not used to perform
        the main genetic algorithm
        """
        
        self.user_id = user_id #
        
    #returns true if the analyst is idle during the given interval
    def is_idle_at_interval(self,start,end):
        if not self.timetable:
            return True
        for task in self.timetable:
            start_active = task.start_time
            end_active = task.end_time
            if (start>start_active and start < end_active) or (end > start_active and end < end_active):
                #print("in fct is_idle_an",str(start),str(end),str(start_active),str(end_active))
                return False
        return True  
 
    def print_analyst(self):
        for task in self.timetable:
            task.print_task()
            
            
    def copy_essential_analyst(self):
        """
        returns a copy of the current analyst, without its timetable (only the 
        fundamental information)

        """
        
        new_analyst = Analyst(timetable=[],an_id=self.an_id,name=self.name,
                              user_id=self.user_id)
        return new_analyst
    
    def add_shift_task(self,shift_start,shift_end,start_day):
        
        """
        shift_start: hour of the start of the shift (number from 0 to 24)
        shift_end: hour of the end of the shift (number from 0 to 24)
        strat_day: beginning of the current day, expressed in the program's time unit
        
        This function will add the tasks representing the fact that 
        the analyst is not
        available as the time span is not part of the shift hours for this day (the
        day starting at start_day).
        This function assumes that the analyst's timetable IS EMPTY
        """
        

        tasks_shift = []
        if shift_end < shift_start:
            
            """
            we start by the case where the shift start a day and end the day after.
            then every hour not in the shift will be represented as a task, which will be
            added to the analyst's timetable
            """
            
            duration = shift_start-shift_end
            task = Task(duration= duration,job_id=-1,machine=None,analysts_ind=None,
                        task_name = "not in shift")
            task.start_time = shift_end+start_day
            task.end_time = task.start_time + task.duration
            tasks_shift.append(task)
            
        else:
            
            """
            if the shift remains within the same day, we'll create 2 tasks
            """
            dur1 = shift_start
            dur2 = 240-shift_end
            task1 = Task(duration= dur1,job_id=-1,machine=None,analysts_ind=None,
                        task_name = "not in shift")                        
            task2 = Task(duration= dur2,job_id=-1,machine=None,analysts_ind=None,
                        task_name = "not in shift")
            task1.start_time = start_day
            task1.end_time = task1.start_time + task1.duration
            task2.start_time = start_day + shift_end
            task2.end_time = task2.start_time + task2.duration
            tasks_shift.append(task1)
            tasks_shift.append(task2)
            
        for task in tasks_shift:
            self.timetable.append(task)
            
    def fuse_shifts(self):
        
        """
        This function fuses the connex non shift times (ie fuses the non shift times
        who start at the time the previous one ends)
        
        THIS FUNCTION ASSUMES THAT ONLY SHIFT TASKS ARE PRESENT IN THE ANALYST'S 
        TIMETABLE
        """            
        
        if len(self.timetable) <=1:
            return
        for task in self.timetable:
            if task.task_name != "not in shift":
                print("not only shift tasks in the timetable")
                return
            
        task_shift_to_remove = []
        task_shift_to_add = []
        
        for i in range(len(self.timetable)-1):
            task0 = self.timetable[i]
            task1 = self.timetable[i+1]
            if task0.end_time == task1.start_time:
                new_task = Task(duration=task0.duration+task1.duration,job_id=-1,
                                machine = None,analysts_ind=None,
                                task_name="not in shift")
                new_task.start_time = task0.start_time
                new_task.end_time = new_task.start_time+new_task.duration
                task_shift_to_remove.append(task0)
                task_shift_to_remove.append(task1)
                task_shift_to_add.append(new_task)
        
        for task_shift in task_shift_to_remove:
            if task_shift in self.timetable:
                self.timetable.remove(task_shift)
                
        for task_shift in task_shift_to_add:
            self.timetable.append(task_shift)
                
        """
        now we sort the timetable by ascending order of shift task's start times
        """
        
        sorted_timetable = []
        start_times_list = [task.start_time for task in self.timetable]
        sorted_indices = np.argsort(start_times_list)
        for i in sorted_indices:
            sorted_timetable.append(self.timetable[i])
        self.timetable = sorted_timetable
        
        
        
        
        

class Task:
    
    def __init__(self,duration=160,job_id=0,machine=0,analysts_ind=None,task_name="name"):
        """
        earliest_start_date: eartliest time this task can start to be completed
        machine: integer indicating the machine that can run this task
        analysts: list of integer indices of analysts who have the required competences to run this task
        job_id: job to which the task belongs
        """
        self.start_time = 0 #
        self.duration=duration #
        self.end_time = self.start_time + self.duration #
        self.mac_id = machine #
        self.analysts_indices = analysts_ind
        self.job_id = job_id #
        self.task_name = task_name #
        
    def print_task(self):
        tup = (self.start_time,self.end_time)
        print("task: ",str(self)," , ",self.task_name, str(tup),
              "on machine: ",str(self.mac_id),"in job: ",str(self.job_id))
        
    def copy_task(self):
        copied_task = Task(self.duration,self.job_id,self.mac_id
                           ,self.analysts_indices)
        copied_task.start_time = self.start_time
        copied_task.end_time = self.end_time
        copied_task.job_id = self.job_id
        return copied_task
            
            
 
    
class Job:
    
    def __init__(self,list_tasks = [],earliest_start_date=0,due_date = 160,job_id=0):
        """

        Parameters
        ----------
        list_tasks : TYPE, optional
            DESCRIPTION. The default is []. 2D array contains tasks ordered by precedence (first dimension)
            contains also max duration between task i and task i+1 (np.inf if no such duration) 
            in second dimension
            
            max_separation_durations: lists the maximum durations between the end of task i-1 and 
                the start of task i. The first element will be -1, to keep the length of 
                max_separation_durations equal to that of list_tasks
        Returns
        -------
        None.

        """
        self.earliest_start_time = earliest_start_date
        self.due_date = due_date #
        self.list_tasks = list_tasks #
        self.max_separation_durations = []
        self.max_separation_durations.append(-1)
        for j in range(len(list_tasks)-1):
            self.max_separation_durations.append(10)
        self.job_id = job_id #
            
    def copy_job(self):
        copied_job = Job(list_tasks=[],earliest_start_date=self.earliest_start_time,
                         due_date=self.due_date)
        copied_job.max_separation_durations = self.max_separation_durations
        copied_job.list_tasks = []
        for task in self.list_tasks:
            copied_job.list_tasks.append(task.copy_task())
            copied_job.job_id = self.job_id
        return copied_job
    
    def print_job(self):
        for task in self.list_tasks:
            task.print_task()
            
    def update_max_sep_durations(self):
        self.max_separation_durations = []
        self.max_separation_durations.append(-1)
        for j in range(len(self.list_tasks)-1):
            self.max_separation_durations.append(10)        
        



class Schedule:
    
    def __init__(self,timetable,job_list,analysts = None,machines=None):
        """
        the schedule's timetable will contain a list of Tasks, ordered by starting date
        machines is 2D array containing the machine objects for each type of machine
        min_time is where the schedule starts i.e. it's the beginning of the work week
        max_time is the end of the work week (end of the schedule)
        job_list contains the list of jobs to schedule
        analysts: list of all the analysts index by their id
        """
        self.timetable = timetable
        self.job_list = []
        for job in job_list:
            self.job_list.append(job.copy_job())
        self.min_time = 0
        self.max_time = 240*31
        self.machines = [[] for k in range(len(number_machines))]   
        for i in range(len(number_machines)):
            for j in range(number_machines[i]):
                self.machines[i].append(Machine([],i))    
        self.analysts = []
        for i in range(8):
            self.analysts.append(Analyst([],i,"Joe"))
        
        if analysts != None:
            self.analysts = analysts
        if machines != None:
            self.machines= machines
            
        """
        The following attributes are not fundamentals of the genetic algorithm, rather 
        they are attributes from the database.
        job_dict_id: dictionnary that maches every testID of the database to the 
            corresponding job index in self.job_list
        """
        self.job_dict_id = {}
        i=0
        for job in self.job_list:
            self.job_dict_id.update({job.job_id:i})
            i+=1
        
    
    # returns the index of a machine of type i idle at time defined by the given interval if there is one
    def machine_i_idle_interval(self,i,start,end):
        if end<=start:
            return -1
        #for all machines of type i, check if one of them is idle
        #print(self.machines,len(self.machines),"test")
        for j in range(len(self.machines[i])):
            #print("machine: ",(i,j),len(self.machines))
            if self.machines[i][j].is_idle_at_interval(start,end):
                return j
        return -1
    
    # checks if there is an available analyst for the given task
    def analyst_idle_task(self,task):
        start = task.start_time
        end = task.end_time
        if end<=start:
            return -1
        for index in task.analysts_indices:
            #task.print_task()
            #print(index,len(self.analysts),task.job_id,self)
            #self.print_schedule()
            analyst = self.analysts[index]
            if analyst.is_idle_at_interval(start,end):
                return index
        return -1        
        
    def find_index_task(self,task):
        """
        returns the index of the given task in the schedule's timetable, or -1 if it's not there
        """
        for i in range(len(self.timetable)):
            if self.timetable[i] == task:
                return i
        return -1
    
    def print_schedule(self):
        for task in self.timetable:
            task.print_task()
      
        
    def search_job_by_id(self,job_id):
        """
        assumes that the jobs of job_list of ordered by job_id
        """
        return self.job_list[job_id]
    
    def fitness_val(self):
        """
        we will evaluate the fitness of a schedule (ie a chromosome) by considerring the number of
        not late jobs in it, which we want to maximise.
        Note that this means that having a few very late jobs is considered less harmful than having 
        many slightly overdue jobs, as most deadlines are hard.
        """
        
        fit = 0
        for job in self.job_list:
            # if the job's due date is lower than the end time of the mast task in the job, add 1 to fit
            if job.due_date > job.list_tasks[-1].end_time:
                fit += 1
        return fit
    
    def order_by_start_time(self):
        
        """
        orders tasks in the schedule's timetable by their starting times. This is the 
        default organisation of a schedule.
        """
        start_times = []
        for task in self.timetable:
            start_times.append(task.start_time)
            
        sort_indices = np.argsort(start_times)
        tmp = copy.copy(self.timetable)
        
        for i in range(len(self.timetable)):
            self.timetable[i] = tmp[sort_indices[i]]
            
    def sort_job_list(self):
        
        """
        orders the job_list variable by ascending order of job id. This is the default organisation
        of job lists in schedules
        """
        
        job_ids = []
        for job in self.job_list:
            job_ids.append(job.job_id)
            
        sort_indices = np.argsort(job_ids)
        tmp = copy.copy(self.job_id)
        
        for i in range(len(self.job_list)):
            self.job_list[i] = tmp[sort_indices[i]]
            
    def get_sorted_list_jobs(self):
        """
        returns the list of jobs sorted by their start dates (start dates of their
        first tasks)

        """
        start_times = []
        for job in self.job_list:
            start_times.append(job.list_tasks[0].start_time)
        sort_indices = np.argsort(start_times)
        sorted_list = []
        for i in sort_indices:
            sorted_list.append(self.job_list[i])
        return sorted_list
    
    def update_dictionary(self):
        self.job_dict_id = {}
        i=0
        for job in self.job_list:
            self.job_dict_id.update({job.job_id:i})
            i+=1   
            
    def total_fit_schedules(schedules):
        """
        computes the average fitness value of a list of schedules
        """
        fit_vals = np.array([sch.fitness_val() for sch in schedules])
        return np.average(fit_vals)
        
        
            
            
        
        
                            
        
        
        
        
        
        