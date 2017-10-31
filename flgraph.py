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

		self._fcosts = map(int, f.readline().split())

		try:
			for i in xrange(0, self.c_len):
				client = map(int, f.readline().split())
				if self._ccosts is None:
					self._ccosts = [client]
				else:
					self._ccosts.append(client)
				if length(client) != f_len:
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
		print "Constructor"

	def c_flat():
		return np.transpose(self._ccosts).flatten().tolist()
