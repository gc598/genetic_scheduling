# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 12:00:03 2020

@author: Gabriel
"""

import schedule as sc
import encoding as en
import random

def uniform_crossover(sch1,sch2):
    """
        Parameters
        ----------
        sch1 : Schedule
            1st schedule
        sch2 : Schedule
            2nd schedule, having the same job list (and same tasks and machines etc) as schedule 1
    
        Returns a crossover schedule combining the 2 given ones
        -------
        This crossover function will select 'genes' pseudo uniformly randomly between the 2
        given schedules.
        'pseudo' means that whenever it's not possible to fit one gene into the new schedule for constraint
        reasons, the gene from the other given will be selected from the other given schedule. We will
        keep track of which schedule has participated more to the offspring to consequently calibrate
        the choice probabilities, therefore artificially keeping the participation of each gene to the 
        offspring close to 50%.
    """
    
    offspring = sc.Schedule([],[],[])
    # number of genes allocated to the offspring coming from schedule1 and schedule2
    balance_genes = [0,0]
    # probability to select a gene from schedule 1
    prob = 0.5
    
    for i in range(len(sch1.job_list)):
        #print("iteration",str(i))
        job1 = sch1.job_list[i].copy_job()
        job2 = sch2.job_list[i].copy_job()
        
        """
        for j in range(len(job1.list_tasks)):
            job1.list_tasks[j].print_task()
            job2.list_tasks[j].print_task()
        """
        p = random.uniform(0,1)
        
        if p<prob:
            flag = en.place_job_timetable(offspring,job1)
            # if the job(gene) from sch1 cannot be placed, place the corresponding one from sch2
            if flag:
                print("placed job1 case1")
            if not flag:
                flag = en.place_job_timetable(offspring,job2)
                if flag:
                    print("placed job2 case1")
                if not flag:
                    #if the crossover is not working, lauch it again
                    return uniform_crossover(sch1, sch2)
                balance_genes[1] +=1 #if we placed a job from schedule 2, increment counter for schedule 2
                offspring.job_list.append(job2.copy_job())
            offspring.job_list.append(job1.copy_job())
        else:
            flag = en.place_job_timetable(offspring,job2)
            
            if flag:
                print("placed job2 case 2")
            # if the job(gene) from sch2 cannot be placed, place the corresponding one from sch1
            if not flag:
                flag = en.place_job_timetable(offspring,job1)
                if flag:
                    print("placed job1 case2")
                if not flag:
                    #if the crossover is not working, lauch it again
                    return uniform_crossover(sch1, sch2)
                balance_genes[0] +=1 #if we placed a job from schedule 1, increment counter for schedule 1
                offspring.job_list.append(job1.copy_job())
            offspring.job_list.append(job2.copy_job())
        
        #prob = (balance_genes[0]+0.0) / (balance_genes[0]+balance_genes[1])
    return offspring
                
            
