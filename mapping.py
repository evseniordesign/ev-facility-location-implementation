"""
Basic mapping to the facility location problem.
Assumes the following format:
{
"facilities:" [{"lat": float, "long": float}],
"clients": [{"lat": float, "long": float}]
}
I really just made this up. Feel free to change
Also I think we should attach names to facilities, but that's
not a priority.
"""

import json
import math
from facility_location.algorithm import choose_facilities, Algorithms

def distance(p1, p2):
    return math.sqrt((p1['lat'] - p2['lat']) ** 2 +
                     (p1['long'] - p2['long']) ** 2)

def make_mapping(filename, facility_func, client_func):
    """
    Makes a mapping to the facility location problem using
    filename (json file with specified schema)
    facility_func (function from facility to facility cost)
    client_func (function from (client, facility) to client cost)
    """
    with open(filename) as datafile:
        data = json.load(datafile)
        
        fcosts = [float(facility_func(facility))
                  for facility in data['facilities']]

        ccosts = [[float(client_func(client, facility))
                   for facility in data['facilities']]
                   for client in data['clients']]

        return fcosts, ccosts
    

def test_mapping(filename):
    """
    A very simplistic mapping to the facility location problem.
    More of a proof of concept than an actual attempt.
    I just made it up, please try different mappings
    """
    # I guess opening the facility will take $1,000,000
    facility_func = lambda facility: 1000000

    # client
    client_func = lambda client, facility: distance(client, facility) * 1000

    return make_mapping(filename, facility_func, client_func)

def main():
    """
    Driver for the algorithm solver.
    """
    # The test I wrote seems to produce different results when
    # run deterministically vs when run probablistically. Maybe look
    # into that? Not really sure why this happened
    fcosts, ccosts = test_mapping('Data/test.json')
    print choose_facilities(fcosts, ccosts)
    print choose_facilities(fcosts, ccosts, algorithm=Algorithms.DET)

if __name__ == '__main__':
    main()
