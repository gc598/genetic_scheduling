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
        for(start_active,end_active) in self.timetable:
            if (start>=start_active and start <= end_active) or (end >= start_active and end <= end_active):
                return False
        return True   
        

class Task:
    
    def __init__(self,earliest_start_time=0,duration=160,job_id=0,machine=None,analysts=None):
        """
        earliest_start_date: eartliest time this task can start to be completed
        machine: integer indicating the machine that can run this task
        analysts: list of indices of analysts who have the required competences to run this task
        job_id: job to which the task belongs
        """
        self.earliest_start_time=earliest_start_time
        self.start_time = self.earliest_start_time
        self.duration=duration
        self.end_time = self.start_time + self.duration
        self.mac_id = machine
        self.analysts = analysts
        self.job_id = job_id
        
    def print_task(self):
        tup = (self.start_time,self.end_time)
        print("task: ",str(self),str(tup),"on machine: ",str(self.mac_id),"in job: ",str(self.job_id))
 
    
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
        



class Schedule:
    
    def __init__(self,timetable,job_list):
        """
        the schedule's timetable will contain a list of Tasks, ordered by starting date
        machines is 2D array containing the machine objects for each type of machine
        min_time is where the schedule starts i.e. it's the beginning of the work week
        max_time is the end of the work week (end of the schedule)
        job_list contains the list of jobs to schedule
        """
        self.timetable = timetable
        self.job_list = job_list
        self.min_time = 0
        self.max_time = 1000
        self.machines = [[] for k in range(len(number_machines))]   
        for i in range(len(number_machines)):
            for j in range(number_machines[i]):
                self.machines[i].append(Machine([],i))    
        
    
    # returns the index of a machine of type i idle at time defined by the given interval if there is one
    def machine_i_idle_interval(self,i,start,end):
        if end<=start:
            return False
        for j in range(len(self.machines[i])):
            if self.machines[i][j].is_idle_at_interval(start,end):
                return j
        return -1
        
    def find_index_task(self,task):
        for i in range(len(self.timetable)):
            if self.timetable[i] == task:
                return i
        return -1
    
    def print_schedule(self):
        for task in self.timetable:
            task.print_task()
            
            
        
        
                            
        
        