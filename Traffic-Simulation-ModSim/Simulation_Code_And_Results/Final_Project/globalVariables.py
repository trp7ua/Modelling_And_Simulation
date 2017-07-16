# For tracking the Signals at all the intersections. Not being used now. 
import random

def signalStateList():
	signalStateList = []
	for i in range(4):
		state = True
		t = 0	
		signalStateList.append((state, t))
	return signalStateList

# Segment lengths assumed for now in feet
# currently not considering the segments at end
def segment_length_list():
	segment_length_list = [442, 412, 354, 344]
	return segment_length_list

# Obtained from NGSIM data
def vehicle_arrival_rate():
	returnvehicle_arrival_rate = [0.60 ,0.08, 0.04, 0.04, 0.04, 0.06, 0.70]
	return returnvehicle_arrival_rate

#assumed same at a given junction from sides or from beggining or end: Order: 1st main, 1st sides, 2nd sides, 3rd sides, 4th sides, 5th main, 5th sides
# main twos: North at index 0 and last index or main from South

# turning rate for each queue from 0 to 9.
# given rates for each queue based on data:
	# q0: 0.5 q9: 0.5, q1: 0.15  q8: 0.02, q2: 0.05 q7: 0.05 , q3:0.2 q6: 0.05 , q4: 0.45 q5: 0.5
def turning_rate():
	turning_rate = [0.5,0.02,0.05,0.05,0.5, 0.45,0.2,0.05,0.15,0.5]
	return turning_rate

# Cycle timings assumed to be: 40 = Green + Yellow, 60: Red
def cycle_timing_list():
	cycle_timing_list = [40, 60]
	return cycle_timing_list

def total_cyle_length():
	total_cyle_length = sum(cycle_timing_list())
	return total_cyle_length

def signal_offset():
	signal_offset = random.randint(4,15)
	return signal_offset
