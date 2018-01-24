"""
Runs the uncapacitated facility location solution.
Calls the LP solver and uses the result to create and approximation of optimal.
"""

import random
import lp
from sortedcontainers import sortedset
from utils import Client, Facility
from enum import Enum

class Algorithms(Enum):
    RAND = 1
    DET = 2


def solve_lp(facility_costs, client_costs):
    """
    Adjust args and pass arrays into LP solver. 
    Return primal and dual solutions.
    """
    flat_ccosts = reduce(lambda acc, curr: acc + curr, client_costs)
    sol = lp.solve(facility_costs, flat_ccosts)
    primal = sol['x']
    dual = sol['y']

    return primal, dual

def init_clients(client_costs, primal, dual, num_facilities):
    """
    Return list of clients with LP information.
    """
    return [Client(client_costs[i], i,
               primal[(i+1)*num_facilities:(i+2)*num_facilities],
               dual[i])
        for i in xrange(0, len(client_costs))]

def init_facilities(facility_costs, primal):
    """
    Return list of facilities with LP information.
    """
    num_facilities = len(facility_costs)
    return [Facility(i, facility_costs[i], primal[i])
                  for i in xrange(0, num_facilities)]

def get_cheapest_neighbor(client, facilities):
    """
    Return neighbor's client that has the lowest cost.
    """
    adj_facilities = client.get_facility_list(facilities)
    return min(adj_facilities, key=lambda fac: fac.open_cost)

def get_probably_good_neighbor(client, facilities):
    """
    Return random facility with probability decided by decision vars
    """
    total_real_membership = sum([client.facility_memberships[facility.index]
                                 for facility in facilities
                                 if client.is_member(facility.index)])
    number = random.uniform(0, total_real_membership)
    for facility in facilities:
        if client.is_member(facility.index):
            number -= client.facility_memberships[facility.index]
            if number < 0:
                return facility
    return None

def get_adjacent_clients(orig_client, clients, facilities):
    """
    Get clients adjacent to facilities of a given client.
    Includes the given client.
    """
    adj_clients = set()
    adj_clients.add(orig_client)

    adj_facilities = orig_client.get_facility_list(facilities)
    for client in clients:
        for facility in adj_facilities:
            if client.is_member(facility.index):
                adj_clients.add(client)
                break

    return adj_clients

def rounding_algorithm(facilities, clients, client_chooser, facility_chooser):
    """
    Run deterministic or randomized rounding algorithm to determine
    facility location costs.
    """
    assignments = dict()

    # sorts clients by dual solution to reduce time complexity
    clients = sortedset.SortedSet(clients, key=client_chooser)

    while clients:
        # choose minimum client
        client = clients.pop(0)

        # best facility for this client
        facility = facility_chooser(client, facilities)

        # assign min client, and all unassigned clients
        # that neighbor neighboring facilities (N^2) of min client to best facility
        neighboring_clients = get_adjacent_clients(client, clients, facilities)

        if facility not in assignments:
            assignments[facility] = set()

        assignments[facility] |= neighboring_clients

        # remove client, N^2(client)
        clients -= neighboring_clients

    return assignments

def choose_facilities(facility_costs, client_costs, algorithm=Algorithms.RAND):
    """
    Run the LP solver and given algorithm to output a solution.
    The solution format is a dictionary with the keys being facilities
    and values being a set of clients.
    """
    primal, dual = solve_lp(facility_costs, client_costs)
    facilities = init_facilities(facility_costs, primal)
    clients = init_clients(client_costs, primal, dual, len(facilities))

    if algorithm == Algorithms.RAND:
        client_chooser = lambda client: client.lowest_pair_cost + client.get_expected_cost()
        facility_chooser = get_cheapest_neighbor
        return rounding_algorithm(facilities, clients, client_chooser, facility_chooser)
    elif algorithm == Algorithms.DET:
        client_chooser = lambda client: client.lowest_pair_cost
        facility_chooser = get_probably_good_neighbor
        return rounding_algorithm(facilities, clients, client_chooser, facility_chooser)
    else:
        return None
