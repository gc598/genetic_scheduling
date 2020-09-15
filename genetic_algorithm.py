# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 12:00:03 2020

@author: Gabriel
"""

"""
This file uses the data structures (objects) of schedule.py and the processing functions of encoding.py
to run the genetic algorithm itself.
The main genetic components are also defined here, such as crossings, mutation, and selection procedures.
"""

import numpy as np
import schedule as sc
import encoding as en
import random
import copy

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
    
    
    offspring = sc.Schedule(timetable=[],job_list=[],analysts=[],machines=[])
    offspring.max_time = max(sch1.max_time,sch2.max_time)
    offspring.min_time = min(sch1.min_time,sch2.min_time)
    for analyst in sch1.analysts:
        offspring.analysts.append(analyst.copy_essential_analyst())
    for mac_id in range(len(sch1.machines)):
        offspring.machines.append([])
        for machine in sch1.machines[mac_id]:
            offspring.machines[mac_id].append(machine.copy_essential_machine())
    offspring.job_dict_id = sch1.job_dict_id
            
    
    # number of genes allocated to the offspring coming from schedule1 and schedule2
    balance_genes = [0,0]
    # probability to select a gene from schedule 1
    prob = 0.5
    
    sorted_jobs1 = sch1.get_sorted_list_jobs()
    sorted_jobs2 = sch2.get_sorted_list_jobs()
    
    for i in range(len(sorted_jobs1)):
        job1 = copy.deepcopy(sorted_jobs1[i])
        job2 = copy.deepcopy(sorted_jobs2[i])
        
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
            offspring.update_dictionary()
    return offspring

# version with sorted jobs by start time
def pseudo_crossover_sorted(sch1,sch2):
    
    if len(sch1.timetable) != len(sch2.timetable):
        return None
    
    offspring = sc.Schedule(timetable=[],job_list=[],analysts=[],machines=[])
    offspring.max_time = max(sch1.max_time,sch2.max_time)
    offspring.min_time = min(sch1.min_time,sch2.min_time)
    for analyst in sch1.analysts:
        offspring.analysts.append(analyst.copy_essential_analyst())
    for mac_id in range(len(sch1.machines)):
        offspring.machines.append([])
        for machine in sch1.machines[mac_id]:
            offspring.machines[mac_id].append(machine.copy_essential_machine())
    offspring.job_dict_id = sch1.job_dict_id 
    
    # job_ids_placed contains the job_id of the jobs that could
    # be placed in the timetable
    job_ids_placed = []
    # count_placed counts the number of jobs put into the timetable
    count_placed = 0
    
    jobs1 = sch1.job_list
    jobs2 = sch2.job_list
    
    sorted_jobs1 = copy.deepcopy(sch1.get_sorted_list_jobs())
    sorted_jobs2 = copy.deepcopy(sch2.get_sorted_list_jobs())
    
    prob = 0.5
    
    
    for i in range(len(sorted_jobs1)):
        p = random.uniform(0,1)
        flag = False
        
        job1 = copy.deepcopy(sorted_jobs1[i])
        job2 = copy.deepcopy(sorted_jobs2[i])
        
        if p < prob:
            if job1.job_id not in job_ids_placed:
                flag = en.place_job_timetable(offspring,job1)
            if flag:
                job_ids_placed.append(job1.job_id)
                offspring.job_list.append(job1)
            else:
                if job2.job_id not in job_ids_placed:
                    flag = en.place_job_timetable(offspring,job2)
                if flag:
                    job_ids_placed.append(job2.job_id)
                    offspring.job_list.append(job2)
        else:
            if job2.job_id not in job_ids_placed:
                flag = en.place_job_timetable(offspring,job2)
            if flag:
                job_ids_placed.append(job2.job_id)
                offspring.job_list.append(job2)
            else:
                if job1.job_id not in job_ids_placed:    
                    flag = en.place_job_timetable(offspring,job1)
                if flag:
                    job_ids_placed.append(job1.job_id)
                    offspring.job_list.append(job1)
        if flag:
            count_placed +=1
        
    
    
    for job in sorted_jobs1:
        if job.job_id not in job_ids_placed:
            job = copy.deepcopy(job)
            en.randomly_place_job_timetable(job, offspring)
            offspring.job_list.append(job)
            
    print((count_placed/len(sch1.job_list))*100,"%")
    print(job_ids_placed)
    return offspring
    
# normal version
def pseudo_crossover_normal(sch1,sch2):
    
    if len(sch1.timetable) != len(sch2.timetable):
        return None
    
    offspring = sc.Schedule(timetable=[],job_list=[],analysts=[],machines=[])
    offspring.max_time = max(sch1.max_time,sch2.max_time)
    offspring.min_time = min(sch1.min_time,sch2.min_time)
    for analyst in sch1.analysts:
        offspring.analysts.append(analyst.copy_essential_analyst())
    for mac_id in range(len(sch1.machines)):
        offspring.machines.append([])
        for machine in sch1.machines[mac_id]:
            offspring.machines[mac_id].append(machine.copy_essential_machine())
    offspring.job_dict_id = sch1.job_dict_id 
    
    # job_ids_placed contains the job_id of the jobs that could
    # be placed in the timetable
    job_ids_placed = []
    # count_placed counts the number of jobs put into the timetable
    count_placed = 0
    
    jobs1 = sch1.job_list
    jobs2 = sch2.job_list
    
    sorted_jobs1 = copy.deepcopy(sch1.get_sorted_list_jobs())
    sorted_jobs2 = copy.deepcopy(sch2.get_sorted_list_jobs())
    
    prob = 0.5
    
    
    for i in range(len(jobs1)):
        p = random.uniform(0,1)
        flag = False
        
        job1 = copy.deepcopy(jobs1[i])
        job2 = copy.deepcopy(jobs2[i])
        
        if p < prob:
            flag = en.place_job_timetable(offspring,job1)
            if flag:
                job_ids_placed.append(job1.job_id)
                offspring.job_list.append(job1)
            else:
                flag = en.place_job_timetable(offspring,job2)
                if flag:
                    job_ids_placed.append(job2.job_id)
                    offspring.job_list.append(job2)
        else:
            flag = en.place_job_timetable(offspring,job2)
            if flag:
                job_ids_placed.append(job2.job_id)
                offspring.job_list.append(job2)
            else:
                flag = en.place_job_timetable(offspring,job1)
                if flag:
                    job_ids_placed.append(job1.job_id)
                    offspring.job_list.append(job1)
        if flag:
            count_placed +=1
        
    
    
    for job in jobs1:
        if job.job_id not in job_ids_placed:
            job = copy.deepcopy(job)
            en.randomly_place_job_timetable(job, offspring)
            offspring.job_list.append(job)
            
    print((count_placed/len(sch1.job_list))*100,"%")
    print(job_ids_placed)
    return offspring 

# version that uses randomly rearranged lists of jobs
def pseudo_crossover(sch1,sch2):
    
    if len(sch1.timetable) != len(sch2.timetable):
        return None
    
    offspring = sc.Schedule(timetable=[],job_list=[],analysts=[],machines=[])
    offspring.max_time = max(sch1.max_time,sch2.max_time)
    offspring.min_time = min(sch1.min_time,sch2.min_time)
    for analyst in sch1.analysts:
        offspring.analysts.append(analyst.copy_essential_analyst())
    for mac_id in range(len(sch1.machines)):
        offspring.machines.append([])
        for machine in sch1.machines[mac_id]:
            offspring.machines[mac_id].append(machine.copy_essential_machine())
    offspring.job_dict_id = sch1.job_dict_id 
    
    # job_ids_placed contains the job_id of the jobs that could
    # be placed in the timetable
    job_ids_placed = []
    # count_placed counts the number of jobs put into the timetable
    count_placed = 0
    
    indices = np.arange(len(sch1.job_list))
    np.random.shuffle(indices)
    
    jobs1 = [sch1.job_list[i] for i in indices]
    jobs2 = [sch2.job_list[i] for i in indices]
    
    
    prob = 0.5
    
    
    for i in range(len(jobs1)):
        p = random.uniform(0,1)
        flag = False
        
        job1 = copy.deepcopy(jobs1[i])
        job2 = copy.deepcopy(jobs2[i])
        
        if p < prob:
            flag = en.place_job_timetable(offspring,job1)
            if flag:
                job_ids_placed.append(job1.job_id)
                offspring.job_list.append(job1)
            else:
                flag = en.place_job_timetable(offspring,job2)
                if flag:
                    job_ids_placed.append(job2.job_id)
                    offspring.job_list.append(job2)
        else:
            flag = en.place_job_timetable(offspring,job2)
            if flag:
                job_ids_placed.append(job2.job_id)
                offspring.job_list.append(job2)
            else:
                flag = en.place_job_timetable(offspring,job1)
                if flag:
                    job_ids_placed.append(job1.job_id)
                    offspring.job_list.append(job1)
        if flag:
            count_placed +=1
        
    
    
    for job in jobs1:
        if job.job_id not in job_ids_placed:
            job = copy.deepcopy(job)
            en.randomly_place_job_timetable(job, offspring)
            offspring.job_list.append(job)
            
    #print((count_placed/len(sch1.job_list))*100,"%")
    #print(job_ids_placed)
    return offspring               
                
        
def mutation(sch,p,n):
    """
    This function will carry out a mutation on a gene, ie a schedule.
    It will select n jobs from the schedule, and change their starting and end times randomly, (also 
    updating the affected analysts and machine's timetables'), with probability p.
    The new starting and end times will be random.
    """
    if n>len(sch.job_list):
        return None
    mutant = copy.deepcopy(sch)
    i=0
    #we will shuffle sch's list of jobs so we have no bias in which jobs are to be modified
    shuffled_jobs = mutant.job_list
    random.shuffle(shuffled_jobs)
    #jobs_to_mutate holds the list of jobs to modify after randomly selecting them from shuffled_jobs
    jobs_to_mutate = []
    for i in range(n):
        r= random.uniform(0,1)
        if r<p:
            jobs_to_mutate.append(shuffled_jobs[i])
            en.remove_job_from_timetable(mutant,shuffled_jobs[i])
            
    
    max_time = sch.max_time
    
    
    for job in jobs_to_mutate:
        print("exec")
        
        
        current_task = job.list_tasks[0]
        start_time = random.randint(current_task.earliest_start_time,max_time-current_task.duration)
        current_task.start_time = start_time
        current_task.end_time = current_task.start_time + current_task.duration
        if current_task not in mutant.timetable:
            en.place_task_timetable(mutant,current_task)
        
        for i in range(1,len(job.list_tasks)):
            current_task = job.list_tasks[i]
            prev_task = job.list_tasks[i-1]
            max_separation_duration = job.max_separation_durations[i] #max time between end of i-1 and start of i
            start_time = random.randint(prev_task.end_time,prev_task.end_time+random.randint(0,max_separation_duration))
            current_task.start_time = start_time
            current_task.end_time = current_task.start_time + current_task.duration
            flag = 0
            if current_task not in mutant.timetable:
                flag=en.place_task_timetable(mutant,current_task)
            #if it's not possible to fit this job in the schedule, we restart the function
            if(current_task.end_time > max_time or flag==-1):  
                return mutation(sch,p,n)
    return mutant

def best_schedule_index(schedules):
    """
    

    Parameters
    ----------
    schedules : array of schedules
        DESCRIPTION.

    Returns the index of the best schedule according to fitness values.


    """
    
    current_best_fitness = 0
    current_best_index = 0
    for i in range(len(schedules)):
        fit = schedules[i].fitness_val()
        if fit > current_best_fitness:
            current_best_fitness = fit
            current_best_index = i
    return current_best_index


# infinite loop when there are too many 0 proability schedules, which is the case for small (non realistic)
#test cases
def roulette_wheel_selection(p_selection,schedules):
    
    """
    Roulette wheel selection is used to select individuals proportionally to their fitness value.
    High fitness individuals will have a higher probabililty to be selected.
    
    schedules: array of all schedules
    p_selection: proportion of chromosomes that will produce offsprings. Every selected schedule will 
        participate in creating 1/p_selection offspring to keep the total popoulation constant
    """

    pop_size = len(schedules)
    
    # probabilities of selecting every chromosome 
    prob = np.zeros(pop_size)
    
    total_fitness = 0
    for i in range(pop_size):
        prob[i] = schedules[i].fitness_val()
        total_fitness += prob[i]
    prob=np.divide(prob,total_fitness+0.0)
    #print(prob,prob.sum())
    
    n_parents = int(pop_size*p_selection)
    parents = []
    
    i=0
    while i < n_parents:
        #print("length parents",len(parents))
        part_sum = 0
        index = 0
        p = np.random.rand()
        #search schedules according to their probability of selection
        while part_sum < p:
            part_sum += prob[index]
            index +=1
        try:
            if schedules[index] not in parents:
                #print("not in parents")
                parents.append(schedules[index])
                i +=1
        except:
            if schedules[-1] not in parents:
                parents.append(schedules[-1])
    return parents


def elitist_selection(p_selection,schedules):
    
    """
    This defines the simplest type of selection. Only the best proportion of individuals will be selected
    to produce offspring. 
    schedules: array of all schedules
    p_selection: proportion of chromosomes that will produce offsprings. Every selected schedule will 
        participate in creating 1/p_selection offspring to keep the total popoulation constant
    """
    
    pop_size = len(schedules)
    n_parents = int(pop_size*p_selection)
    
    # we create an array with the fitness values of all schedules

    fitness_selection = np.arange(pop_size)
    for i in range(pop_size):
        fitness_selection[i] = schedules[i].fitness_val()
    #sort indices contains the indices of the best schedules in ascending order (worst to best)
    sort_indices = np.argsort(fitness_selection)
    
    #print(fitness_selection)
    
    parents = []
    for i in range(n_parents):
        parents.append(schedules[sort_indices[pop_size-1-i]])
    return parents



def tournament_selection(p_selection,n_tournament,schedules):
    
    """
    tournament_selection chooses random samples of schedules, and makes them go through a tournament
    i.e. only the best individual of the sample is selected to become a parent and produce offsprings.
    p_selection: proportion of chromosomes that will produce offsprings. Every selected schedule will 
        participate in creating 1/p_selection offspring to keep the total popoulation constant
    n_tournament: number of contestants in each tournament
    """    
    
    pop_size = len(schedules)
    n_parents = int(pop_size*p_selection)
    # tournament will contain the schedules of each tournament
    parents = []
    
    
    for i in range(n_parents):
        tournament = []
        # indices contains random indices from which to select the schedules for the tournament
        indices = np.arange(pop_size)
        np.random.shuffle(indices)
        for j in range(n_tournament):
            tournament.append(schedules[indices[j]])
        # we find the index of the best schedule from the tournament
        best_index_from_tournament = best_schedule_index(tournament)
        # we add the best schedule from the tournament to the list of future offspring producers
        if tournament[best_index_from_tournament] not in parents:
            parents.append(tournament[best_index_from_tournament])
    
    # if the number of selected shedules is less than n_parents, fill the rest randomly
    tmp = [sch for sch in schedules if sch not in parents]
    if len(parents) < n_parents:
        rest_to_add = n_parents-len(parents)
        np.random.shuffle(tmp)
        for i in range(rest_to_add):
            parents.append(tmp[i])
            
    return parents

def genetic_algorithm(pop_size,week_n,max_iter):
     
    schedules = en.random_schedules(pop_size,week_n)
    p_select_roulette = 0.25
    p_select_elite = 0.5
    p_select_tournament = 0.25
    n_tournament = int(pop_size/10)
    it = 0
    parents = []
    offsprings = []
    
    """
    the main while loop carries out the selection proces to get the pooling mates
    (i.e. the set of parents), which will then randomly produce offsprings
    """

    while it < max_iter:
    
        print("iteration: ",it)
    
        parents_tournament = tournament_selection(p_select_tournament,
                                                  n_tournament, schedules)
        parents_elite = elitist_selection(p_select_elite, schedules)
        parents_roulette = roulette_wheel_selection(p_select_roulette, schedules)
        
        # first we select all parents from the roulette wheel and elitist selections
        parents = parents_elite + parents_roulette + parents_tournament
        
        # parents probably contains duplicates so we remove them
        parents = list(dict.fromkeys(parents))
            
        # if parents are still missing, we select them randomly from the ones that are not
        # yet selected
        not_selected = [sch for sch in schedules]
        for i in range(pop_size-len(parents)):
            parents.append(not_selected[i])
    
        """
        Now we apply the crossover part. Here
        we will select pop_size couples (possibly there will be twice the same), each
        one of which will produce one offspring.
        """
        
        offsprings = []
        for i in range(pop_size):
            
            # we select 2 random parents to produce an offspring
            parent1_index = np.random.randint(pop_size)
            parent2_index = np.random.randint(pop_size)
            
            offspring = pseudo_crossover(parents[parent1_index], parents[parent2_index])
            offsprings.append(offspring)
            
        # the produced offsprings become the next generation of parents
        parents = offsprings
        it += 1

    
    return offsprings

        
    

    
    
    
    