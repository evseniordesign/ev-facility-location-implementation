import sys
import time
sys.path.append('../')
from facility_location.algorithm import choose_facilities
from mapping.cost_gen import get_fcost, get_ccost
from mapping.mapping import make_mapping, process_input

def main():
    with open('Data/atx_facilities.csv') as facfile, \
         open('Data/atx_clients.csv') as clifile:
             data = process_input({'csvfacility': facfile,
                                   'csvclient': clifile})

             for i in xrange(1, len(data['facilities'])):
                 for j in xrange(1, len(data['clients'])):
                     start_time = time.time();
                     curr_data = {'facilities': data['facilities'][:i],
                                  'clients': data['clients'][:j]}
                     make_mapping(curr_data, get_fcost, get_ccost)
                     choose_facilities(curr_data['facilities'], curr_data['clients'])
                     print i, j, time.time() - start_time

if __name__ == '__main__':
    main()
