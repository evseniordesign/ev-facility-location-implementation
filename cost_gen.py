import pandas as pd 
from flgraph import fgraph as fg
from math import sin, cos, sqrt, atan2

SERVICE_RADIUS = 4

class CostGenerator:
	c_data = None
	f_data = None

	graph = None

	def __init__(self, fn_c, fn_f):
		self.c_data = pd.read_csv(fn_c, names=['TRACTCE', 'POPULATION', 'LATITUDE', 'LONGITUDE'])
		self.f_data = pd.read_csv(fn_f, names=['FACILITY', 'LAT', 'LONG'])

		self.graph = fg()
		self.graph.f_len = self.f_data.count()
		self.graph.c_len = self.c_data.count()
		self.generate_fcosts()
		self.generate_ccosts()

	def get_fgraph(self):
		return graph

	def generate_fcosts(self):
		self.graph._fcosts = []
		for f_index, f_row in self.f_data.iterrows():
			population = 0
			for c_index, c_row in self.c_data.iterrows():
				lat1 = f_row['LAT']
				long1 = f_row['LONG']
				lat2 = c_row['LATITUDE']
				long2 = c_row['LONGITUDE']

				distance = getDistance(lat1, long1, lat2, long2)
				if(abs(distance) <= SERVICE_RADIUS):
					population = population + c_row['POPULATION']
			self.graph._fcosts.append(self.fcost_func(population))


	def fcost_func(self, population):
		#TO DO


	def generate_ccosts(self):
		self.graph._ccosts = []
		for c_index, c_row in self.c_data.iterrows():
			ccosts = []
			for f_index, f_row in self.f_data.iterrows():
				lat1 = f_row['LAT']
				long1 = f_row['LONG']
				lat2 = c_row['LATITUDE']
				long2 = c_row['LONGITUDE']

				distance = getDistance(lat1, long1, lat2, long2)
				ccosts.append(distance)
			self.graph._ccosts.append(ccosts)


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

