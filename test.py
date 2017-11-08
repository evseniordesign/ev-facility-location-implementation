from neighborhood import neighborhood as nb
from flgraph import fgraph as fg
import lp


myg = fg("test.txt")
sol = lp.solve(*fg.read_graph(myg))['x']
mynb = nb(myg, sol)

print sol
print mynb.n_mat

print mynb.getNeighbors(0)
print mynb.getFacilityNeighbors(4)
print mynb.getN2(0)