from common.helpers import distance
from census import get_ev_count, fill_tract_params

C_SCHEMA = ['lat', 'long']
F_SCHEMA = ['lat', 'long']

SERVICE_RADIUS = 4
FAC_COST = 50

POWER_COST = 2  # Based on city needs
USER_COST = 15   # Opportunity cost for each user

def get_fcost(facility):
    """
    Facility cost function. Currently has a fixed cost
    value based on FAC_COST above.
    """
    if "dummy" in facility:
        return 0
    else:
        return FAC_COST

def get_ccost(client, facility):
    """
    Function to calculate client cost. 
    Currently is the distance from client to facility.
    """
    if "dummy" in facility:
        return opp_cost(client) 

    lat1 = float(facility['lat'])
    long1 = float(facility['long'])
    lat2 = float(client['lat'])
    long2 = float(client['long'])

    dist = distance(lat1, long1, lat2, long2)
    return dist

def opp_cost(client):
    """
    Calculate opportunity cost.
    """
    return POWER_COST + get_ev_count(
        fill_tract_params(client)) * USER_COST