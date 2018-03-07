from common.helpers import distance

C_SCHEMA = ['lat', 'long']
F_SCHEMA = ['lat', 'long']

SERVICE_RADIUS = 4
FAC_COST = 1000

POWER_COST = 2  # Based on city needs
USER_COST = 5   # Opportunity cost for each user

def get_fcost(facility):
    """
    Facility cost function. Currently has a fixed cost
    value based on FAC_COST above.
    """
    if "dummy" in facility:
        return 0
    else:
        return FAC_COST
    
    """
    This code used population instead of a fixed facility
    cost value. Leaving this here in case we want to use 
    population or any other parameter in facility cost values.
    """
    #self.graph._fcosts = []

    # for f_index, f_row in self.f_data.iterrows():
    #   population = 0
    #   for c_index, c_row in self.c_data.iterrows():
    #       lat1 = f_row['LAT']
    #       long1 = f_row['LONG']
    #       lat2 = c_row['LATITUDE']
    #       long2 = c_row['LONGITUDE']

    #       distance = getDistance(lat1, long1, lat2, long2)
    #       if(abs(distance) <= SERVICE_RADIUS):
    #           population = population + c_row['POPULATION']
    #   self.graph._fcosts.append(self.fcost_func(population))


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
    return POWER_COST + float(client['population']) * USER_COST
