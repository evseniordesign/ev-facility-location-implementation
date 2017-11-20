"""
Runs the uncapacitated facility loaction problem solution.
Calls the LP solver and uses the result to create and approximation of optimal.
"""

import random
import lp
from sortedcontainers import sortedset
from utils import Client, Facility

def solve_lp(facility_costs, client_costs):
    """
    Adjust args and pass arrays into LP solver.
    """
    flat_ccosts = reduce(lambda acc, curr: acc + curr, client_costs)
    sol = lp.solve(facility_costs, flat_ccosts)
    return sol['x'], sol['y']

def get_cheapest_neighbor(client, facilities, baseline):
    """
    Return neighbor's client that has the lowest cost.
    """
    adj_facilities = client.get_facility_list(facilities, baseline)
    return min(adj_facilities, key=lambda fac: fac.open_cost)

def get_probably_good_neighbor(client, facilities, baseline):
    """
    Return random facility with probability decided by decision vars
    """
    total_real_membership = sum([client.facility_memberships[facility.index]
                                 for facility in facilities
                                 if client.is_member(facility.index, baseline)])
    number = random.uniform(0, total_real_membership)
    for facility in facilities:
        if client.is_member(facility.index, baseline):
            number -= client.facility_memberships[facility.index]
            if number < 0:
                return facility
    return None

def get_adjacent_clients(orig_client, clients, facilities, baseline):
    """
    Get clients adjacent to facilities of a given client.
    Includes the given client.
    """
    adj_clients = set()
    adj_clients.add(orig_client)

    adj_facilities = orig_client.get_facility_list(facilities, baseline)
    for client in clients:
        for facility in adj_facilities:
            if client.is_member(facility.index, baseline):
                adj_clients.add(client)
                break

    return adj_clients

def rounding(facility_costs, client_costs, is_deterministic):
    """
    Solve LP, get optimal primal (x*, y*) and dual (v*, w*)
    C <- D
    K <- 0
    while C != 0 do
        choose jk in C that minimizes vj* for all j in C
        choose ik in N(jk) that is the cheapest facility
        assign jk and all of N^2(jk) to ik
        C <- C - {jk} - N^2(jk)
    """

    primal, dual = solve_lp(facility_costs, client_costs)

    # TODO check if baseline makes any sense
    # if decision variable is less than baseline, treat it as 0
    num_facilities = len(facility_costs)
    baseline = 1.0 / (2 * num_facilities)
    assignments = dict()

    if is_deterministic:
        facility_chooser = get_cheapest_neighbor
        client_chooser = lambda client: client.lowest_pair_cost
    else:
        facility_chooser = get_probably_good_neighbor
        client_chooser = lambda client: client.lowest_pair_cost + client.get_expected_cost(baseline)

    # sorts clients by dual solution to reduce time complexity d
    clients = sortedset.SortedSet([
        Client(client_costs[i], i,
               primal[(i+1)*num_facilities:(i+2)*num_facilities],
               dual[i])
        for i in xrange(0, len(client_costs))], key=client_chooser)

    facilities = [Facility(i, facility_costs[i], primal[i])
                  for i in xrange(0, num_facilities)]

    while clients:
        # choose minimum client
        client = clients.pop(0)

        # best facility for this client
        facility = facility_chooser(client, facilities, baseline)

        # assign min client, and all unassigned clients
        # that neighbor neighboring facilities (N^2) of min client to best facility
        neighboring_clients = get_adjacent_clients(client, clients, facilities, baseline)

        if facility not in assignments:
            assignments[facility] = set()

        assignments[facility] |= neighboring_clients

        # remove client, N^2(client)
        clients -= neighboring_clients

    return assignments

def deterministic_rounding(facility_costs, client_costs):
    """
    Call the algorithm's deterministic version.
    """
    return rounding(facility_costs, client_costs, True)

def randomized_rounding(facility_costs, client_costs):
    """
    Call the algorithm's randomized version.
    """
    return rounding(facility_costs, client_costs, False)
