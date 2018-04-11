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

import csv
import json
from cost_gen import get_fcost, get_ccost
from common.helpers import get_distance

def process_input(datafiles):
    """
    Convert json and csv files to an array of dicts for cost generation.
    """
    if 'json' in datafiles:
        return json.loads(datafiles['json'].read())
    elif 'csvfacility' in datafiles and 'csvclient' in datafiles and 'csvpower' in datafiles:
        return {'facilities': [curr for curr in csv.DictReader(datafiles['csvfacility'])],
                'clients': [curr for curr in csv.DictReader(datafiles['csvclient'])],
                'powerlines': [curr for curr in csv.DictReader(datafiles['csvpower'])]
               }

def make_mapping(data, facility_func, client_func,
                 use_dummy=True, use_time_dist=False):
    """
    Makes a mapping to the facility location problem using
    filename (json file with specified schema)
    facility_func (function from facility to facility cost)
    client_func (function from (client, facility) to client cost)
    """
    if use_dummy:
        data['facilities'].append({'dummy': True})

    if use_time_dist:
        get_distance(data)

    for index in xrange(len(data['facilities'])):
        facility = data['facilities'][index]
        facility['index'] = index
        facility['cost'] = float(facility_func(facility))
        print facility['cost']

    for index in xrange(len(data['clients'])):
        client = data['clients'][index]
        client['index'] = index
        client['costs'] = [float(client_func(client, facility)) for facility in data['facilities']]
        print 'client'
        print client['costs']
