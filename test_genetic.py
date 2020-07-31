# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 15:01:05 2020

@author: Gabriel
"""


import genetic_algorithm as ga
import schedule as sc
import encoding


#sample test 1
t3 = sc.Task(5,5,0,1,[1,3])
t2 = sc.Task(5,15,0,1,[1,3])
t1 = sc.Task(5,5,0,1,[1,3])
job0 = sc.Job([t1,t2,t3],80)

#sample test 2
s3 = sc.Task(30,5,1,2,[2,3,7])
s2 = sc.Task(30,15,1,2,[2,3,7,5])
s1 = sc.Task(30,5,1,2,[2,3,7])
job1 = sc.Job([s1,s2,s3],120)

#sample test 3
u3 = sc.Task(15,5,2,3,[2,3,7])
u2 = sc.Task(30,30,2,3,[2,3,7,5])
u1 = sc.Task(30,10,2,3,[2,3,7])
job2 = sc.Job([u1,u2,u3],160)

job_list = [job0,job1,job2]
schedules = encoding.generate_random_schedules(5, job_list)





