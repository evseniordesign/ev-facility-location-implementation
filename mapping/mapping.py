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
import requests
from cost_gen import get_fcost, get_ccost

BASE_MAP_REQ = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

def process_input(datafiles):
    """
    Convert json and csv files to an array of dicts for cost generation.
    """
    if 'json' in datafiles:
        return json.loads(datafiles['json'].read())
    elif 'csvfacility' in datafiles and 'csvclient' in datafiles:
        return {'facilities': [curr for curr in csv.DictReader(datafiles['csvfacility'])],
                'clients': [curr for curr in csv.DictReader(datafiles['csvclient'])]
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
        get_time_distance(data)

    for index in xrange(len(data['facilities'])):
        facility = data['facilities'][index]
        facility['index'] = index
        facility['cost'] = float(facility_func(facility))

    for index in xrange(len(data['clients'])):
        client = data['clients'][index]
        client['index'] = index
        client['costs'] = [float(client_func(client, facility)) for facility in data['facilities']]

def encode_location(location):
    """
    Convert location to string that is inserted into URL.
    """
    return '%s,%s' % (location['lat'], location['long'])

def get_time_distance(data):
    """
    Add time_dist field that represents how long it takes
    to drive from a given facility to a given client.
    client['time_dist'][fac_num] contains the distance between the two in seconds.
    """
    origins = '|'.join(encode_location(cli) for cli in data['clients'])
    destinations = '|'.join(encode_location(fac) for fac in data['facilities'])
    maps_request = BASE_MAP_REQ + 'origins=' + origins + '&destinations=' + destinations
    map_data = requests.get(maps_request).json()

    for cli, results in zip(data['clients'], map_data['rows']):
        cli['time_dist'] = [elem['duration']['value'] for elem in results['elements']]
