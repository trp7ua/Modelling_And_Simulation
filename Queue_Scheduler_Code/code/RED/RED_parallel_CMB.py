import Queue, time
import random
import numpy as np
import threading

# this is a lock used for parallel implementations. Used in putting the barriers for execution, while sharing the variables
lock = threading.Lock()


def generate_req(n):
	l = [i for i in range(n)]
	a = l[random.randint(0,n-1)]
	l.pop(a)
	k= random.randint(0,n-2)
	b = l[k]
	return (a,b)

# generates the packet with some exponential distribution
def expo_rate(lmda):
	return random.expovariate(lmda)

# for randomly generating the serving rates
def generate_serving_rates(n):
	rates = []
	for i in range(n):
		#rates.append(int(10*random.random()))
		rates.append(random.random())
	return rates



# number of leaf nodes. That is total number of computers in the network
num_server = 5

# topology of the network. 0,1,2 number computers connected to router or node 1 while others at node 2
nodes = {0:0,1:0,2:0,\
			3:1,4:1}

# number of serving nodes/routers
num_nodes = 2

# for random generation of node throughpout. In current study they are fixed
node_throughput = [expo_rate(i) for i in generate_serving_rates(num_nodes)]


# for random generation of node throughpout. In current study they are fixed
node_throughput = [expo_rate(i) for i in generate_serving_rates(num_nodes)]
node_throughput = [0.456, 0.648]
print "node_throughput:", node_throughput

# Node queue length. The max capacity of the serving queues
node_queue_length = [10,10]


# total number of packets to be generated
num_requests = 20000
#simulation_time = 100
look_ahead_time = 0

# Packet arrival rate
lam=5000000;

# Some scalar multiplication of packet arrival rate at varies leaf nodes
arrival_rates =[1,2,3,2,4]
arrival_rates = [lam*i for i in arrival_rates]


# Not used
server_req_queue = []
for i in range(num_server):
	q = Queue.PriorityQueue()
	server_req_queue.append(q)


# Function to know all those packets which are supposed to leave in current iteration in the event based approach.
# Not used though
def count_less_time_stamps(l1, threshold):
	#l2 = [i for i in l1 if i > threshold]
	l2 = []
	ini_len = len(l1)
	for i in l1:
		if i > threshold:
			l2.append(i)
			l1.pop(l1.index(i))

	return (l2, l1, ini_len - len(l1))


# Few global varibales to be shared in parallel processing as shared varibales. leading to use of locks
serving_FEL0_length = []
serving_FEL1_length = []
packet_drop_count = 0
count_served = 0
prev_curr_time0 = 0
prev_curr_time1 = 0
curr_time = 0
prev_curr_time0 = 0
prev_curr_time1 = 0

# The actual event handler. The method which executes the event oriented simulation
def serving_tail_drop_nodes(FEL0, FEL1, FEL_NUM, prob):
	serve_count = 0
	

	serving_FEL0 = []
	serving_FEL1 = []
	
	global prev_curr_time0
	global prev_curr_time1
	global serving_FEL0_length
	global serving_FEL1_length

	global packet_drop_count
	global count_served

	global curr_time

	curr_time = 0
	#check logical process numeber: 0 or 1 i.e. 1 or 2:
	if FEL_NUM == 0:

		# termination condition
		while (not FEL0.empty()):
			if prev_curr_time0 < prev_curr_time1:
				if not (FEL0.empty()):
					service0 = FEL0.get()


				curr_time += service0[0]
				if (service0[3]):
			
					served_in_last_iter = int((curr_time- prev_curr_time0)*node_throughput[0])
				
					serving_FEL0.sort() # should always be served in the order of the timestamp in anycase

					for i in range(served_in_last_iter):
						if len(serving_FEL0):
							prev_curr_time0 = serving_FEL0[0]
						serving_FEL0 = serving_FEL0[1:]

					if (len(serving_FEL0) < 0.8*node_queue_length[0]):
						serving_FEL0.append(service0[0])
						serving_FEL0_length.append(len(serving_FEL0))
						count_served += 1

					else:

						temp_p = random.random()
						if (temp_p > prob):

							FEL0.put(serving_FEL0)
						else:
							packet_drop_count +=1
							serving_FEL0_length.append(node_queue_length[0])
						#print "yo"
					prev_curr_time0 = curr_time
				else:
					service0[0] += look_ahead_time
					service0[3] = 1
					FEL1.put(service0)

			else:
				# termination condition
				# parallely running other process as in CMB
				while not FEL1.empty():
					if not (FEL1.empty()):
						service1 = FEL1.get()

					curr_time += service1[0]
					if (service1[3]):

						served_in_last_iter = int((curr_time- prev_curr_time1)*node_throughput[1])
						serving_FEL1.sort() # should always be served in the order of the timestamp in anycase
						#print serving_FEL1
						for i in range(served_in_last_iter):
							if len(serving_FEL1):
								prev_curr_time1 = serving_FEL1[0]
							serving_FEL1 = serving_FEL1[1:]

						#serving_FEL1 = [i for i in serving_FEL1 if i > curr_time]

						if (len(serving_FEL1) < 0.8*node_queue_length[1]):
							serving_FEL1.append(service1[0])
							serving_FEL1_length.append(len(serving_FEL1))

							count_served +=1
						else:
							#packet_drop_count.append(len(serving_FEL1) - node_queue_length[1])
							temp_p = random.random()
							if (temp_p > prob):
								#if (len(serving_FEL1) < node_queue_length[1]):
								#	serving_FEL1.append(service1[0])
								#	serving_FEL1_length.append(len(serving_FEL1))
								#	count_served += 1
								FEL1.put(serving_FEL1)
							else:
								packet_drop_count +=1
								serving_FEL1_length.append(node_queue_length[1])
							#print "yo"
						prev_curr_time1 = curr_time
					else:
						service1[0] += look_ahead_time
						service1[3] = 1
						FEL0.put(service1)
			#print len(serving_FEL0)

	else:
		# termination condition
		while not FEL1.empty():
			if prev_curr_time1 < prev_curr_time0:
				if not (FEL1.empty()):
					service1 = FEL1.get()
				#FEL0.put(service0)
				curr_time += service1[0]
				if (service1[3]):
					#serving_FEL1, old_serving_FEL1, count_lesser = count_less_time_stamps(serving_FEL1, curr_time)
					served_in_last_iter = int((curr_time- prev_curr_time1)*node_throughput[1])
					serving_FEL1.sort() # should always be served in the order of the timestamp in anycase
					#print serving_FEL1
					for i in range(served_in_last_iter):
						if len(serving_FEL1):
							prev_curr_time1 = serving_FEL1[0]
						serving_FEL1 = serving_FEL1[1:]

					#serving_FEL1 = [i for i in serving_FEL1 if i > curr_time]

					if (len(serving_FEL1) < 0.8*node_queue_length[1]):
						serving_FEL1.append(service1[0])
						serving_FEL1_length.append(len(serving_FEL1))

						count_served +=1
					else:
						#packet_drop_count.append(len(serving_FEL1) - node_queue_length[1])
						temp_p = random.random()
						if (temp_p > prob):
							#if (len(serving_FEL1) < node_queue_length[1]):
							#	serving_FEL1.append(service1[0])
							#	serving_FEL1_length.append(len(serving_FEL1))
							#	count_served += 1
							FEL1.put(serving_FEL1)
						else:
							packet_drop_count +=1
							serving_FEL1_length.append(node_queue_length[1])
						#print "yo"
					prev_curr_time1 = curr_time
				else:
					service1[0] += look_ahead_time
					service1[3] = 1
					FEL0.put(service1)

			else:
				while not FEL0.empty():
					if not (FEL0.empty()):
						service0 = FEL0.get()

					#if (service0[0] <= service1[0]):
					#	FEL1.put(service1)
					curr_time += service0[0]
					if (service0[3]):
						#serving_FEL0, old_serving_FEL0, count_lesser = count_less_time_stamps(serving_FEL0, curr_time)
						#print curr_time, prev_curr_time0
						served_in_last_iter = int((curr_time- prev_curr_time0)*node_throughput[0])
						#print "served_in_last_iter", served_in_last_iter
						serving_FEL0.sort() # should always be served in the order of the timestamp in anycase
						#print served_in_last_iter
						#print "length of serving_FEL0: ",len(serving_FEL0), served_in_last_iter
						for i in range(served_in_last_iter):
							if len(serving_FEL0):
								prev_curr_time0 = serving_FEL0[0]
							serving_FEL0 = serving_FEL0[1:]

						#serving_FEL0 = [i for i in serving_FEL0 if i > curr_time]
						#print "length of serving_FEL0: ",len(serving_FEL0)

						if (len(serving_FEL0) < 0.8*node_queue_length[0]):
							serving_FEL0.append(service0[0])
							serving_FEL0_length.append(len(serving_FEL0))
							count_served += 1

						else:
							#print "==============", node_queue_length[0], len(serving_FEL0)
							#packet_drop_count.append(len(serving_FEL0) - node_queue_length[0])
							temp_p = random.random()
							if (temp_p > prob):
								#if (len(serving_FEL0) < node_queue_length[0]):
								#serving_FEL0.append(service0[0])
								#serving_FEL0_length.append(len(serving_FEL0))
								#count_served += 1
								FEL0.put(serving_FEL0)
							else:
								packet_drop_count +=1
								serving_FEL0_length.append(node_queue_length[0])
							#print "yo"
						prev_curr_time0 = curr_time
					else:
						service0[0] += look_ahead_time
						service0[3] = 1
						FEL1.put(service0)
				#print len(serving_FEL1)

	print (np.mean(serving_FEL0_length), np.mean(serving_FEL1_length),packet_drop_count, count_served)
	#return (np.mean(serving_FEL0_length), np.mean(serving_FEL1_length),packet_drop_count, count_served)


# The actual simulation: Generation of FEL	
def tail_drop_simulation(prob):
	FEL0 = Queue.PriorityQueue()
	FEL1 = Queue.PriorityQueue()
	FEL0_size = 0
	FEL1_size = 0
	count = 0
	curr_time = 0 # time varialble
	

	# while not the max number of packets are generated. Or FEL generations
	while count < num_requests:
		count += 1


		time_lists = []

		a, b = generate_req(num_server)
		temp_arrival_rate = arrival_rates[a]
		temp_time = expo_rate(temp_arrival_rate)
		curr_time_temp = curr_time + temp_time
		time_lists.append(curr_time_temp)

		
		if (nodes[a] == 0):

			if nodes[a] == nodes[b]:
				FEL0.put([curr_time_temp, a, b, 1]) # last value is for checking whether source and destination are on same node else 0
			else:
				FEL0.put([curr_time_temp, a, b, 0])
			FEL0_size += 1
		else:
			#if FEL1_size < node_queue_length[1]:
			if nodes[a] == nodes[b]:
				FEL1.put([curr_time_temp, a, b, 1]) # last value is for checking whether source and destination are on same node else 0
			else:
				FEL1.put([curr_time_temp, a, b, 0])
			FEL1_size += 1

		#curr_time = max(time_lists)
		curr_time = curr_time_temp
	

	# Logical Processes
	process1 = threading.Thread(target= serving_tail_drop_nodes, args = (FEL0, FEL1,0, prob,))
	process2 = threading.Thread(target= serving_tail_drop_nodes, args = (FEL0, FEL1,1,prob,))

	process1.start()
	process2.start()

	process1.join()
	process2.join()

prob = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
#prob = [0.7]
for p in prob:
	results = []

	for i in range(3):
		start = time.time()
		tail_drop_simulation(p)
		print "results above: avg queue length at node 0, vg queue length at node 1, #packets dropped, #packets served"
		end = time.time()
		print "total time: ", end-start
		#results.append(list(tail_drop_simulation(p)))
		serving_FEL0_length = []
		serving_FEL1_length = []
		packet_drop_count = 0
		count_served = 0
		curr_time = 0
		prev_curr_time0 = 0
		prev_curr_time1 = 0
	#results = zip(*results)
	#print [np.mean(i) for i in results]
