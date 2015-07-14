# reconciliationGraph.py

# Srinidhi Srinivasan, Juliet Forman
# July 2015

# This file contains function for building the cycle checking graph, 
# reconGrap, which is in the form of a dictionary. This dictionary has keys 
# that are nodes and values that are a list of all the children. The 
# reconGraph represents edges between nodes that show the temporal 
# relationship between the host tree and the parasite Tree. The main function
# in this file is buildReconstruction and the rest of the functions are 
# helper function that are used by buildReconstruction

def findRoot(Tree):
	"""This function takes in a tree and returns a string with the name of 
	the root vertex of the tree."""

	if 'pTop' in Tree:
		return Tree['pTop'][1]
	return Tree['hTop'][1]

def InitDicts(tree):
	"""This function takes as input a tree dictionary and returns a dictionary
	with all of the bottom nodes of the edges as keys and empty lists as 
	values."""

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
	"""Takes a tree in the format that it comes out of newickFormatReader and
	converts it into a dictionary with keys which are the bottom nodes of the
	edges and values which are the children."""

	treeDict = InitDicts(tree)
	treeRoot = findRoot(tree)
	for key in tree:
		#deal with case where the key is not in tuple form
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
			#where key is in tuple form
			if tree[key][-2] == None:
				treeDict[key[1]] = treeDict[key[1]] + [tree[key][-2]]
			else:
				treeDict[key[1]] = treeDict[key[1]] + [tree[key][-2][1]]
			if tree[key][-1] == None:
				treeDict[key[1]] = treeDict[key[1]] + [tree[key][-1]]
			else:
				treeDict[key[1]] = treeDict[key[1]] + [tree[key][-1][1]]
	return treeDict

def parentsDict(H, P):
	"""Takes a host and a parasite tree with edges as keys and returns a 
	dictionary with keys which are the bottom nodes of those edges and values
	which are the top nodes of those edges."""

	parentsDict = {}
	for key in H:
		if key == 'hTop':
			parentsDict[H[key][1]] = H[key][0]
		else:
			parentsDict[key[1]] = H[key][0]
	for key in P:
		if key == 'pTop':
			parentsDict[P[key][1]] = P[key][0]
		else:
			parentsDict[key[1]] = P[key][0]
	return parentsDict

def uniquify(list):
	"""Takes as input a list and returns a list containing only the unique 
	elements of the input list."""

	keys = {}
	for e in list:
		keys[e] = 1
	return keys.keys()

def buildReconstruction(HostTree, ParasiteTree, reconciliation):
	"""Takes as input a host tree, a parasite tree, and a reconciliation, and
	returns a graph where the keys are host or parasite nodes, and the values
	are a list of the children of a particular node. The graph represents 
	temporal relationships between events."""

	parents = parentsDict(HostTree, ParasiteTree)
	H = treeFormat(HostTree)
	P = treeFormat(ParasiteTree)
	reconGraph = H
	reconGraph.update(P) 
	for key in reconciliation:
		#deal with transfer case:
		if reconciliation[key][0] == 'T':
			reconGraph[key[0]] = P[key[0]] + [reconciliation[key][1][1], \
												reconciliation[key][2][1]]
			parent1 = parents[reconciliation[key][1][1]]
			parent2 = parents[reconciliation[key][2][1]]
			reconGraph[parent1] = reconGraph[parent1] + [key[0]]
			reconGraph[parent2] = reconGraph[parent2] + [key[0]]
		#deal with speciation case:
		elif reconciliation[key][0] == 'S':
			parent = parents[key[0]]
			if parent != 'Top':
				reconGraph[parent] = reconGraph[parent] + [key[1]]
			reconGraph[key[1]] = reconGraph[key[1]] + reconGraph[key[0]]

		#deal with duplication case:
		elif reconciliation[key][0] == 'D':
			parent = parents[key[1]]
			if parent != 'Top':
				reconGraph[parent] = reconGraph[parent] + [key[0]]
			reconGraph[key[0]] = reconGraph[key[0]] + [key[1]]
		#deal with contemporary case:
		elif reconciliation[key][0] == 'C':
			reconGraph[key[1]] = [None]
			reconGraph[key[0]] = [None]

	for key in reconGraph:
		reconGraph[key] = uniquify(reconGraph[key])

	return reconGraph













