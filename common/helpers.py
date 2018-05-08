# helpers.py
# contains helper functions for various classes

from functools import partial
from math import sin, cos, sqrt, atan2, radians
from multiprocessing import Pool
import requests
import json
import os

BASE_MAP_REQ = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
M_TO_MI = 0.000621371
KM_TO_M = 1000
SEC_TO_MIN = 1 / 60.0
DEG_TO_MI = 1 / 69.0
CLI_PER_REQ = 4
FAC_PER_REQ = 25
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

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
    """
    Send request for distances between the given clients and facilities.
    Uses the Google Maps Distance Matrix API.
    """
    origins = '|'.join(encode_location(cli) for cli in clientchunk)
    destinations = '|'.join(encode_location(fac) for fac in facilitychunk)
    maps_request = BASE_MAP_REQ + 'origins=' + origins + '&destinations=' + destinations
    return requests.get(maps_request).json()['rows']

def try_cache(data):
    """
    Try to get distance data from cache.
    Returns true if all values could be obtained from cache.
    """
    try:
        cachefile = open(os.path.join(BASE_FOLDER, 'cache.json'), 'r')
    except IOError:
        return False

    cache = json.load(cachefile)

    for client in data['clients']:
        client['time_dist'] = []
        client['phys_dist'] = []
        client_str = ' '.join((client['lat'], client['long']))

        for facility in data['facilities']:
            if 'dummy' in facility:
                continue

            facility_str = ' '.join((facility['lat'], facility['long']))

            key1 = ' '.join((facility_str, client_str))
            key2 = ' '.join((client_str, facility_str))
            key = None

            if key1 in cache:
                key = key1
            elif key2 in cache:
                key = key2

            if key:
                time = cache[key]['time']
                dist = cache[key]['dist']
                client['time_dist'].append(float(time))
                client['phys_dist'].append(float(dist))
            else:
                cachefile.close()
                return False

    cachefile.close()
    return True


def get_map_distance(data):
    """
    Add time_dist field that represents how long it takes
    to drive from a given facility to a given client.
    client['time_dist'][fac_num] contains the distance between the two in seconds.
    """
    # Use line dist if not found in cache
    if not try_cache(data):
        for client in data['clients']:
            client['phys_dist'] = [distance(float(client['lat']), float(client['long']),
                                            float(facility['lat']), float(facility['long']))
                                   * KM_TO_M * M_TO_MI
                                   for facility in data['facilities'] if 'dummy' not in facility]

            client['time_dist'] = [0 for _ in xrange(len(data['facilities']))]

    # Not currently using API because it is expensive
    # 2500 requests/day free limit
    return

    pool = Pool()
    # API can only handle 100 elements at once, and at most
    # 25 origins or 25 destinations
    # Break data into 100 element chunks that the API will process
    dist_results = [pool.map_async(partial(matrix_request, clientchunk),
                                   chunks(data['facilities'], FAC_PER_REQ))
                    for clientchunk in chunks(data['clients'], CLI_PER_REQ)]

    # Combine dist_results into usable format
    for cindex, clientchunk in enumerate(chunks(data['clients'], CLI_PER_REQ)):
        api_result = dist_results[cindex].get()

        for i, client in enumerate(clientchunk):
            client['time_dist'] = [elem['duration']['value'] * SEC_TO_MIN
                                   for elem in api_result[i]['elements']]

            client['phys_dist'] = [elem['distance']['value'] * M_TO_MI
                                   for elem in api_result[i]['elements']]

    pool.close()
    pool.join()
