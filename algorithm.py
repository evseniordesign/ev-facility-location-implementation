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

def get_adjacent_facilities(facilities, decision_vars, baseline):
    """
    Get adjacent facilities of a given client.
    """
    adjacent_facilities = set()
    return set()

def get_adjacent_clients(facilities, decision_vars, baseline):
    """
    Get clients adjacent to facilities of a given client.
    """
    return set()

def get_min(dual):
    """
    Get min vj* from the dual LP.
    """
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
    # if decision variable is less than baseline, treat it as 0
    num_facilities = len(facility_costs)
    baseline = 1.0 * len(facility_costs) / len(client_costs) / 2

    clients = set(xrange(0, len(client_costs)))
    facilities = dict()

    decision_vars = list(primal)
    # needed for the loop
    client_decision_vars = decision_vars[num_facilities:]
    facility_decision_vars = decision_vars[:num_facilities]
    get_min_cost = lambda acc, curr: acc if facility_costs[acc] < facility_costs[curr] else curr

    while clients != set():
        # choose jk
        client = get_min(dual)

        # choose ik
        # start acc at 2 so that
        facility = reduce(get_min_cost,
                          get_adjacent_facilities(
                              facility_decision_vars,
                              client_decision_vars[client],
                              baseline),
                          2)

        # assign jk, N^2(jk) to ik
        neighboring_clients = get_adjacent_clients(
            facility_decision_vars,
            client_decision_vars[client],
            baseline)

        if facilities[facility] is None:
            facilities[facility] = set()

        facilities[facility].union_update(neighboring_clients)
        facilities[facility].add(client)

        # remove jk, N^2(jk)
        clients.difference_update(neighboring_clients)
        clients.remove(facility)

    return facilities
