import numpy as np 
from cvxopt import matrix
import flgraph as fg 

class neighborhood:
	n_mat = None

	def __init__(self, fgraph, weights):
		self.n_mat = np.empty([fgraph.c_len, fgraph.f_len], int)
		for i in xrange(0,fgraph.c_len):
			for j in xrange(0,fgraph.f_len):
				if round(weights[fgraph.f_len + i*fgraph.f_len + j], 2) == 0.00:
					self.n_mat[i][j] = 0
				else:
					self.n_mat[i][j] = 1

	def getNeighbors(self, client):
		return np.nonzero(self.n_mat[client])[0]

	def getN2(self, client):
		print "Get n2 neighborhood"

	def getFacilityNeighbors(self, facility):
		n_mat_tp = np.transpose(self.n_mat)
		return np.nonzero(n_mat_tp[facility])[0]

	def getCheapestFacility(self, client):
		print "return cheapest facility here"
