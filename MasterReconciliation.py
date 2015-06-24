import DP
import Greedy
import newickToVis
import ReconConversion
import orderGraph
import newickFormatReader
import ReconciliationGraph
from sys import argv
import copy

def Reconcile(argList):
	print fileName
	"""Takes command-line arguments of File, costs, and amount of desired reconciliations. Creates Files for 
	the host, parasite, and reconciliations"""
	fileName = argList[1]
	D = int(argList[2])
	T = int(argList[3])
	L = int(argList[4])
	k = int(argList[5])
	orderedGraphs = []
	host, paras, phi = newickFormatReader.getInput(fileName)
	hostRoot = findRoot(host)
	hostv = treeFormat(host)
	hostOrder = orderGraph.date(hostv)
	hostBranchs = branch(hostv, hostOrder)
	DTL, numRecon = DP.DP(host, paras, phi, D, T, L)
	DTLGraph = copy.deepcopy(DTL)
	rec = Greedy.Greedy(DTL, paras, k)
	graph = []
	for item in rec:
		graph.append(ReconciliationGraph.buildReconstruction(host, paras, item))
	for item in range(len(graph)):
			orderedGraphs += orderGraph.date(graph[item])
			#ReconConversion.convert(rec[item], DTLGraph, paras, fileName[:-7], item)
	#newickToVis.convert(fileName,hostBranchs)
	return numRecon, rec

def branch(tree, treeOrder):
	"""Computes Ultra-metric Branchlength from a tree dating"""
	branches = {}
	for key in tree:
		if key != None:
			for child in tree[key]:
				if child != None:
					branches[child] = abs(treeOrder[child] - treeOrder[key])
	for key in treeOrder:
		if not key in branches:
			branches[key] = 0
	return branches

def findRoot(Tree):
    """This function takes in a parasiteTree and returns a string with the name of
    the root vertex of the tree"""

    if 'pTop' in Tree:
    	return Tree['pTop'][1]
    return Tree['hTop'][1]

def InitDicts(tree):
	"""This function takes as input a tree dictionary and returns a dictionary with all of the bottom nodes 
	of the edges as keys and empty lists as values."""
	treeDict = {}
	for key in tree:
		if key == 'pTop':
			treeDict[tree[key][1]] = [] 
		elif key == 'hTop':
			treeDict[tree[key][1]] = []
		else:
			treeDict[key[1]] = []
	return treeDict

def treeFormat(tree):
	"""Takes a tree in the format that it comes out of newickFormatReader and converts it into a dictionary
	with keys which are the bottom nodes of the edge and values which are the children."""
	treeDict = InitDicts(tree)
	treeRoot = findRoot(tree)
	for key in tree:
		if key == 'hTop' or key == 'pTop':
			if tree[key][-2] == None:
				treeDict[treeRoot] = treeDict[treeRoot] + [tree[key][-2]]
			else:
				treeDict[treeRoot] = treeDict[treeRoot] + [tree[key][-2][1]]
			if tree[key][-1] == None:
				treeDict[treeRoot] = treeDict[treeRoot] + [tree[key][-1]]
			else:
				treeDict[treeRoot] = treeDict[treeRoot] + [tree[key][-1][1]]
		else:
			if tree[key][-2] == None:
				treeDict[key[1]] = treeDict[key[1]] + [tree[key][-2]]
			else:
				treeDict[key[1]] = treeDict[key[1]] + [tree[key][-2][1]]
			if tree[key][-1] == None:
				treeDict[key[1]] = treeDict[key[1]] + [tree[key][-1]]
			else:
				treeDict[key[1]] = treeDict[key[1]] + [tree[key][-1][1]]
	return treeDict

def main():
	Reconcile(argv)

if __name__ == "__main__": main()