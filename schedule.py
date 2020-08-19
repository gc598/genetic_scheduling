# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:07:51 2020

@author: Gabriel
"""

import numpy as np

#the value v at index i indicates that there are v machines of type i
number_machines = [2,3,1,5]
#each analyst is represented by an index for now
analysts = range(15)


class Machine:
    def __init__(self,timetable=None,mac_id=0):
        """
        timetable: list of tuples indicating activity starting time, end time, and task being executed. 
                any time not within the bounds of a tuple indicates an idle period
        mac_id: id of the machine as defined by the indices of array number_machines
        """
        self.timetable = timetable
        self.mac_id = mac_id
    
    #returns true if the machine is idle during the given interval
    def is_idle_at_interval(self,start,end):
        if not self.timetable:
            return True
        for task in self.timetable:
            start_active = task.start_time
            end_active = task.end_time
            if (start>start_active and start < end_active) or (end > start_active and end < end_active):
                print("in fct is_idle_mac",str(start),str(end),str(start_active),str(end_active))
                return False
        return True   
    
    def print_machine(self):
        for task in self.timetable:
            task.print_task()
            
    

class Analyst:
    
    def __init__(self,timetable=None,an_id=0,name = "G"):
        

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
        self.name = name
        self.timetable = timetable
        self.an_id= an_id
        
    #returns true if the analyst is idle during the given interval
    def is_idle_at_interval(self,start,end):
        if not self.timetable:
            return True
        for task in self.timetable:
            start_active = task.start_time
            end_active = task.end_time
            if (start>start_active and start < end_active) or (end > start_active and end < end_active):
                print("in fct is_idle_an",str(start),str(end),str(start_active),str(end_active))
                return False
        return True  
 
    def print_analyst(self):
        for task in self.timetable:
            task.print_task()       
        

class Task:
    
    def __init__(self,earliest_start_time=0,duration=160,job_id=0,machine=None,analysts_ind=None):
        """
        earliest_start_date: eartliest time this task can start to be completed
        machine: integer indicating the machine that can run this task
        analysts: list of integer indices of analysts who have the required competences to run this task
        job_id: job to which the task belongs
        """
        self.earliest_start_time=earliest_start_time
        self.start_time = self.earliest_start_time
        self.duration=duration
        self.end_time = self.start_time + self.duration
        self.mac_id = machine
        self.analysts_indices = analysts_ind
        self.job_id = job_id
        
    def print_task(self):
        tup = (self.start_time,self.end_time)
        print("task: ",str(self),str(tup),"on machine: ",str(self.mac_id),"in job: ",str(self.job_id))
        
    def copy_task(self):
        copied_task = Task(self.earliest_start_time,self.duration,self.job_id,self.mac_id
                           ,self.analysts_indices)
        return copied_task
            
            
 
    
class Job:
    
    def __init__(self,list_tasks = [],due_date = 160):
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
        self.due_date = due_date
        self.list_tasks = list_tasks
        self.max_separation_durations = []
        self.max_separation_durations.append(-1)
        for j in range(len(self.list_tasks)-1):
            self.max_separation_durations.append(10)
            
    def copy_job(self):
        copied_job = Job([],self.due_date)
        copied_job.max_separation_durations = self.max_separation_durations
        copied_job.list_tasks = []
        for task in self.list_tasks:
            copied_job.list_tasks.append(task.copy_task())
        return copied_job
        



class Schedule:
    
    def __init__(self,timetable,job_list,analysts = None):
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
        self.max_time = 1000
        self.machines = [[] for k in range(len(number_machines))]   
        for i in range(len(number_machines)):
            for j in range(number_machines[i]):
                self.machines[i].append(Machine([],i))    
        self.analysts = analysts
        for i in range(8):
            self.analysts.append(Analyst([],i,"Joe"))
            
        
    
    # returns the index of a machine of type i idle at time defined by the given interval if there is one
    def machine_i_idle_interval(self,i,start,end):
        if end<=start:
            return -1
        #for all machines of type i, check if one of them is idle
        for j in range(len(self.machines[i])):
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
            
            
        
        
                            
        
        
        
        
        
        