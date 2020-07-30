# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 15:01:05 2020

@author: esteb
"""


import genetic_algorithm as ga
import schedule as sc


#sample test 1
t3 = sc.Task(5,120,5,1,[1,3],None)
t2 = sc.Task(5,120,15,1,[1,3],t3)
t1 = sc.Task(5,120,5,1,[1,3],t2)

#sample test 2
s3 = sc.Task(30,120,5,2,[2,3,7],None)
s2 = sc.Task(30,120,15,2,[2,3,7,5],s3)
s1 = sc.Task(30,120,5,2,[2,3,7],s2)

#sample test 3
u3 = sc.Task(15,120,5,3,[2,3,7],None)
u2 = sc.Task(30,120,30,3,[2,3,7,5],u3)
u1 = sc.Task(30,120,10,3,[2,3,7],u2)




