"""
Runs the uncapacitated facility loaction problem solution.
Calls the LP solver and uses the result to create and approximation of optimal.
"""

import lp

def solve_lp(facility_costs, client_costs):
    """
    Adjust args and pass arrays into LP solver.
    """
    flat_ccosts = reduce((lambda acc, curr: acc + curr), client_costs)
    sol = lp.solve(facility_costs, flat_ccosts)
    return sol['x'], sol['z']

def is_adjacent(single_client_vars, facilities, baseline):
    """
    Check if the given client is adjacent to any of the facilities.
    """
    for facility in facilities:
        if single_client_vars[facility] > baseline:
            return True

    return False

def get_adjacent_facilities(facility_vars, client_vars, client, baseline):
    """
    Get adjacent facilities of a given client.
    """
    num_facilities = len(facility_vars)
    return [facility for facility in xrange(0, num_facilities)
            if client_vars[client][facility] > baseline]

def get_adjacent_clients(facility_vars, client_vars, client, baseline):
    """
    Get clients adjacent to facilities of a given client.
    """
    num_clients = len(client_vars)
    facilities = get_adjacent_facilities(facility_vars, client_vars, client, baseline)
    return [client for client in xrange(0, num_clients)
            if is_adjacent(client_vars[client], facilities, baseline)]

def get_min(dual):
    """
    Get min vj* from the dual LP.
    """
    # TODO how do this
    return 0

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
    baseline = 1.0 / (2 * num_facilities)

    clients = set(xrange(0, len(client_costs)))
    facilities = dict()

    # Organize LP into facility vars and 2D array of client vars
    facility_decision_vars = primal[:num_facilities]
    client_decision_vars = [primal[i:i+num_facilities]
                            for i in xrange(num_facilities, len(primal), num_facilities)]

    get_min_cost = lambda acc, curr: acc if facility_costs[acc] < facility_costs[curr] else curr

    while clients != set():
        # choose jk
        client = get_min(dual)

        # choose ik
        # start acc at 2 so that all facility values are less than starting acc
        facility = reduce(get_min_cost,
                          get_adjacent_facilities(
                              facility_decision_vars,
                              client_decision_vars,
                              client,
                              baseline),
                          2)

        # assign jk, N^2(jk) to ik
        neighboring_clients = get_adjacent_clients(
            facility_decision_vars,
            client_decision_vars,
            client,
            baseline)

        if facilities[facility] is None:
            facilities[facility] = set()

        facilities[facility].union_update(neighboring_clients)
        facilities[facility].add(client)

        # remove jk, N^2(jk)
        clients.difference_update(neighboring_clients)
        clients.remove(facility)

    return facilities
