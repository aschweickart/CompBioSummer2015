import DP
import Greedy
import newickToVis
import ReconConversion
import orderGraph
import math

def Reconcile(fileName, D, T, L, k):
	host, paras, phi = DP.newickFormatReader.getInput(fileName)
	hostv = treeFormat(host)
	hostOrder = orderGraph.date(hostv)
	hostBranchs = branch(hostv,hostOrder)
	DTL = DP.DP(host, paras, phi, D, T, L)
	rec = Greedy.Greedy(DTL, paras, k)
	ReconConversion.convert(rec[0], fileName[:-7])
	newickToVis.convert(fileName,hostBranchs)
	return DTL, rec

def branch(tree, treeOrder):
	braches = {}
	for key in tree:
		for child in tree[key]:
			if child != None:
				branches[child] = math.abs(treeOrder[child] - treeOrder[key])
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