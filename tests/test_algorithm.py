import sys
import unittest
sys.path.append('../')
from facility_location.algorithm import choose_facilities
from mapping.cost_gen import get_fcost, get_ccost
from mapping.mapping import make_mapping, process_input
from itertools import product

def cost(solution):
    output = 0
    for fac in solution.keys():
        output += fac['cost']
        for client in solution[fac]:
            output += client['costs'][fac.index]

    return output

def bruteforce(data):
    min_cost = 0
    for permutation in product(range(len(data['facilities'])), repeat=len(data['clients'])):
        permutation = list(permutation)
        curr_cost = 0
        facilities_used = set()
        for fac_num, client in zip(permutation, data['clients']):
            facilities_used.add(fac_num)
            curr_cost += client['costs'][fac_num]

        for fac_num in facilities_used:
            curr_cost += data['facilities'][fac_num]['cost']

        if curr_cost < min_cost or min_cost == 0:
            min_cost = curr_cost

    return min_cost

def check_against_bruteforce(files):
    data = process_input(files)
    make_mapping(data, get_fcost, get_ccost)
    algo_cost = cost(choose_facilities(data['facilities'], data['clients']))
    return bruteforce(data) * 2 >= algo_cost

class TestAlgorithm(unittest.TestCase):
    def test_json_small(self):
        with open('Data/test.json') as datafile:
            self.assertTrue(check_against_bruteforce({'json': datafile}))

    def test_json_bigger(self):
        with open('Data/othertest.json') as datafile:
            self.assertTrue(check_against_bruteforce({'json': datafile}))

    def test_csv_small(self):
        with open('Data/test_facilities_small.csv') as facfile, \
             open('Data/test_clients_small.csv') as clifile:

            self.assertTrue(check_against_bruteforce({
                'csvfacility': facfile,
                'csvclient': clifile
                }))

if __name__ == '__main__':
    unittest.main()
