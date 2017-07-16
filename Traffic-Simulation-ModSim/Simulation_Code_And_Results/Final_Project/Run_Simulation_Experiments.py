import os
from Process_Synchronized import processBasedSimulation
#from Process_Unsynchronized_And_Spillover import processBasedSimulation
#from Process_Unsynchronized_backup import processBasedSimulation



for i in range(500):
	simulation_num = i
	avg_trvl_time_ns, avg_trvl_time_sn = processBasedSimulation(simulation_num)

	