# calcCostscapeScore.py
# Juliet Forman and Srinidhi Srinivasan
# July 2015

# This file contains functions for calculating scores for events in the DTL 
# based on their frequency among the different regions of costscape. The 
# score for each event is the fraction of regions in costscape in which the 
# event appears. The main function is newScoreWrapper, and the other 
# functions are helper functions for newScoreWrapper.

from DP import *
from costscapeScore import *
from sys import argv
import newickFormatReader

def deleteCommas(pointList):
	"""This function takes as input a list of points, returns a new list 
	which is the same as pointList but with all commas removed."""

	newList = []
	for point in pointList:
		string = ""
		for i in point:
			if i != ',':
				string = string + i
		newList.append(string)
	return newList


def getDTLVals(pointList):
	"""This function takes as input a list of centroids of the costscape 
	regions, and returns a list of tuples containing the T, L costs for each 
	region."""

	pointList = deleteCommas(pointList)
	DTLPairs = []
	for point in pointList:
		coordList = point[7:-1].split()
		pair = []
		#pair = (float(coordList[0]),float(coordList[1])) ?
		for i in coordList:
			pair.append(float(i))
		DTLPairs.append(tuple(pair))
	return DTLPairs


def getCostscapeDTLs(DTLPairs, hostTree, parasiteTree, phi):
	"""This function takes as input DTLPairs, a list of tuples with T and L 
	costs, and the hostTree, parasiteTree, and phi. It returns a list of DTLs 
	who scores are computed with the T and L values from each element in 
	DTLPairs."""
	
	DTLList = []
	for i in DTLPairs:
		newDTL = DP(hostTree, parasiteTree, phi, 1, i[0], i[1])[0]
		DTLList.append(newDTL)
	return DTLList


def changeDTLScores(originalDTL, DTLList):
	"""This function takes as input the originalDTL and a list DTLList of the 
	DTLs from each region in costscape. This function calculates a new score 
	for each event in originalDTL, and returns a newDTL with these scores."""

	newDTL = {}
	numDTL = len(DTLList)
	for event in originalDTL:
		counter = 0
		for DTL in DTLList:
			if event in DTL:
				counter += 1
		newScore = 1.0*counter/numDTL
		oldVal = originalDTL[event]
		oldVal[0][-1] = newScore
		newDTL[event] = oldVal
	return newDTL


def newScoreWrapper(newickFile, switchLo, switchHi, lossLo, lossHi, D, T, L):
	"""This function takes as input hostTree, parasiteTree, phi, duplication 
	cost D, transfer cost T, and loss cost L, and returns the newDTL whose 
	scores were calculated from costscape."""

	H, P, phi = newickFormatReader.getInput(newickFile)
	originalDTL, numRecon, leaves = DP(H, P, phi, D, T, L)
	pointList = findCenters(newickFile, switchLo, switchHi, lossLo, lossHi)
	DTLPairs = getDTLVals(pointList)
	DTLList = getCostscapeDTLs(DTLPairs, H, P, phi)
	newDTL = changeDTLScores(originalDTL, DTLList)
	return newDTL, numRecon, leaves
