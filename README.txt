
This program is aimed at computing weekly schedules for the QC lab. 

															BRIEF GUIDE TO THE DIFFERENT PARTS OF THE PROGRAM
					
					SCHEDULE:

OBJECTS

This file groups all the necessary objects to tackle the problem. The actors are "Machine" and "Analyst" objects. A sample test is represented as a "Job". Every phase of a sample test is represented as a "Task" (constituting the jobs).
A "Schedule" a list of jobs to schedule.

REPRESENTATION OF TIME

Time is represented using discrete units (1 unit = 6 minutes) arising from is considered relevant in solving this scheduling problem. Time will start at 0 (the lowest date at which a job starts) and goes generally to a month after 0. Timetables are used for the Analyst and Machine objects, to represent which task they carry out and when. A timetable which contains all the tasks is also used for the schedule object.

					ENCODING:

This file is essentailly a library used to "encode" the information of the objects into a genomic form. "Genomic form" here means that the information is usable by the genetoc algotithm.

					DATABASE_ACCESS:

This is used to get the data from the database (ranging from the id's if the machines usable for each job to the analyst's shift times).

					GENETIC_ALGORITHM:

This file contains the necessary functions to carry out the main genetic algorithm. The genetic algorithm operates as follows:
	- generates a certain number (pop_size) of schedules (a schedule is therefore a genome)
	- selects a mating pool. This done through the selection functions defined in the file.
	- mates the individuals randomly from the mating pool (crossover). After this step, there should be a mutation step applied to the obtained offsprings. However, this is already done in the crossover function.

					TEST_GENETIC:

This file contains testing code.

To launch the genetic algorithm, define a pop_size, a week from which to schedule, and a max_iteration parameter. then lauch:
		
		offsprings = ga.genetic_algorithm(pop_size, week_n,100) 

to get a list of randomly generated schedules, define the number of schedules to get (n) and the week number to draw them from (week_n), and type:
		
		schedules = encoding.random_schedules(n, week_n)





