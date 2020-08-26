# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 15:01:05 2020

@author: Gabriel
"""


import genetic_algorithm as ga
import schedule as sc
import encoding
import copy


#sample test 1
t3 = sc.Task(5,5,0,1,[1,3])
t2 = sc.Task(5,15,0,1,[1,3])
t1 = sc.Task(5,5,0,1,[1,3])
job0 = sc.Job([copy.deepcopy(t1),copy.deepcopy(t2),copy.deepcopy(t3)],80,0)

#sample test 2
s3 = sc.Task(30,5,1,2,[2,3,7])
s2 = sc.Task(30,15,1,2,[2,3,7,5])
s1 = sc.Task(30,5,1,2,[2,3,7])
job1 = sc.Job([copy.deepcopy(s1),copy.deepcopy(s2),copy.deepcopy(s3)],120,1)

#sample test 3
u3 = sc.Task(15,5,2,3,[2,3,7])
u2 = sc.Task(30,30,2,3,[2,3,7,5])
u1 = sc.Task(30,10,2,3,[2,3,7]) 
job2 = sc.Job([copy.deepcopy(u1),copy.deepcopy(u2),copy.deepcopy(u3)],160,2)

job_list = [copy.deepcopy(job0),copy.deepcopy(job1),copy.deepcopy(job2)]
schedules = encoding.generate_random_schedules(100, job_list)
sch0 = schedules[0]
sch1 = schedules[1]
sch2 = schedules[2]

#off = ga.uniform_crossover(sch0,sch1)
#mutant = ga.mutation(sch0,0.8,1)

p_sel = 0.25
n_tournament = 10
print("  ")
sched = ga.tournament_selection(p_sel, n_tournament, schedules)
sched
for s in sched:
    print(s.fitness_val())











