"""
This module contains the user interface class to interact with the LP solution.
"""

import algorithm

class Fgraph(object):
    """
    This class acts as a user interface for the program.

    It solves the LP and then provides and interface to work with the solution.
    """
    num_facilities = None
    num_clients = None
    _fcosts = None
    _ccosts = None
    _sol = None

    def __init__(self, facility_costs, client_costs):
        """
        Initializes the graph.
        facility_costs is a list of costs for a given facility, and client_costs
        is a 2d list of client costs for being associated with a given facility.
        Set up like client_costs[client_num][facility_num].
        """

        self.num_facilities = len(facility_costs)
        self.num_clients = len(client_costs)
        self._fcosts = facility_costs
        self._ccosts = client_costs

        for client in client_costs:
            assert self.num_facilities == len(client)


        self._sol = algorithm.facility_location_solve(facility_costs, client_costs)

    @classmethod
    def from_file(cls, filename):
        """
        Initializes the graph from the given file.
        """
        infofile = open(filename)
        lengths = infofile.readline().split()
        num_facilities = int(lengths[0])
        num_clients = int(lengths[1])

        fcosts = map(float, infofile.readline().split())
        ccosts = None

        try:
            for _ in xrange(0, num_clients):
                client = map(float, infofile.readline().split())
                if ccosts is None:
                    ccosts = [client]
                else:
                    ccosts.append(client)
                if len(client) != num_facilities:
                    raise ValueError()
        except ValueError:
            print "_fcosts and _ccosts must contain f_len values."
            exit(1)

        infofile.close()
        return cls(fcosts, ccosts)

    def is_open(self, facility_num):
        """
        Returns true if the given facility should be opened.
        """
        pass

    def is_assigned_to(self, client_num):
        """
        Returns the facility number of the facility the client is assigned to.
        """
        pass

    def get_assigned_clients(self, facility_num):
        """
        Returns a list of clients that were assigned to the given facility.
        """
        pass

    def get_facility_cost(self, facility_num):
        """
        Returns the cost associated with opening a given facility.
        """
        return self._ccosts[facility_num]
