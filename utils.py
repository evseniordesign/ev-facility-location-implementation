"""
Utility classes:

Client:
list of cij costs (array where index = facility)
list of xij decision variables from primal
vj from dual
index

Facility:
opening cost
yij decision variable from primal
"""

class Client:
	c_costs = None
	facility_memberships = None
	lowest_pair_cost = None  # dual solution
	index = -1

	def __init__(self, cij_costs, i, primal, dual):
		self.c_costs = cij_costs
		self.index = i
		self.facility_memberships = primal
		self.lowest_pair_cost = dual

	def __hash__(self):
		return hash(self.index)

	def __str__(self):
		return "Client index: %d" % self.index

	def __repr__(self):
		return self.__str__()

	def is_member(self, fac_index, baseline):
		return self.facility_memberships[fac_index] >= baseline

	def get_facility_list(self, facilities, baseline):
		return [f for f in facilities if self.is_member(f.index, baseline)]

	@staticmethod
	def get_client_list(c_costs):
		"""Input a 2D list of costs

		Each row represents a client's costs.
		Output a list of client objects.
		"""
		output = []
		for x in range(len(c_costs)):
			output.append(Client(c_costs[x], x))
		return output

class Facility:
	index = -1
	open_cost = None
	open_decision = None

	def __init__(self, index, f_cost, primal):
		self.index = index
		self.open_cost = f_cost
		self.open_decision = primal

	def __hash__(self):
		return hash(self.index)

	def __str__(self):
		return "Facility index: %d" % self.index 

	def __repr__(self):
		return self.__str__()
