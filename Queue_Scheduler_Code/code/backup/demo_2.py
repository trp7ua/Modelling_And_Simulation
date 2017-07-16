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

def expo_rate(lmda):
	return random.expovariate(lmda)

def generate_serving_rates(n):
	rates = []
	for i in range(n):
		#rates.append(int(10*random.random()))
		rates.append(random.random())
	return rates



num_server = 5
nodes = {0:0,1:0,2:0,\
			3:1,4:1}

num_nodes = 2
node_throughput = [expo_rate(i) for i in generate_serving_rates(num_nodes)]
print "node_throughput:", node_throughput
#node_throughput = [15,20]
node_throughput = [0.45613688284373793, 0.6487844048981645]
node_queue_length = [2,2]


num_requests = 20000
simulation_time = 100
look_ahead_time = 0
#server_rates = generate_serving_rates(num_server)
#arrival_rates = generate_serving_rates(num_server)
lam=5000000000000000000;
arrival_rates =[1,2,3,2,4]
arrival_rates = [lam*i for i in arrival_rates]


server_req_queue = []
for i in range(num_server):
	q = Queue.PriorityQueue()
	server_req_queue.append(q)


def count_less_time_stamps(l1, threshold):
	#l2 = [i for i in l1 if i > threshold]
	l2 = []
	ini_len = len(l1)
	for i in l1:
		if i > threshold:
			#print i
			#print l2
			l2.append(i)
			l1.pop(l1.index(i))

	return (l2, l1, ini_len - len(l1))

def serving_tail_drop_nodes(FEL0, FEL1, num, final_time):
	serve_count = 0
	

	serving_FEL0 = []
	serving_FEL1 = []
	prev_curr_time0 = 0
	prev_curr_time1 = 0
	serving_FEL0_length = []
	serving_FEL1_length = []

	packet_drop_count = 0
	count_served = 0

	curr_time = 0
	#while (curr_time < final_time):
	while (not FEL0.empty() and not FEL1.empty()):
		if not (FEL0.empty()):
			service0 = FEL0.get()
		if not (FEL1.empty()):
			service1 = FEL1.get()

		if (service0[0] <= service1[0]):
			FEL1.put(service1)
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
					serving_FEL0 = serving_FEL0[1:]
				#print "length of serving_FEL0: ",len(serving_FEL0)
				if (len(serving_FEL0) < node_queue_length[0]):
					serving_FEL0.append(service0[0])
					serving_FEL0_length.append(len(serving_FEL0))
					count_served += 1

				else:
					#print "==============", node_queue_length[0], len(serving_FEL0)
					#packet_drop_count.append(len(serving_FEL0) - node_queue_length[0])
					packet_drop_count +=1
					serving_FEL0_length.append(node_queue_length[0])
					#print "yo"
				prev_curr_time0 = curr_time
			else:
				service0[0] += look_ahead_time
				service0[3] = 1
				FEL1.put(service0)

			#print len(serving_FEL0)

		else:

			FEL0.put(service0)
			curr_time += service1[0]
			if (service1[3]):
				#serving_FEL1, old_serving_FEL1, count_lesser = count_less_time_stamps(serving_FEL1, curr_time)
				served_in_last_iter = int((curr_time- prev_curr_time1)*node_throughput[1])
				serving_FEL1.sort() # should always be served in the order of the timestamp in anycase
				#print serving_FEL1
				for i in range(served_in_last_iter):
					serving_FEL1 = serving_FEL1[1:]

				if (len(serving_FEL1) < node_queue_length[1]):
					serving_FEL1.append(service1[0])
					serving_FEL1_length.append(len(serving_FEL1))

					count_served +=1
				else:
					#packet_drop_count.append(len(serving_FEL1) - node_queue_length[1])
					packet_drop_count +=1
					serving_FEL1_length.append(node_queue_length[1])
					#print "yo"
				prev_curr_time1 = curr_time
			else:
				service1[0] += look_ahead_time
				service1[3] = 1
				FEL0.put(service1)

			#print len(serving_FEL1)


	return (np.mean(serving_FEL0_length), np.mean(serving_FEL1_length),packet_drop_count, count_served)

			
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

		#curr_time += temp_time
		time_lists = []
		#for i in range(500):
		a, b = generate_req(num_server)
		temp_arrival_rate = arrival_rates[a]
		temp_time = expo_rate(temp_arrival_rate)
		curr_time_temp = curr_time + temp_time
		time_lists.append(curr_time_temp)
		#temp_time = expo_rate(random.random())
		#print temp_time
		#curr_time += temp_time
		
		if (nodes[a] == 0):
			#if FEL0_size < node_queue_length[0]:
			# we can also accept/reject with some probability here instead of taildrop later
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
	
	print serving_tail_drop_nodes(FEL0, FEL1, FEL0_size+FEL1_size, curr_time)
	print "FEL sizes: ", FEL0_size, FEL1_size
	print curr_time
	#print "arrival_rates", arrival_rates


tail_drop_simulation()
