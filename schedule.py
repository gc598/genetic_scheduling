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
        timetable: list of tuples indicating activity starting and end times. 
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
    
    def __init__(self,earliest_start_time=0,duration=160,machine=None,analysts=None):
        """
        earliest_start_date: eartliest time this task can start to be completed
        machine: integer indicating the machine that can run this task
        analysts: list of indices of analysts who have the required competences to run this task
        nextTask: tuple indicating whether this task precedes an other one, and if so indicates the max
                duration between the end of this task and the beginning of the next one
        """
        self.earliest_start_time=earliest_start_time
        self.duration=duration
        self.machine = machine
        self.analysts = analysts
 
    
class Job:
    
    def __init__(self,list_tasks = [],due_date = 160):
        """

        Parameters
        ----------
        list_tasks : TYPE, optional
            DESCRIPTION. The default is []. 2D array contains tasks ordered by precedence (first dimension)
            contains also max duration between task i and task i+1 (np.inf if no such duration) 
            in second dimension
        Returns
        -------
        None.

        """
        self.due_date = due_date
        self.list_tasks = list_tasks
        



class Schedule:
    
    def __init__(self,timetable=None):
        """
        the schedule's timetable will contain a list of Tasks, ordered by starting date
        machines is 2D array containing the machine objects for each type of machine
        """
        self.timetable = timetable
        self.machines = [[] for k in range(len(number_machines))]   
        for i in range(len(number_machines)):
            for j in range(number_machines[i]):
                self.machines[i].append (Machine([],i))    
        
    def fitness(self):
        fit = 0
        for (index,start_time,task) in self.timetable:
            if task.due_date >= start_time:
                fit+=1
        return fit
    
    # returns true if there is a machine of type i idle at time defined by the givent interval
    def machine_i_idle_interval(self,i,start,end):
        if end<=start:
            return False
        
        
                            
        
        