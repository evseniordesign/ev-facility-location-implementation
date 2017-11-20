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

class Client(object):
    """
    Representation of a client from LP output.
    """
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
        return str(self)

    def is_member(self, fac_index, baseline):
        """
        Check if self is a member of facility number fac_index.
        """
        return self.facility_memberships[fac_index] >= baseline

    def get_facility_list(self, facilities, baseline):
        """
        Return a list of facilities that self is a member of.
        """
        return [f for f in facilities if self.is_member(f.index, baseline)]

    def get_expected_cost(self, baseline):
        """
        Return expected cost of assigning self to a neighbor
        """
        acc = 0
        for facility_number in xrange(len(self.c_costs)):
            if self.is_member(facility_number, baseline):
                acc += self.c_costs[facility_number] * self.facility_memberships[facility_number]
        return acc

class Facility(object):
    """
    Representation of a client from LP output.
    """
    index = -1
    open_cost = None
    open_decision = None
    memberships = None

    def __init__(self, index, f_cost, primal):
        self.index = index
        self.open_cost = f_cost
        self.open_decision = primal

    def __hash__(self):
        return hash(self.index)

    def __str__(self):
        return "Facility index: %d" % self.index

    def __repr__(self):
        return str(self)
