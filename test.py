"""
Temporary test file to run the algorithm code.
"""
from fgraph import Fgraph
print Fgraph.from_file('test.txt').get_lp_sol()['x']
