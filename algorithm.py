"""
Runs the uncapacitated facility loaction problem solution.
Calls the LP solver and uses the result to create and approximation of optimal.
"""

import lp, sys
from sortedcontainers import sortedset
from utils import Client, Facility

def solve_lp(facility_costs, client_costs):
    """
    Adjust args and pass arrays into LP solver.
    """
    flat_ccosts = reduce((lambda acc, curr: acc + curr), client_costs)
    sol = lp.solve(facility_costs, flat_ccosts)
    return sol['x'], sol['y']

def get_cheapest_neighbor(client, facilities, baseline):
    lowest_fac = Facility(-1, sys.maxint, 0)
    for f in facilities:
        if client.is_member(f.index, baseline) and f.open_cost < lowest_fac.open_cost:
            lowest_fac = f
    return lowest_fac

def is_adjacent(single_client_vars, facilities, baseline):
    """
    Check if the given client is adjacent to any of the facilities.
    """
    for facility in facilities:
        if single_client_vars[facility] > baseline:
            return True

    return False

def get_adjacent_clients(orig_client, clients, facilities, baseline):
    """
    Get clients adjacent to facilities of a given client.
    Includes the given client.
    """
    adj_clients = set()
    adj_facilities = orig_client.get_facility_list(facilities, baseline)
    for client in clients:
        for f in adj_facilities:
            if client.is_member(f.index, baseline):
                adj_clients.add(client)
    return adj_clients


def get_min(clients):
    """
    Get min vj* from the dual LP.
    """
    return clients.pop(0)

def facility_location_solve(facility_costs, client_costs):
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
    num_clients = len(client_costs)
    baseline = 1.0 / (2 * num_facilities)

    #clients = set(xrange(0, len(client_costs)))
    clients = sortedset.SortedSet([Client(client_costs[i], i, primal[(i+1)*num_facilities:(i+2)*num_facilities], dual[i])
                for i in xrange(0, num_clients)])
    facilities = [Facility(i, facility_costs[i], primal[i])
                    for i in xrange(0, num_facilities)]
    assignments = dict()

    while clients:
        # choose jk
        client = get_min(clients)

        # cheapest facility for this client
        cheapest_f = get_cheapest_neighbor(client, facilities, baseline)

        # assign jk, N^2(jk) to ik
        neighboring_clients = get_adjacent_clients(
            client,
            clients,
            facilities,
            baseline)

        if not cheapest_f in assignments:
            assignments[cheapest_f] = set()

        assignments[cheapest_f] |= neighboring_clients
        assignments[cheapest_f].add(client)

        # remove jk, N^2(jk)
        clients.difference_update(neighboring_clients)

    return assignments
