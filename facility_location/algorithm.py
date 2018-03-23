"""
Runs the uncapacitated facility location solution.
Calls the LP solver and uses the result to create and approximation of optimal.
"""

import random
from collections import defaultdict
from enum import Enum
import facility_location.lp as lp
from facility_location.utils import Client, Facility
from sortedcontainers.sortedset import SortedSet

def solve_lp(facilities, clients):
    """
    Adjust args and pass arrays into LP solver.
    Return primal and dual solutions.
    """
    facility_costs = [facility['cost'] for facility in facilities]
    client_costs = [client['costs'] for client in clients]

    flat_ccosts = reduce(lambda acc, curr: acc + curr, client_costs)
    sol = lp.solve(facility_costs, flat_ccosts)
    primal = sol['x']
    dual = sol['y']

    return primal, dual

def init_clients(clients, primal, dual):
    """
    Return list of clients with LP information.
    """
    num_facilities = len(clients[0]['costs'])

    return [Client(i,
                   primal[(i + 1) * num_facilities : (i + 2) * num_facilities],
                   dual[i],
                   clientprops)
            for i, clientprops in enumerate(clients)]

def init_facilities(facilities, primal):
    """
    Return list of facilities with LP information.
    """
    return [Facility(i, primal[i], facilities[i])
            for i in xrange(len(facilities))]

def get_cheapest_neighbor(client, facilities):
    """
    Return neighbor's client that has the lowest cost.
    """
    adj_facilities = client.get_facility_list(facilities)
    return min(adj_facilities, key=lambda fac: fac['cost'])

def get_probably_good_neighbor(client, facilities):
    """
    Return random facility with probability decided by decision vars
    """
    total_real_membership = sum(client.facility_memberships[facility.index]
                                for facility in facilities
                                if client.is_member(facility.index))

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
    assignments = defaultdict(set)

    # sorts clients by dual solution to reduce time complexity
    clients = SortedSet(clients, key=client_chooser)

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

def choose_facilities(facilities, clients, algorithm='randomized'):
    """
    Run the LP solver and given algorithm to output a solution.
    The solution format is a dictionary with the keys being facilities
    and values being a set of clients.
    """
    primal, dual = solve_lp(facilities, clients)
    facilities = init_facilities(facilities, primal)
    clients = init_clients(clients, primal, dual)

    if algorithm == 'randomized':
        client_chooser = lambda client: client.lowest_pair_cost + client.get_expected_cost()
        facility_chooser = get_cheapest_neighbor
        return rounding_algorithm(facilities, clients, client_chooser, facility_chooser)
    elif algorithm == 'deterministic':
        client_chooser = lambda client: client.lowest_pair_cost
        facility_chooser = get_probably_good_neighbor
        return rounding_algorithm(facilities, clients, client_chooser, facility_chooser)
    else:
        return None
