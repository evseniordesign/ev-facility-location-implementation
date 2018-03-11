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
import math

from cost_gen import get_fcost, get_ccost

def process_input(datafiles):
    if 'json' in datafiles:
        return json.loads(datafiles['json'].read())
    elif 'csvfacility' in datafiles and 'csvclient' in datafiles:
        return {'facilities': [curr for curr in csv.DictReader(datafiles['csvfacility'])],
                'clients': [curr for curr in csv.DictReader(datafiles['csvclient'])]
               }

def make_mapping(data, facility_func, client_func, use_dummy=True):
    """
    Makes a mapping to the facility location problem using
    filename (json file with specified schema)
    facility_func (function from facility to facility cost)
    client_func (function from (client, facility) to client cost)
    """
    if use_dummy:
        data['facilities'].append({'dummy': True})

    for facility in data['facilities']:
        facility['cost'] = float(facility_func(facility))

    for client in data['clients']:
        client['costs'] = [float(client_func(client, facility)) for facility in data['facilities']]
