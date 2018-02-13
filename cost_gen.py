import pandas as pd 
from math import sin, cos, sqrt, atan2, radians

C_SCHEMA = ['lat', 'long']
F_SCHEMA = ['lat', 'long']

SERVICE_RADIUS = 4
FAC_COST = 5

def get_fcost(facility):
	"""
	Facility cost function. Currently has a fixed cost
	value based on FAC_COST above.
	"""
	return FAC_COST
	
	"""
	This code used population instead of a fixed facility
	cost value. Leaving this here in case we want to use 
	population or any other parameter in facility cost values.
	"""
	#self.graph._fcosts = []

	# for f_index, f_row in self.f_data.iterrows():
	# 	population = 0
	# 	for c_index, c_row in self.c_data.iterrows():
	# 		lat1 = f_row['LAT']
	# 		long1 = f_row['LONG']
	# 		lat2 = c_row['LATITUDE']
	# 		long2 = c_row['LONGITUDE']

	# 		distance = getDistance(lat1, long1, lat2, long2)
	# 		if(abs(distance) <= SERVICE_RADIUS):
	# 			population = population + c_row['POPULATION']
	# 	self.graph._fcosts.append(self.fcost_func(population))


# Artifact of the above commented out code.

# def fcost_func(self, population):
# 	#TO DO


def get_ccost(client, facility):
	"""
	Function to calculate client cost. 
	Currently is the distance from client to facility.
	"""
	
	lat1 = facility['lat']
	long1 = facility['long']
	lat2 = client['lat']
	long2 = client['long']

	distance = getDistance(lat1, long1, lat2, long2)
	return distance



def getDistance(lat1, long1, lat2, long2):
	R = 6373.0

	lat1 = radians(lat1)
	lon1 = radians(long1)
	lat2 = radians(lat2)
	lon2 = radians(long2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance

