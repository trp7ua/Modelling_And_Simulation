import Queue
import time
import random
import copy
import numpy as np
from genRandVel import returnRandomVelocity
import sys,getopt
import os
import rename
from time import sleep
import shutil
from globalVariables import signalStateList, segment_length_list, vehicle_arrival_rate, turning_rate, cycle_timing_list, total_cyle_length, signal_offset
from vehicleProperties import vehicle_mu, vehicle_sigma, vehicle_length_mu, vehicle_length_sigma, offset_between_vehicles
from creatingFutureEventLists import FELqueueing
from replace_file import replace

# For tracking the queues at all the intersections. Not being used now. 

queueList =[]
for i in range(10):
	q = Queue.PriorityQueue()
	queueList.append(q)

# Importing global variables from globalVariables file
signalStateList = signalStateList()
segment_length_list = segment_length_list()
vehicle_arrival_rate = vehicle_arrival_rate()
turning_rate = turning_rate()
cycle_timing_list = cycle_timing_list()
total_cyle_length = total_cyle_length()
signal_offset = signal_offset()

# Importing vehicle properties 
vehicle_mu = vehicle_mu()
vehicle_sigma = vehicle_sigma()
vehicle_length_mu = vehicle_length_mu()
vehicle_length_sigma = vehicle_length_sigma()
offset_between_vehicles = offset_between_vehicles()


# For generating the arrivals based on exponential distribution
def arrival_rate(lmda):
	return random.expovariate(lmda)

# FEL generator for each previous FEL and state variables and other dependencies based on Simulation Engine/Even handler
def FELqueueing(queue, vehicles, queue_copy, next_queue, last_queue, segment_num, segment_length_list, signal_offset):
	vehicle_number_in_queue = 0
	is_vehicle_first_in_queue = 1
	temp_time = 0
	
	if (last_queue == -1):
		while not queue.empty():
			temp = queue.get()
			velocity = temp[1][0]
			vehicle_length = temp[1][1]
			cur_temp_time = temp[0]

			if (temp[2] not in vehicles):
				queue_copy.put(temp)
				vehicles.append(temp[2])
			# make a set of car ids, if the car is not yet added then append

			if (is_vehicle_first_in_queue):
				travel_time = segment_length_list[0] / float(velocity) 
				next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
				is_vehicle_first_in_queue = 0
				vehicle_number_in_queue += 1
				temp_time = temp[0]
			else:
				if ( (cur_temp_time - temp_time) <= cycle_timing_list[0] ):
					if ((temp[0] % total_cyle_length) <= cycle_timing_list[0]  ):
						travel_time = segment_length_list[segment_num] / float(velocity) + vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) 
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
					else:
						travel_time = (cycle_timing_list[1] - (temp[0] % total_cyle_length - cycle_timing_list[0])) + segment_length_list[segment_num] / float(velocity) + vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity))
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
					vehicle_number_in_queue += 1
				else:
					temp_time = 0
					is_vehicle_first_in_queue = 1
					vehicle_number_in_queue = 0

					if ((temp[0] % total_cyle_length) <= cycle_timing_list[0]  ):
						travel_time = segment_length_list[segment_num] / float(velocity) + vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) 
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
					else:
						travel_time = (cycle_timing_list[1] - (temp[0] % total_cyle_length - cycle_timing_list[0])) + segment_length_list[segment_num] / float(velocity) + vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity))
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
	elif (last_queue == 0):
		while not queue.empty():
			temp = queue.get()
			velocity = temp[1][0]
			vehicle_length = temp[1][1]
			cur_temp_time = temp[0]

			if (temp[2] not in vehicles):
				queue_copy.put(temp)
				vehicles.append(temp[2])
			# make a set of car ids, if the car is not yet added then append

			if (is_vehicle_first_in_queue):
				travel_time = segment_length_list[0] / float(velocity) 
				next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
				is_vehicle_first_in_queue = 0
				vehicle_number_in_queue += 1
				temp_time = temp[0]
			else:
				if ( (cur_temp_time - temp_time) <= cycle_timing_list[0] ):
					if ((temp[0] % total_cyle_length) <= segment_num*signal_offset  ):
						travel_time = segment_length_list[segment_num] / float(velocity) + vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) 
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
					else:
						travel_time = segment_length_list[segment_num] / float(velocity) + vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) + segment_num*signal_offset 
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
					vehicle_number_in_queue += 1
				else:
					temp_time = 0
					is_vehicle_first_in_queue = 1
					vehicle_number_in_queue = 0

					if ((temp[0] % total_cyle_length) <= segment_num*signal_offset  ):
						travel_time = segment_length_list[segment_num] / float(velocity) + vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) 
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
					else:
						travel_time = segment_length_list[segment_num] / float(velocity) + vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) + segment_num*signal_offset
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))

	else:
		while not queue.empty():
			temp = queue.get()
			velocity = temp[1][0]
			vehicle_length = temp[1][1]
			cur_temp_time = temp[0]

			if (temp[2] not in vehicles):
				queue_copy.put(temp)
				vehicles.append(temp[2])
			# make a set of car ids, if the car is not yet added then append

			if (is_vehicle_first_in_queue):
				travel_time = segment_length_list[0] / float(velocity)
				next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
				is_vehicle_first_in_queue = 0
				vehicle_number_in_queue += 1
				temp_time = temp[0]
			else:
				if ( (cur_temp_time - temp_time) <= cycle_timing_list[0] ):
					if ((temp[0] % total_cyle_length) <= segment_num*signal_offset  ):
						travel_time =  vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) 
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
					else:
						travel_time =  vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) + segment_num*signal_offset 
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
					vehicle_number_in_queue += 1
				else:
					temp_time = 0
					is_vehicle_first_in_queue = 1
					vehicle_number_in_queue = 0

					if ((temp[0] % total_cyle_length)  <= segment_num*signal_offset  ):
						travel_time =  vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) 
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))
					else:
						travel_time = vehicle_number_in_queue* ((vehicle_length + offset_between_vehicles) / float(velocity)) + segment_num*signal_offset 
						next_queue.put((temp[0]+ travel_time, temp[1], temp[2]))

	return (next_queue, queue_copy, vehicles)

# Serving/Simulating each FEL/Queue and updating the state variables
def simulatingOneEntireTrip(queues, segment_length_list, north_to_south, signal_offset):
	global total_cyle_length
	global cycle_timing_list

	queue_copy = Queue.PriorityQueue()
	vehicles = []
	q_size  = 0
	if (north_to_south):
		queue = queues[0]
		queue1 = queues[1]
		queue2 = queues[2]
		queue3 = queues[3]
		queue4 = queues[4]

	else:
		queue = queues[5]
		queue1 = queues[6]
		queue2 = queues[7]
		queue3 = queues[8]
		queue4 = queues[9]

		segment_length_list.reverse()

	q_size = queue.qsize() + queue1.qsize() + queue2.qsize()+ queue3.qsize() + queue4.qsize()

	queue_final = Queue.PriorityQueue()

	segment_num = 0
	queue1, queue_copy, vehicles = FELqueueing(queue, vehicles, queue_copy, queue1, -1, segment_num, segment_length_list, signal_offset)

	total_cyle_length = total_cyle_length 
	
	segment_num = 1
	queue2, queue_copy, vehicles = FELqueueing(queue1, vehicles, queue_copy, queue2, 0, segment_num, segment_length_list, signal_offset)
	
	total_cyle_length = total_cyle_length 
	
	segment_num = 2
	queue3, queue_copy, vehicles = FELqueueing(queue2, vehicles, queue_copy, queue3, 0, segment_num, segment_length_list, signal_offset)

	total_cyle_length = total_cyle_length 
	
	segment_num = 3
	queue4, queue_copy, vehicles = FELqueueing(queue3, vehicles, queue_copy, queue4, 0, segment_num, segment_length_list, signal_offset)

	total_cyle_length = total_cyle_length 
	
	segment_num = 3
	queue_final, queue_copy, vehicles = FELqueueing(queue4, vehicles, queue_copy, queue_final, 1, segment_num, segment_length_list, signal_offset)
	
	print queue_final.qsize(), queue_copy.qsize()
	out = "final queue size: " +  str(queue_final.qsize())  + "\n"
	f2.write(out)
	
	return (queue_final, queue_copy)

# Main Event handler 
def Simulation_Engine(queues, signals, segment_length_list, signal_offset):
	#print queues[0].qsize()
	q_0 = queues[0]
	q_1 = queues[1]
	q_2 = queues[2]
	q_3 = queues[3]
	q_4 = queues[4]
	q_5 = queues[5]
	q_6 = queues[6]
	q_7 = queues[7]
	q_8 = queues[8]
	q_9 = queues[9]

	s_0 = signals[0]
	s_1 = signals[1]
	s_2 = signals[2]
	s_3 = signals[3]

	final_out_queue_at_south = Queue.PriorityQueue()
	final_out_queue_at_north = Queue.PriorityQueue()

	wait_times = []
	travel_times_NS = []
	travel_times_SN = []


	###### getting all the vehicles in one direction and their arrival and departure time #######
	# bool north to south or south to north
	# generally q_0 imply N to S and w_5 implies SOuth to North
	
	out_queue_at_south, q_0_copy = simulatingOneEntireTrip(queues, segment_length_list, 1, signal_offset)
	out_queue_at_north, q_5_copy = simulatingOneEntireTrip(queues, segment_length_list, 0, signal_offset)

	####### replacing priority queue's key which was time to vehicle id #####

	final_q_0_temp = Queue.PriorityQueue()
	final_q_5_temp = Queue.PriorityQueue()

	for i in range(q_0_copy.qsize()):
		temp = q_0_copy.get()
		temp = (temp[2], temp[0], temp[1])
		final_q_0_temp.put(temp)

	for i in range(q_5_copy.qsize()):
		temp = q_5_copy.get()
		temp = (temp[2], temp[0], temp[1])
		final_q_5_temp.put(temp)
	

	for i in range(out_queue_at_north.qsize()):
		temp = out_queue_at_north.get()
		temp = (temp[2], temp[0], temp[1])
		final_out_queue_at_north.put(temp)

	for i in range(out_queue_at_south.qsize()):
		temp = out_queue_at_south.get()
		temp = (temp[2], temp[0], temp[1])
		final_out_queue_at_south.put(temp)

	#### Calculating travel times for each vehicle ##########

	n = final_out_queue_at_south.qsize()
	m = final_out_queue_at_north.qsize()
	while (n):
		temp1 = final_out_queue_at_south.get()
		temp2 = final_q_0_temp.get()
		travel_time = temp1[1]-temp2[1]
		travel_times_NS.append(temp1[1]-temp2[1])
		out = str(temp1[0]) + "," + "NB" + "," + str(travel_time) + "," + str(temp1[1]) + "," + str(temp2[1]) + "," + str(temp1[2][0]) + "," + str(temp1[2][1]) + '\n'
		f2.write(out)
		n -= 1
	
	while(m):
		temp1 = final_out_queue_at_north.get()
		temp2 = final_q_5_temp.get()
		travel_time = temp1[1]-temp2[1]
		travel_times_SN.append(temp1[1]-temp2[1])
		out = str(temp1[0]) + "," + "SB" + "," + str(travel_time)  + "," + str(temp1[1])  + "," + str(temp2[1]) + "," + str(temp1[2][0]) + "," + str(temp1[2][1]) + '\n'
		f2.write(out)
		m-=1

	ns_travel_time = np.mean(travel_times_NS)
	sn_travel_time = np.mean(travel_times_SN)
	print ns_travel_time
	print sn_travel_time	
	travel_times = travel_times_NS + travel_times_SN
	
	return (ns_travel_time, sn_travel_time)

# An Approximate method to randomly make turns with a given rate at each intersection
def maintainTurns(queue, rate):
	# does 2 things: makes turn for each queue based on the given rate and makes arrival time as the key 
	n = queue.qsize()
	new_queue = Queue.PriorityQueue()

	for i in range(n):
		if random.random() < rate:
			temp = queue.get()
			
	while (not queue.empty()):
		temp = queue.get()
		new_queue.put ((temp[1], temp[2], temp[3]))
	return new_queue


# Initial FEL handler/generator: Maintain arrival events
def trafficSim(lmda, lmda2, segment_length_list, cycle_timing_list, simulation_time):
	
	Vehicles = []
	global f1
	global f2

	s_0 = signalStateList[0]
	s_1 = signalStateList[1]
	s_2 = signalStateList[2]
	s_3 = signalStateList[3]

	q_0 = queueList[0]
	q_1 = queueList[1]
	q_2 = queueList[2]
	q_3 = queueList[3]
	q_4 = queueList[4]
	q_5 = queueList[5]
	q_6 = queueList[6]
	q_7 = queueList[7]
	q_8 = queueList[8]
	q_9 = queueList[9]

	car_id_0 = 0
	car_id_1 = 0
	car_id_2 = 0
	car_id_3 = 0
	car_id_4 = 0
	car_id_5 = 0
	car_id_6 = 0
	car_id_7 = 0
	car_id_8 = 0
	car_id_9 = 0

	veh_id = 0

	t = 0
	while (t < simulation_time):

		curr_time = t
		service_time = 0
		signal_times = []

		# Intersection 1 Main North
		lmda1 = vehicle_arrival_rate[0]
		lmbda_side = vehicle_arrival_rate[1]
		temp_time_0 = arrival_rate(lmda)
		loop_time = temp_time_0
		if (random.random() < lmda1):
			temp_time_0 = arrival_rate(lmda)
			loop_time = temp_time_0
			car_id_0 += 1 
			#velocity = random.randint(6,10) # Instead of the car velocity we can define car categories/types with properties (speed, length) and append that class type in priority queue
			#velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			velocity = returnRandomVelocity(1)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_0.put((rand_for_maintaining_turns,temp_time_0+t, car_property, car_id_0))
			out = str(car_id_0) + ',' +  "NB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q0") + ',' + "1"+ '\n' #intesection
			f1.write(out)

		# adding a vehicle from side with very less probability
		if (random.random() < lmbda_side): #for vehicle from left
			temp_time_0 = arrival_rate(lmda1)
			car_id_0 += 1
			#velocity = random.randint(6,10)
			#velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			velocity = returnRandomVelocity(1)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_0.put((rand_for_maintaining_turns,temp_time_0+t, car_property, car_id_0))
			out = str(car_id_0) + ',' + "NB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q0") + ',' + "1"+ '\n'
			f1.write(out)

		if (random.random() < lmbda_side): #for vehicle from right
			lmbda_side = vehicle_arrival_rate[5]
			temp_time_0 = arrival_rate(lmda1)
			car_id_5 += 1
			#velocity = random.randint(6,10)
			#velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			velocity = returnRandomVelocity(1)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_9.put((rand_for_maintaining_turns,temp_time_0+t, car_property, car_id_5))
			out = str(car_id_5) + ',' + "SB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q9") + ',' + "1"+ '\n'
			f1.write(out)

		# Intersection 2 intermediate

		lmbda_side = vehicle_arrival_rate[2] # for vehicle from right
		if (random.random() < lmbda_side):
			temp_time_0 = arrival_rate(lmda1)
			car_id_0 += 1
			#velocity = random.randint(6,10)
			velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			#velocity = returnRandomVelocity(2)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_1.put((rand_for_maintaining_turns,temp_time_0+t, car_property, car_id_0))
			out = str(car_id_0) + ',' + "NB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q1") + ',' + "2"+ '\n'
			f1.write(out)


		lmbda_side = vehicle_arrival_rate[2] #for vehicle from left
		if (random.random() < lmbda_side):
			temp_time_0 = arrival_rate(lmda1)
			car_id_5 += 1
			#velocity = random.randint(6,10)
			velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			#velocity = returnRandomVelocity(2)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_8.put((rand_for_maintaining_turns, temp_time_0+t, car_property, car_id_5))
			out = str(car_id_5) + ',' + "SB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q8") + ',' + "2"+ '\n'
			f1.write(out)


		# Intersection 3 intermediate

		lmbda_side = vehicle_arrival_rate[3] # for vehicle from right
		if (random.random() < lmbda_side):
			temp_time_0 = arrival_rate(lmda1)
			car_id_0 += 1
			#velocity = random.randint(6,10)
			velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			#velocity = returnRandomVelocity(3)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_2.put((rand_for_maintaining_turns, temp_time_0+t, car_property, car_id_0))
			out = str(car_id_0) + ',' + "NB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q2") + ',' + "3"+ '\n'
			f1.write(out)

		lmbda_side = vehicle_arrival_rate[3] #for vehicle from left
		if (random.random() < lmbda_side):
			temp_time_0 = arrival_rate(lmda1)
			car_id_5 += 1
			#velocity = random.randint(6,10)
			velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			#velocity = returnRandomVelocity(3)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_7.put((rand_for_maintaining_turns, temp_time_0+t, car_property, car_id_5))
			out = str(car_id_5) + ',' + "SB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q7") + ',' + "3"+ '\n'
			f1.write(out)

		# Intersection 4 intermediate

		lmbda_side = vehicle_arrival_rate[4] # for vehicle from right
		if (random.random() < lmbda_side):
			temp_time_0 = arrival_rate(lmda1)
			car_id_0 += 1
			#velocity = random.randint(6,10)
			velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			#velocity = returnRandomVelocity(4)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_3.put((rand_for_maintaining_turns, temp_time_0+t, car_property, car_id_0))
			out = str(car_id_0) + ',' + "NB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q3") + ',' + "4"+ '\n'
			f1.write(out)

		lmbda_side = vehicle_arrival_rate[4] #for vehicle from left
		if (random.random() < lmbda_side):
			temp_time_0 = arrival_rate(lmda1)
			car_id_5 += 1
			#velocity = random.randint(6,10)
			velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			#velocity = returnRandomVelocity(4)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_6.put((rand_for_maintaining_turns, temp_time_0+t, car_property, car_id_5))
			out = str(car_id_5) + ',' + "SB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q6") + ',' + "4"+ '\n'
			f1.write(out)

		# S to N Main entry: Last Intersection
		lmda1 = vehicle_arrival_rate[-1]
		if (random.random() < lmda1):
			temp_time_5 = arrival_rate(lmda2)
			car_id_5 += 1
			#velocity = random.randint(6,10)
			velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			#velocity = returnRandomVelocity(5)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_5.put((rand_for_maintaining_turns, temp_time_5+t, car_property, car_id_5))
			out = str(car_id_5) + ',' + "SB" + ',' + str(temp_time_5+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q5") + ',' +  "5"+ '\n'
			f1.write(out)	

		lmbda_side = vehicle_arrival_rate[4] #for vehicle from left
		if (random.random() < lmbda_side):
			temp_time_0 = arrival_rate(lmda1)
			car_id_0 += 1
			#velocity = random.randint(6,10)
			velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			#velocity = returnRandomVelocity(6)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_4.put((rand_for_maintaining_turns, temp_time_0+t, car_property, car_id_0))
			out = str(car_id_0) + ',' + "NB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q4") + ',' + "5"+ '\n'
			f1.write(out)

		lmbda_side = vehicle_arrival_rate[5] #for vehicle from right
		if (random.random() < lmbda_side):
			temp_time_0 = arrival_rate(lmda1)
			car_id_5 += 1
			#velocity = random.randint(6,10)
			velocity = np.random.normal(vehicle_mu, vehicle_sigma)
			#velocity = returnRandomVelocity(6)
			length = np.random.normal(vehicle_length_mu, vehicle_length_sigma)
			car_property = (velocity, length)
			rand_for_maintaining_turns = random.randint(1, 100000)
			q_5.put((rand_for_maintaining_turns, temp_time_0+t, car_property, car_id_5))
			out = str(car_id_5) + ',' + "SB" + ',' + str(temp_time_0+t) + ',' + str(velocity) + ',' + str(length) + ',' + str("q5") + ',' + "5" + '\n'
			f1.write(out)

		t += loop_time
	
	######## Maintaining right and left turns for each queue based on input data ############		

	queueList[0] = q_0
	queueList[1] = q_1
	queueList[2] = q_2
	queueList[3] = q_3
	queueList[4] = q_4
	queueList[5] = q_5
	queueList[6] = q_6
	queueList[7] = q_7
	queueList[8] = q_8
	queueList[9]=  q_9
	
	print "Total number of vehicles entering queue # : "
	for i in range(10):
		enter = queueList[i].qsize()
		queueList[i] = maintainTurns(queueList[i], turning_rate[i])
		exited = queueList[i].qsize()
		out =  "queue # " + str(i) + " entering: " + str(enter) + " \t and after exit: " + str(exited) + '\n'
		f2.write(out) 

	signal_offset = random.randint(4,15)
	#print signal_offset
	out = "Signal Offset NS and SN: " + str(signal_offset) + '\n'
	f2.write(out)
	
	final_average_travel_times = Simulation_Engine(queueList, signalStateList, segment_length_list, signal_offset)
	#print final_average_travel_time
	return final_average_travel_times

# Process Oriented Simulation Model
def processBasedSimulation(simulation_num):
	#global f1
	#global f2
	f1 = open("./output/input.csv" , "w")
	f2 = open("./output/output.csv", "w")
	global f1
	global f2
	avg_trvl_time_ns, avg_trvl_time_sn = trafficSim(0.45,0.5, segment_length_list, cycle_timing_list, 900)
	
	avg_trvl_time_ns, avg_trvl_time_sn = int(avg_trvl_time_ns), int(avg_trvl_time_sn)
	
	path = "./output/"
	path2 = "./synchronized/"
	in_file = "input.csv"
	out_file = "output.csv"

	file_name1 =  str(simulation_num) + "_" + in_file + "_" +  str(avg_trvl_time_ns) + "_" + str(avg_trvl_time_sn)
	file_name2 =  str(simulation_num) + "_" +out_file + "_" + str(avg_trvl_time_ns) + "_" + str(avg_trvl_time_sn)
	
	replace(path, in_file, file_name1)
	replace(path, out_file, file_name2)


	f1.close()
	f2.close()
	src = path + file_name1
	dest = path2 + file_name1
	shutil.move(src, dest)

	src = path + file_name2
	dest = path2 + file_name2
	shutil.move(src, dest)

	return (avg_trvl_time_ns, avg_trvl_time_sn)

