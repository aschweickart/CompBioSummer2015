from DP import *
from newickFormatReader import *
from Greedy import *




def GreedyNewick(newickFile, D, T, L, k):
	""" """
	H, P, phi = newickFormatReader(newickFile)
	DTL, numRecon = DP(H, P, phi, D, T, L)
	return Greedy(DTL, numRecon, P, k)


