"""
This module generates census tract data based on a gamma distribution
and means and standard deviations computed in a paper [needs citation].
The module takes census tract data and estimates the number of
Electric Vehicle users in a tract.

The parameters:
Total population of tract (exposure variable)
Fraction of population 16 years old or younger 
Median age (years) 
Male fraction 
African American fraction 
Average household size (# persons) 
Fraction of pop. with Bachelor's degree or higher
Population density (per square mile)
Fraction of workers commuting by driving 
Mean household income (dollars per year, in 2010) 
Fraction of households with income over $100,000 
Fraction of families below poverty level 
Land use balance
Employment density per square mile
"""

import numpy as np
import math

census_params = {
    'population' : {
        'mean': 4841,
        'stddev': 2450,
    },
    'age_below_16_fraction' : {
        'mean': .236,
        'stddev': 0.059,
        'beta': 1.05
    },
    'median_age' : {
        'mean' : 35.18,
        'stddev' : 6.652,
        'beta': .0248
    },
    'male_fraction' : {
        'mean': .495,
        'stddev': 0.033,
        'beta': 3.91
    },
    'african_american_fraction' : {
        'mean': .119,
        'stddev': .164,
        'beta': -2.64
    },
    'average_household_size' : {
        'mean': 2.77,
        'stddev': .5,
        'beta': -.42
    },
    'fraction_with_at_least_bachelors' : {
        'mean': .248,
        'stddev': .191,
        'beta': 1.36
    },
    'population_density' : {
        'mean': 3103,
        'stddev': 3288,
        'beta': -.0000794
    },
    'driving_commuter_fraction' : {
        'mean': .783,
        'stddev': 0.091,
        'beta': .36
    },
    'mean_household_income' : {
        'mean': 66416,
        'stddev': 36273,
        'beta': -.00000144
    },
    '100K+_income_fraction' : {
        'mean': .186,
        'stddev': .166,
        'beta': .97
    },
    'poverty_fraction' : {
        'mean': .144,
        'stddev': .124,
        'beta': -.26
    },
    'land_use_balance' : {
        'mean': .645,
        'stddev': .229,
        'beta': .3
    },
    'employment_density' : {
        'mean': 1200.1,
        'stddev': 1379.2,
        'beta': -.0000688
    }
}

def get_gamma_params(mean, var):
	theta = var/mean
	k = mean/theta
	return k, theta

def fill_tract_params(tract={}):
    for param in census_params:
        if param in tract:
            continue
        mean = census_params[param]['mean']
        sd = census_params[param]['stddev']
        k, theta = get_gamma_params(mean, sd*sd)
        estimate = np.random.gamma(k, theta, 1)[0]
        tract[param] = estimate
    return tract

def tract_to_string(tract):
    for param in tract:
        print(param.replace("_", " ").title() + ": " + str(tract[param]))
    print(" ")

def get_ev_count(data):
    """
    Use a poisson lognormal model to calculate the expected number
    of electric vehicle in each zone. The variables are listed in the top docstring.

    The parameters are based on this research paper:
    https://scholarworks.montana.edu/xmlui/bitstream/handle/1/9169/Wang_JTG_2015_A1b.pdf
    """

    pop = int(data['population'])
    pop = pop if pop > 0 else 1
    #beta = [1.05, .0248, 3.91, -2.64, -.42, 1.36, -.0000794, .36, -.00000144, .97, -.26, .3, -.0000688]
    E = math.log(pop)

    ev_count = 0
    for param in census_params:
        if param == 'population':
            continue
        ev_count += census_params[param]['beta'] * data[param]

    return E*math.exp(E + ev_count - 7.54)