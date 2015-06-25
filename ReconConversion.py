# PROF WU VISUALIZATION RECONCILIATION FORMAT CONVERSION
import newickFormatReader
import DP
import Greedy
import copy
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
	D = argList[2]
	T = argList[3]
	L = argList[4]
	k = argList[5]
	fileName = newickFile[:-7]
	f = open(fileName+"freqFile.txt", 'w')
	individSum = []
	totalSum = 0
	host, paras, phi = newickFormatReader.getInput(newickFile)
	DTL, numRecon = DP.DP(host, paras, phi, D, T, L)
	DTLGraph = copy.deepcopy(DTL)
	reconciliation = Greedy.Greedy(DTL, paras, k)
	for index in reconciliation:
		currentScore = 0
		freqDict = frequencyDict(DTLGraph, index)
		for key in index:
			currentScore+=freqDict[key]
		individSum.append(currentScore)
		totalSum += currentScore
	print individSum
	print totalSum
	f.write(str(individSum)+'\n')
	f.write(str(totalSum))	
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































