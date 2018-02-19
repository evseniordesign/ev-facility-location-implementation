# helpers.py
# contains helper functions for various classes

from math import sin, cos, sqrt, atan2, radians

def distance(lat1, long1, lat2, long2):
	"""
	Input two arrays of lat and long coordinates
	Return the straight line distance between them
	using the Haversine formula
	"""
	R = 6373.0

	dlon = radians(long2 - long1)
	dlat = radians(lat2 - lat1)

	a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance