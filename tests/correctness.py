"""
Rough test file that checks correctness by printing lower and upper bounds.
The lower bound is the LP (fewer constraints)
The upper bound is the rounding result (valid solution)
Therefore if the two are equal, the rounding result is optimal.
If they are close, then our algorithm is performing well.
If the upper bound is many times larger than the lower bound, then there is likely something wrong.
"""

import sys
sys.path.append('../') # Get all the necessary files on the path
from facility_location.algorithm import rounding_algorithm, get_cheapest_neighbor, get_probably_good_neighbor, init_clients, init_facilities
import facility_location.lp as lp
from mapping.cost_gen import get_fcost, get_ccost
from mapping.mapping import make_mapping, process_input
from itertools import product
import random

def cost(solution):
    """
    Print the cost of a rounding solution
    """
    output = 0
    for fac in solution.keys():
        output += fac['cost']
        for client in solution[fac]:
            output += client['costs'][fac['index']]

    return output

def run(percent):
    """
    Return the lower and upper bound, using the given percentage of
    clients and facilities from atx_clients and atx_facilities.
    """
    facfile = open('Data/atx_clients.csv')
    clifile = open('Data/atx_facilities.csv')

    data = process_input({'csvfacility': facfile, 'csvclient': clifile})

    random.shuffle(data['facilities'])
    random.shuffle(data['clients'])

    data['facilities'] = data['facilities'][:int(percent / 100.0 * len(data['facilities']))]
    data['clients'] = data['clients'][:int(percent / 100.0 * len(data['clients']))]
    make_mapping(data, get_fcost, get_ccost, use_time_dist=True)

    facility_costs = [facility['cost'] for facility in data['facilities']]
    client_costs = [client['costs'] for client in data['clients']]

    flat_ccosts = reduce(lambda acc, curr: acc + curr, client_costs)
    sol = lp.solve(facility_costs, flat_ccosts)

    facilities = init_facilities(data['facilities'], sol['x'])
    clients = init_clients(data['clients'], sol['x'], sol['y'])

    client_chooser = lambda client: client.lowest_pair_cost + client.get_expected_cost()
    facility_chooser = get_probably_good_neighbor
    result = rounding_algorithm(facilities, clients, client_chooser, facility_chooser)

    facfile.close()
    clifile.close()

    return sol['primal objective'], cost(result)

if __name__ == '__main__':
    for i in xrange(10, 101):
        lower, upper = run(i)
        print 'lower:', lower, 'upper:', upper
