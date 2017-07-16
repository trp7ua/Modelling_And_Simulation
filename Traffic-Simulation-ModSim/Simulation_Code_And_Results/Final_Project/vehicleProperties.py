import random


# Vehicle velocity distribution in feet per second
def vehicle_mu():
	vehicle_mu = 23
	return vehicle_mu

def vehicle_sigma():
	vehicle_sigma = 3#random.randint(2,3) # actually this va
	return vehicle_sigma


# vehicle length in feet
def vehicle_length_mu():
	vehicle_length_mu = 16
	return vehicle_length_mu

def vehicle_length_sigma():
	vehicle_length_sigma = 1
	return vehicle_length_sigma

def offset_between_vehicles():
	offset_between_vehicles = 10
	return offset_between_vehicles


