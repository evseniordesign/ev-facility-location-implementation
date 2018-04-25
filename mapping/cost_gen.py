from common.helpers import distance
from census import get_ev_count, fill_tract_params
import math

C_SCHEMA = ['lat', 'long']
F_SCHEMA = ['lat', 'long']

SERVICE_RADIUS = 1
FAC_COST = 50

POWER_COST = 2  # Based on city needs
USER_COST = 15   # Opportunity cost for each user

TIME_COST = 0.11
PHYS_COST = 0.85

USE_LOT_AREA = False

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

    time_dist = client['time_dist'][facility['index']]
    phys_dist = client['phys_dist'][facility['index']]
    if phys_dist > SERVICE_RADIUS:
        phys_dist **= 2

    if USE_LOT_AREA:
        dist_cost = time_dist * TIME_COST + phys_dist * PHYS_COST
        return dist_cost*math.sqrt(facility['lotarea'])
        
    return time_dist * TIME_COST + phys_dist * PHYS_COST

def opp_cost(client):
    """
    Calculate opportunity cost.
    """
    return POWER_COST + get_ev_count(
        fill_tract_params(client)) * USER_COST
