#Creating Future Event Lists

from globalVariables import signalStateList, segment_length_list, vehicle_arrival_rate, turning_rate, cycle_timing_list, total_cyle_length, signal_offset

# Importing global variables from globalVariables file
signalStateList = signalStateList()
segment_length_list = segment_length_list()
vehicle_arrival_rate = vehicle_arrival_rate()
turning_rate = turning_rate()
cycle_timing_list = cycle_timing_list()
total_cyle_length = total_cyle_length()
signal_offset = signal_offset()

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