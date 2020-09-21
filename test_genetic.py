# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 15:01:05 2020

@author: Gabriel
"""


import genetic_algorithm as ga
import schedule as sc
import encoding
import copy
import numpy as np
import database_access as dba



#sample test 1
t3 = sc.Task(5,0,1,[1,3])
t2 = sc.Task(15,0,1,[1,3])
t1 = sc.Task(5,0,1,[1,3])
job0 = sc.Job([copy.deepcopy(t1),copy.deepcopy(t2),copy.deepcopy(t3)],80,0,0)

#sample test 2
s3 = sc.Task(5,1,2,[2,3,7])
s2 = sc.Task(15,1,2,[2,3,7,5])
s1 = sc.Task(5,1,2,[2,3,7])
job1 = sc.Job([copy.deepcopy(s1),copy.deepcopy(s2),copy.deepcopy(s3)],120,15,1)

#sample test 3
u3 = sc.Task(5,2,3,[2,3,7])
u2 = sc.Task(30,2,3,[2,3,7,5])
u1 = sc.Task(10,2,3,[2,3,7]) 
job2 = sc.Job([copy.deepcopy(u1),copy.deepcopy(u2),copy.deepcopy(u3)],160,50,2)

"""
job_list = [copy.deepcopy(job0),copy.deepcopy(job1),copy.deepcopy(job2)]
schedules_simple = encoding.generate_random_schedules(10, job_list)
sch0 = schedules_simple[0]
sch1 = schedules_simple[1]
sch2 = schedules_simple[2]
"""

#off = ga.uniform_crossover(sch0,sch1)
#mutant = ga.mutation(sch0,0.8,1)

p_sel = 0.25
n_tournament = 10


###############################################################################
week_n = 25

"""
list_jobs,machines,analysts_obj  = encoding.create_empty_schedule(week_n)
schedules = encoding.random_schedules(100, 25)
sc0 = schedules[0]
sc1 = schedules[1]
"""


pop_size = 100
offsprings = ga.genetic_algorithm(pop_size, week_n,100)










