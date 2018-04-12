# helpers.py
# contains helper functions for various classes

from functools import partial
from math import sin, cos, sqrt, atan2, radians
from multiprocessing import Pool
import requests
import json

BASE_MAP_REQ = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
M_TO_MI = 0.000621371
SEC_TO_MIN = 1 / 60.0
CLI_PER_REQ = 4
FAC_PER_REQ = 25

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def distance(lat1, long1, lat2, long2):
    """
    Input two arrays of lat and long coordinates
    Return the straight line distance between them
    using the Haversine formula
    """
    R = 6373.0

    dlon = radians(long2 - long1)
    dlat = radians(lat2 - lat1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def encode_location(location):
    """
    Convert location to string that is inserted into URL.
    """
    return '%s,%s' % (location['lat'], location['long'])

def matrix_request(clientchunk, facilitychunk):
    origins = '|'.join(encode_location(cli) for cli in clientchunk)
    destinations = '|'.join(encode_location(fac) for fac in facilitychunk)
    maps_request = BASE_MAP_REQ + 'origins=' + origins + '&destinations=' + destinations
    return requests.get(maps_request).json()['rows']

def get_map_distance(data):
    """
    Add time_dist field that represents how long it takes
    to drive from a given facility to a given client.
    client['time_dist'][fac_num] contains the distance between the two in seconds.
    """
    with open('cache.json', 'r') as cachefile:
        cache = json.load(cachefile)

        for clientnum, client in enumerate(data['clients']):
            client['time_dist'] = []
            client['phys_dist'] = []
            for facilitynum, facility in enumerate(data['facilities']):
                if 'dummy' in facility:
                    continue

                time = cache[clientnum][facilitynum]['time']
                dist = cache[clientnum][facilitynum]['dist']
                client['time_dist'].append(float(time))
                client['phys_dist'].append(float(dist))

        # Currently just use the cache
        return

    pool = Pool()
    dist_results = [pool.map_async(partial(matrix_request, clientchunk),
                                   chunks(data['facilities'], FAC_PER_REQ))
                    for clientchunk in chunks(data['clients'], CLI_PER_REQ)]

    for cindex, clientchunk in enumerate(chunks(data['clients'], CLI_PER_REQ)):
        result = dist_results[cindex].get()

        for i, client in enumerate(clientchunk):
            client['time_dist'] = [elem['duration']['value'] * SEC_TO_MIN
                                   for elem in result[i]['elements']]

            client['phys_dist'] = [elem['distance']['value'] * M_TO_MI
                                   for elem in result[i]['elements']]

    pool.close()
    pool.join()
