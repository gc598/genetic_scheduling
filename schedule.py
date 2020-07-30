# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:07:51 2020

@author: esteb
"""

import numpy as np

#the value v at index i indicates that there are v machines of type i
number_machines = [2,3,1,5]
#each analyst is represented by an index for now
analysts = range(15)


class Machine:
    def __init__(self,timetable=None,mac_id=0):
        # list of tuples indicating activity starting and end times. any time not within the bounds of a tuple is idle
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
    
    def __init__(self,earliest_start_time=0,due_date=160,duration=160,machine=None,analysts=None,nextTask=None):
        #time will be counted by units of 6 min starting at 8 pm and finishing at 12pm so 160=12pm
        self.earliest_start_time=earliest_start_time
        self.due_date=due_date
        self.duration=duration
        self.machine = machine
        self.analysts = analysts
        #next task is used in case the next task need to be performed within a certain time after completion this task 
        self.nextTask = nextTask
        



class Schedule:
    
    def __init__(self,timetable=None):
        #the schedule's timetable will contain a list of Tasks, ordered by starting date
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
        
        
                            
        
        