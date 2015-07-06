#calcCostscapeScore.py
#July 2015
#JULIET AND SRINIDHI

from DPcostscape import *
from costscapeScore import *
from sys import argv


def deleteCommas(pointList):
	"""Takes in a list of points, returns the same list except without commas"""

	newList = []
	for point in pointList:
		string = ""
		for i in point:
			if i != ',':
				string = string + i
		newList.append(string)
	return newList


def getDTLVals(pointList):
	"""Takes in a list of centroids of the costscape regions, and returns a list of tuples 
	containing the T, L costs for each region."""
	pointList = deleteCommas(pointList)
	DTLPairs = []
	for point in pointList:
		coordList = point[7:-1].split()
		pair = []
		for i in coordList:
			pair.append(float(i))
		DTLPairs.append(tuple(pair))
	return DTLPairs

def getCostscapeDTLs(DTLPairs, hostTree, parasiteTree, phi):
	"""takes as input DTLPairs, a list of tuples with T and L costs, and the hostTree, parasiteTree, and phi. 
	It returns a list of DTLs who scores are computed with the T and L values from DTLPairs"""
	DTLList = []
	for i in DTLPairs:
		newDTL = DP(hostTree, parasiteTree, phi, 1, i[0], i[1])
		DTLList.append(newDTL)
	return DTLList

def changeDTLScores(originalDTL, DTLList):
	"""takes as input the originalDTL and a list DTLList of the DTLs from each region in costscape. This function
	calculates a new score for each event in originalDTL, and returns a newDTL with these scores"""
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
	"""takes as input hostTree, parasiteTree, phi, D, T, and L, and returns the newDTL whose scores were calculated from
	costscape."""
	# newickFile = argList[1]
	# switchLo = float(argList[2])
	# switchHi = float(argList[3])
	# lossLo = float(argList[4])
	# lossHi = float(argList[5])
	# D = float(argList[6])
	# T = float(argList[7])
	# L = float(argList[8])
	H, P, phi = newickFormatReader(newickFile)
	originalDTL = DP(H, P, phi, D, T, L)
	pointList = findCenters(newickFile, switchLo, switchHi, lossLo, lossHi)
	DTLPairs = getDTLVals(pointList)
	DTLList = getCostscapeDTLs(DTLPairs, H, P, phi)
	newDTL = changeDTLScores(originalDTL, DTLList)
	return newDTL

# def main():
# 	newScoreWrapper(argv)

# if __name__=="__main__": main()