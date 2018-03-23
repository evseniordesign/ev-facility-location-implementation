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

    def __init__(self, i, primal, dual, props):
        self.index = i
        self.facility_memberships = primal
        self.lowest_pair_cost = dual
        self.props = props
        self.baseline = Client.get_baseline(self.facility_memberships)

    def __hash__(self):
        return hash(self.index)

    def __str__(self):
        return "Client index: %d" % self.index

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self.props[key]

    def __contains__(self, key):
        return key in self.props

    def __setitem__(self, key, item):
        self.props[key] = item

    @staticmethod
    def get_baseline(memberships):
        """
        Return baseline to be used with given memberships.
        """
        sorted_memberships = sorted(memberships, reverse=True)
        acc = 0
        for index, decision_var in enumerate(sorted_memberships):
            if acc < (1 - 1e-7): # acceptable error
                acc += decision_var
            else:
                # baseline in between used and unused values
                return (sorted_memberships[index - 1] + sorted_memberships[index]) / 2

        return 0

    def is_member(self, fac_index):
        """
        Check if self is a member of facility number fac_index.
        """
        return self.facility_memberships[fac_index] >= self.baseline

    def get_facility_list(self, facilities):
        """
        Return a list of facilities that self is a member of.
        """
        return [f for f in facilities if self.is_member(f.index)]

    def get_expected_cost(self):
        """
        Return expected cost of assigning self to a neighbor
        """
        return sum(
            self['costs'][facility_num] * self.facility_memberships[facility_num]
            for facility_num in xrange(len(self['costs']))
            if self.is_member(facility_num)
        )

class Facility(object):
    """
    Representation of a facility from LP output.
    """

    def __init__(self, index, primal, props):
        self.index = index
        self.open_decision = primal
        self.props = props

    def __hash__(self):
        return hash(self.index)

    def __str__(self):
        return "Facility index: %d" % self.index

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self.props[key]

    def __contains__(self, key):
        return key in self.props

    def __setitem__(self, key, item):
        self.props[key] = item
