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

import numpy as np
import pandas as pd

from facility_location.algorithm import choose_facilities, Algorithms
from cost_gen import get_fcost, get_ccost

def distance(p1, p2):
    return math.sqrt((p1['lat'] - p2['lat']) ** 2 +
                     (p1['long'] - p2['long']) ** 2)

def process_input(file):
    if file.filename.rsplit('.', 1)[1].lower() == 'json':
        data_out = json.loads(file.read())
        data_out["facilities"].append({"dummy": True})
        return data_out
    elif file.filename.rsplit('.', 1)[1].lower() == 'csv':
        # TODO: CSV processing
        return None


def make_mapping(data, facility_func, client_func):
    """
    Makes a mapping to the facility location problem using
    filename (json file with specified schema)
    facility_func (function from facility to facility cost)
    client_func (function from (client, facility) to client cost)
    """
    fcosts = [float(facility_func(facility))
              for facility in data['facilities']]

    ccosts = [[float(client_func(client, facility))
               for facility in data['facilities']]
               for client in data['clients']]

    return fcosts, ccosts
    

# set "gen" to True if you'd like to use generated facility data based on
# the datafile instead of the actual data
def test_mapping(filename, gen = False):
    """
    A very simplistic mapping to the facility location problem.
    More of a proof of concept than an actual attempt.
    I just made it up, please try different mappings
    """
    with open(filename) as datafile:
        data = json.load(datafile)

        # I guess opening the facility will take $1,000,000
        #facility_func = lambda facility: 1000000

        #client_func = lambda client, facility: distance(client, facility) * 1000
        if gen:
            data['facilities'] = generate(data['facilities'])

        return make_mapping(data, get_fcost, get_ccost)

def generate(facilities):
    # locations = pd.read_csv(filename)
    locations = pd.DataFrame(facilities)

    centroid = (np.sum(locations.lat) / len(locations.lat), np.sum(locations.long) / len(locations.long))

    lat_normalized = []
    for i in locations.lat:
        lat_normalized.append(locations.lat - centroid[0])

    long_normalized = []
    for i in locations.long:
        long_normalized.append(locations.long - centroid[1])

    cov = np.cov(lat_normalized, long_normalized)
    # cov[0][0]
    # cov[0][len(cov[0])/ 2] # len/2

    # set this range to however many values you want to generate
    out = []
    for i in range(0,100):
        vals = np.random.multivariate_normal(centroid, [[cov[0][0], cov[0][len(cov) / 2]],[cov[1][0], cov[1][len(cov) / 2]]])
        out.append(
            {
                'lat': vals[0],
                'long': vals[1]
            }
        )
            


    print("Generate out: ") 
    print(out)
    print("---")

    return out

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
