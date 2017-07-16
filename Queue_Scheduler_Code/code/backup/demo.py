import Queue
import random
import numpy as np


def generate_req(n):
	l = [i for i in range(n)]
	a = l[random.randint(0,n-1)]
	l.pop(a)
	k= random.randint(0,n-2)
	b = l[k]
	return (a,b)

def generate_serving_rates(n):
	rates = []
	for i in range(n):
		#rates.append(int(10*random.random()))
		rates.append(random.random())
	return rates

def expo_rate(lmda):
	return random.expovariate(lmda)

num_server = 5
nodes = {0:0,1:0,2:0,\
			3:1,4:1}

num_nodes = len(nodes)
node_throughput = generate_serving_rates(num_nodes)
#node_throughput = [0.1,0.1,0.05,0.05,0.1]
node_queue_length = [15,10]


num_requests = 100
simulation_time = 100
look_ahead_time = 2
#server_rates = generate_serving_rates(num_server)
arrival_rates = generate_serving_rates(num_server)

server_req_queue = []
for i in range(num_server):
	q = Queue.PriorityQueue()
	server_req_queue.append(q)


def count_less_time_stamps(l1, threshold):
	#l2 = [i for i in l1 if i > threshold]
	l2 = []
	for i in l1:
		if i > threshold:
			#print i
			#print l2
			l2.append(i)
			l1.pop(l1.index(i))

	return (l2, l1, len(l1) - len(l2))

def serving_tail_drop_nodes(FEL0, FEL1, num, final_time):
	serve_count = 0
	
	buffer_FEL0 = []
	buffer_FEL1 = []
	temp_FEL0 = []
	temp_FEL1 = []
	prev_bufefer0_time = 0
	prev_bufefer1_time = 0

	buffer0_length = []
	buffer1_length = []

	curr_time = 0
	while (curr_time < final_time):
		service0 = FEL0.get()
		service1 = FEL1.get()
		if (service0[0] <= service1[0]):
			FEL1.put(service1)
			if (service0[3]):
				temp_FEL0.append(service0[0])
				temp_FEL0, old_temp_FEL0, count_lesser = count_less_time_stamps(temp_FEL0, curr_time)
				print temp_FEL0
				count_served_in_buffer0 = (curr_time - prev_bufefer0_time)*node_throughput[0]
				if (len(buffer0_length) + count_lesser - count_served_in_buffer0 ) <= node_queue_length[0]:
					
					buffer_FEL0, old_buffer_FEL0, count_buffer = count_less_time_stamps(buffer_FEL0, curr_time)
					#print buffer_FEL0, old_buffer_FEL0, count_buffer 
					for i in old_temp_FEL0:
						if i > prev_bufefer0_time:
							buffer_FEL0.append(i)
					buffer0_length.append(len(buffer_FEL0))

					prev_bufefer0_time = curr_time
				else:
					buffer0_length.append(node_queue_length[0])
			else:
				service0[3] = 1
				service0[0] += look_ahead_time
				FEL1.put(service0)
				temp_FEL0.append(service0[0] + look_ahead_time)
				temp_FEL0, old_temp_FEL0, count_lesser = count_less_time_stamps(temp_FEL0, curr_time)
				count_served_in_buffer0 = (curr_time - prev_bufefer0_time)*node_throughput[0]
				if (len(buffer0_length) + count_lesser - count_served_in_buffer0 ) <= node_queue_length[0]:
					
					buffer_FEL0, old_buffer_FEL0, count_buffer = count_less_time_stamps(buffer_FEL0, curr_time)
					for i in old_temp_FEL0:
						if i > prev_bufefer0_time:
							buffer_FEL0.append(i)
					buffer0_length.append(len(buffer_FEL0))

					prev_bufefer0_time = curr_time
				else:
					buffer0_length.append(node_queue_length[0])
			


			print len(buffer_FEL0)
			prev_bufefer0_time = curr_time
			curr_time += service0[0]
		else:
			FEL0.put(service0)
			if (service1[3]):
				temp_FEL1.append(service1[0])
				temp_FEL1, old_temp_FEL1, count_lesser = count_less_time_stamps(temp_FEL1, curr_time)
				count_served_in_buffer1 = (curr_time - prev_bufefer1_time)*node_throughput[1]
				if (len(buffer1_length) + count_lesser - count_served_in_buffer1 ) <= node_queue_length[1]:
					
					buffer_FEL1, old_buffer_FEL1, count_buffer = count_less_time_stamps(buffer_FEL1, curr_time)
					for i in old_temp_FEL1:
						if i > prev_bufefer1_time:
							buffer_FEL1.append(i)
					buffer1_length.append(len(buffer_FEL1))

					prev_bufefer1_time = curr_time
				else:
					buffer1_length.append(node_queue_length[1])
			else:
				service1[3] = 1
				service1[0] += look_ahead_time
				FEL0.put(service1)
				temp_FEL1.append(service1[0])
				temp_FEL1, old_temp_FEL1, count_lesser = count_less_time_stamps(temp_FEL1, curr_time)
				count_served_in_buffer1 = (curr_time - prev_bufefer1_time)*node_throughput[1]
				if (len(buffer1_length) + count_lesser - count_served_in_buffer1 ) <= node_queue_length[1]:
					
					buffer_FEL1, old_buffer_FEL1, count_buffer = count_less_time_stamps(buffer_FEL1, curr_time)
					for i in old_temp_FEL1:
						if i > prev_bufefer1_time:
							buffer_FEL1.append(i)
					buffer1_length.append(len(buffer_FEL1))

					prev_bufefer1_time = curr_time
				else:
					buffer1_length.append(node_queue_length[1])
			print len(buffer_FEL0)
			prev_bufefer1_time = curr_time
			curr_time += service1[0]

			
def tail_drop_simulation():
	FEL0 = Queue.PriorityQueue()
	FEL1 = Queue.PriorityQueue()
	FEL0_size = 0
	FEL1_size = 0
	count = 0
	curr_time = 0 # time varialble
	
	#mean_arrival_rate = np.mean(arrival_rates)

	while count < num_requests:
		count += 1
		a, b = generate_req(num_server)
		temp_arrival_rate = arrival_rates[a]
		temp_time = expo_rate(temp_arrival_rate)
		curr_time += temp_time

		if (nodes[a] == 0):
			#if FEL0_size < node_queue_length[0]:
			# we can also accept/reject with some probability here instead of taildrop later
			if nodes[a] == nodes[b]:
				FEL0.put([curr_time, a, b, 1]) # last value is for checking whether source and destination are on same node else 0
			else:
				FEL0.put([curr_time, a, b, 0])
			FEL0_size += 1
		else:
			#if FEL1_size < node_queue_length[1]:
			if nodes[a] == nodes[b]:
				FEL1.put([curr_time, a, b, 1]) # last value is for checking whether source and destination are on same node else 0
			else:
				FEL1.put([curr_time, a, b, 0])
			FEL1_size += 1

	serving_tail_drop_nodes(FEL0, FEL1, FEL0_size+FEL1_size, curr_time)


tail_drop_simulation()
