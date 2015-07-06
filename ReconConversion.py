#ReconConversion.py
#July 2015

# PROF WU VISUALIZATION RECONCILIATION FORMAT CONVERSION
import newickFormatReader
import DP
import HeyJuliet
import copy
import calcCostscapeScore
import MasterReconciliation
from sys import argv
def convert(reconciliation, DTL, ParasiteTree, outputFile, n):
	"""Takes as input a dictionary of a reconciliation between host and parasite trees, a DTL graph, and a string containing the name of a 
	file where it will put the output. The function outputs the same tree converted to brecon format. 
	Note that for losses, the parasite node in the brecon representation is the parent of the given parasite node. 
	This accounts for the brecon format's inability to handle losses"""
	freqSum = 0
	D = {'T': 'trans', 'S': 'spec', 'D': 'dup', 'C': 'gene', 'L': 'loss'}
	f = open(outputFile + str(n) + ".mowgli.brecon", 'w')
	event = ""
	pParent = parasiteParentsDict(ParasiteTree)
	freqDict = frequencyDict(DTL, reconciliation)
	for key in reconciliation:
		freqSum += freqDict[key]
		event = reconciliation[key][0]
		f.write(key[0] + '\t' + key[1] + '\t' + D[event] + '\t' + str(freqDict[key]) + '\n')
	f.close()

def freqSummation(argList):
	newickFile = argList[1]
	D = float(argList[2])
	T = float(argList[3])
	L = float(argList[4])
	freqType = argList[5]
	switchLo = float(argList[6])
	switchHi = float(argList[7])
	lossLo = float(argList[8])
	lossHi = float(argList[9])
	fileName = newickFile[:-7]
	f = open(fileName+"freqFile.txt", 'w')
	host, paras, phi = newickFormatReader.getInput(newickFile)
	DTL, numRecon = DP.DP(host, paras, phi, D, T, L)
	if freqType == "Frequency":
		newDTL = DTL
	elif freqType == "xscape":
		newDTL = calcCostscapeScore.newScoreWrapper(newickFile, switchLo, switchHi, lossLo, lossHi, D, T, L)
	elif freqType == "unit":
		newDTL = MasterReconciliation.unitScoreDTL(host, paras, phi, D, T, L)
	scoresList, reconciliation = HeyJuliet.Greedy(newDTL, paras)
	totalSum = 0
	for score in scoresList:
		totalSum +=score
	for index in reconciliation:
		totalColst = 0
		for key in index:
			if index[key][0] == "L":
				totalColst+=L
			elif index[key][0] == "T":
				totalColst+=T
			elif index[key][0] == "D":
				totalColst+=D
	f.write(str(scoresList)+'\n')
	f.write(str(totalSum)+'\n')
	f.write(str(totalColst)+'\n')
	f.write(str(numRecon))
	f.close()

def frequencyDict(DTL, reconciliation):
	""" """
	freqDict = {}
	for key in reconciliation:
		events = DTL[key][:-1]
		for event in events:
			if event[0] == reconciliation[key][0] and event[1] == reconciliation[key][1] and event[2] == reconciliation[key][2]:
				freqDict[key] = event[-1]
	return freqDict

def parasiteParentsDict(P):
	"""Takes a parasite tree with edges as keys and returns a dictionary with 
	keys which are the bottom nodes of those edges and values which are the top nodes of 
	those edges."""

	parentsDict = {}
	for key in P:
		if key == 'pTop':
			parentsDict[P[key][1]] = P[key][0]
		else:
			parentsDict[key[1]] = P[key][0]
	return parentsDict

def main():
	freqSummation(argv)

if __name__ == "__main__": main()































