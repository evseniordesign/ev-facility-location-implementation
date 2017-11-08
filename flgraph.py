import numpy as np

class fgraph:
    f_len = None
    c_len = None
    _fcosts = None
    _ccosts = None

    def __init__(self, fn):
       f = open(fn)

       lengths = f.readline().split()
       self.f_len = int(lengths[0])
       self.c_len = int(lengths[1])

       self._fcosts = map(float, f.readline().split())

       try:
            for i in xrange(0, self.c_len):
                client = map(float, f.readline().split())
                if self._ccosts is None:
                    self._ccosts = [client]
                else:
                    self._ccosts.append(client)
                if len(client) != self.f_len:
                    raise ValueError()
       except ValueError as err:
           print "_fcosts and _ccosts must contain f_len values."
       except Exception as err:
           print "Invalid Input File Format"
           print "Proper Format is"
           print "f_len c_len"
           print "[_fcosts]"
           print "[_ccosts][0]"
           print "[_ccosts][1]"
           print ". . ."

    def getfcost(self, facility):
        return _fcosts[facility]

    def getccost(self, client, facility):
        return _ccosts[client][facility]

    def getNeighbors(self, facility):
        try:
            neighbor = np.transpose(self._ccosts)[facility]
        except IndexError as err:
            print "fgraph instance contains " + str(f_len) + " facilities."

    def read_graph(fg):
        ccosts = reduce((lambda acc, curr: acc + curr), fg._ccosts)
        return (fg._fcosts, ccosts)
