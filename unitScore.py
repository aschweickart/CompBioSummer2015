

from DPcostscape import *

def unitScoreDTL(hostTree, parasiteTree, phi, D, T, L):
	""" Takes a hostTree, parasiteTree, tip mapping function phi, and duplication cost (D), 
	transfer cost (T), and loss cost (L) and returns the DTL graph in the form of a dictionary, 
	with event scores set to 1. Cospeciation is assumed to cost 0. """
	DTL = DP(hostTree, parasiteTree, phi, D, T, L)
	newDTL = {}
	for vertex in DTL:
		newDTL[vertex] = []
		for i in range(len(DTL[vertex]) - 1):
			event = DTL[vertex][i]
			event = event[:-1] + [1.0]
			newDTL[vertex] = newDTL[vertex] + [event]
		newDTL[vertex] = newDTL[vertex] + [DTL[vertex][-1]]
	return newDTL
