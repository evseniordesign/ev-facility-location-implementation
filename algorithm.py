"""
Runs the uncapacitated facility loaction problem solution.
Calls the LP solver and uses the result to create and approximation of optimal.
"""

from sys import maxint
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
    lowest_fac = Facility(-1, maxint, 0)
    for facility in facilities:
        if client.is_member(facility.index, baseline) and facility.open_cost < lowest_fac.open_cost:
            lowest_fac = facility
    return lowest_fac

def get_adjacent_clients(orig_client, facilities, baseline):
    """
    Get clients adjacent to facilities of a given client.
    Includes the given client.
    """
    adj_facilities = orig_client.get_facility_list(facilities, baseline)
    return reduce(lambda acc, facility: acc | facility.memberships, adj_facilities, set())

def facility_location_solve(facility_costs, client_costs):
    primal, dual = solve_lp(facility_costs, client_costs)
    return deterministic_rounding(facility_costs, client_costs, primal, dual)

def deterministic_rounding(facility_costs, client_costs, primal, dual):
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

    # TODO check if baseline makes any sense
    # if decision variable is less than baseline, treat it as 0
    num_facilities = len(facility_costs)
    baseline = 1.0 / (2 * num_facilities)
    assignments = dict()

    # sorts clients by dual solution to reduce time complexity d
    clients = sortedset.SortedSet([
        Client(client_costs[i], i,
               primal[(i+1)*num_facilities:(i+2)*num_facilities],
               dual[i])
        for i in xrange(0, len(client_costs))], 
        key=lambda c : c.lowest_pair_cost)

    facilities = [Facility(i, facility_costs[i], primal[i])
                  for i in xrange(0, num_facilities)]

    for facility in facilities:
        facility.memberships = set([client for client in clients
                                    if client.is_member(facility.index, baseline)])

    while clients:
        # choose minimum client
        client = clients.pop(0)

        # cheapest facility for this client
        cheapest_f = get_cheapest_neighbor(client, facilities, baseline)

        # assign min client, and all unassigned clients
        # that neighbor neighboring facilities (N^2) of min client to cheap facility
        neighboring_clients = get_adjacent_clients(client, facilities, baseline)

        if cheapest_f not in assignments:
            assignments[cheapest_f] = set()

        assignments[cheapest_f] |= neighboring_clients

        # remove client, N^2(client)
        clients -= neighboring_clients

    return assignments
