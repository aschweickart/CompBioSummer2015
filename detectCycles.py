H = {('h2', 'h4'): ('h2', 'h4', None, None), 
('h3', 'h7'): ('h3', 'h7', None, None), 
('h1', 'h2'): ('h1', 'h2', ('h2', 'h4'), ('h2', 'h5')), 
('h1', 'h3'): ('h1', 'h3', ('h3', 'h6'), ('h3', 'h7')), 
'hTop': ('Top', 'h1', ('h1', 'h2'), ('h1', 'h3')), 
('h2', 'h5'): ('h2', 'h5', None, None), 
('h3', 'h6'): ('h3', 'h6', None, None)} 

P = {('p3', 'p7'): ('p3', 'p7', None, None), 
('p1', 'p2'): ('p1', 'p2', ('p2', 'p4'), ('p2', 'p5')), 
('p1', 'p3'): ('p1', 'p3', ('p3', 'p6'), ('p3', 'p7')), 
('p3', 'p6'): ('p3', 'p6', None, None), 
('p2', 'p4'): ('p2', 'p4', None, None), 
('p2', 'p5'): ('p2', 'p5', None, None), 
'pTop': ('Top', 'p1', ('p1', 'p2'), ('p1', 'p3'))}

phi = {'p6': 'h4', 'p7': 'h6', 'p4': 'h5', 'p5': 'h7'}

DTL = {('p3', 'h6'): [['T', ('p7', 'h6'), ('p6', 'h4'), 0.5], 1], 
('p2', 'h5'): [['T', ('p4', 'h5'), ('p5', 'h7'), 0.5], 1], 
('p2', 'h7'): [['T', ('p5', 'h7'), ('p4', 'h5'), 0.5], 1], 
('p7', 'h6'): [['C', (None, None), (None, None), 1.0], 0], 
('p5', 'h7'): [['C', (None, None), (None, None), 1.0], 0], 
('p3', 'h4'): [['T', ('p6', 'h4'), ('p7', 'h6'), 0.5], 1], 
('p6', 'h4'): [['C', (None, None), (None, None), 1.0], 0], 
('p1', 'h2'): [['S', ('p3', 'h4'), ('p2', 'h5'), 0.5], 2], 
('p1', 'h3'): [['S', ('p3', 'h6'), ('p2', 'h7'), 0.5], 2], 
('p4', 'h5'): [['C', (None, None), (None, None), 1.0], 0]}

R = {('p1', 'h1'): ['S', ('p3', 'h3'), ('p2', 'h2')], 
('p2', 'h2'): ['L', ('p2', 'h5'), (None, None)],
('p3', 'h3'): ['L', ('p3', 'h6'), (None, None)], 
('p3', 'h6'): ['T', ('p7', 'h6'), ('p6', 'h2')], 
('p6', 'h2'): ['L', ('p6', 'h4'), (None, None)], 
('p2', 'h5'): ['T', ('p4', 'h5'), ('p5', 'h3')], 
('p5', 'h3'): ['L', ('p5', 'h7'), (None, None)], 
('p6', 'h4'): ['C', (None, None), (None, None)],
('p4', 'h5'): ['C', (None, None), (None, None)],
('p7', 'h6'): ['C', (None, None), (None, None)],
('p5', 'h7'): ['C', (None, None), (None, None)]}

def findRoot(Tree):
	"""This function takes in a tree and returns a string with the name of the root vertex of the tree"""

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

def parentsDict(H, P):
	"""Takes a host and a parasite tree with edges as keys and returns a dictionary with 
	keys which are the bottom nodes of those edges and values which are the top nodes of 
	those edges."""

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
	"""Takes as input a list and returns a list containing only the unique elements of 
	the input list."""

	keys = {}
	for e in list:
		keys[e] = 1
	return keys.keys()

def buildReconciliation(HostTree, ParasiteTree, reconciliation):
	"""Takes as input a host tree, a parasite tree, and a reconciliation, and returns a graph where the
	keys are host or parasite nodes, and the values are a list of the children of a particular node. The
	graph represents temporal relationships between events."""

	parents = parentsDict(HostTree, ParasiteTree)
	H = treeFormat(HostTree)
	P = treeFormat(ParasiteTree)
	reconGraph = H
	reconGraph.update(P) 
	transferList = []
	for key in reconciliation:
		print "key:", key
		if reconciliation[key][0] == 'T':
			reconGraph[key[0]] = P[key[0]] + [reconciliation[key][1][1], reconciliation[key][2][1]]
			parent1 = parents[reconciliation[key][1][1]]
			parent2 = parents[reconciliation[key][2][1]]
			reconGraph[parent1] = reconGraph[parent1] + [key[0]]
			reconGraph[parent2] = reconGraph[parent2] + [key[0]]
			transferEdge = reconciliation[key][1][1]
			print "key[1]:", key[1]
			print "transferEdge:", transferEdge
			if transferEdge == key[1]:
				transferEdge = reconciliation[key][2][1]
				print "iftransferedge:", transferEdge
				transferList.append([key[0], parent1, transferEdge])
			else:
				transferList.append([key[0], parent2, transferEdge])
			print transferList

		elif reconciliation[key][0] == 'S':
			parent = parents[key[0]]
			if parent != 'Top':
				reconGraph[parent] = reconGraph[parent] + [key[1]]
			reconGraph[key[1]] = reconGraph[key[1]] + reconGraph[key[0]]
			#del reconGraph[key[0]]

		elif reconciliation[key][0] == 'D':
			parent = parents[key[1]]
			if parent != 'Top':
				reconGraph[parent] = reconGraph[parent] + [key[0]]
			reconGraph[key[0]] = reconGraph[key[0]] + [key[1]]

		elif reconciliation[key][0] == 'C':
			reconGraph[key[1]] = [None]
			reconGraph[key[0]] = [None]

	for key in reconGraph:
		reconGraph[key] = uniquify(reconGraph[key])

	return reconGraph, transferList

#transferList = [['p3', 'h3', 'h2'], ['p2', 'h2', 'h3']]
reconGraph = {'p2': ['h3', 'h5', 'p4', 'p5'], 
'p3': ['h2', 'h6', 'p6', 'p7'], 
'p1': ['p2', 'p3'], 
'p6': [None], 'p7': [None], 'p4': [None], 'p5': [None], 
'h2': ['p2', 'h4', 'h5'], 
'h3': ['p3', 'h6', 'h7'], 
'h1': ['h2', 'h3', 'p2', 'p3'], 
'h6': [None], 'h7': [None], 'h4': [None], 'h5': [None]}

# def initMarkingDict(reconGraph):
# 	"""This function takes as input the cycle checking graph, reconGraph and returns markingDict, a dictionary that
# 	keeps track of all the childNodes that are marked and their parents"""
# 	markingDict = {}
# 	for key in reconGraph:
# 		markingDict[key] = []
# 	return markingDict

markingDict = {'p2': 'p1', 'p3': 'h3', 'p1': 'root', 'p6': 'p3', 'p7': 'p3', 'p4': 'p2', 'p5': 'p2', 'h2': 'p3', 'h3': 'p2', 'h1': 'root', 'h6': 'p3', 'h5': 'p2'}

def detectCycles(reconGraph, H, P):
	"""This function takes as input the cycle checking graph, reconGraph, and returns a new reconGraph where the cycles
	are removed and also keeps track of where the transfers occurred in the reconciliation."""
	markingDict = {}
	#stack = []
	Proot = findRoot(P)
	Hroot = findRoot(H)
	#stack.append([P, H])
	markingDict[Proot] = 'root'
	markingDict[Hroot] = 'root'
	#recurseChildren(reconGraph, markingDict, Proot)
	recurseChildren(reconGraph, markingDict, Hroot)
	return markingDict


def recurseChildren(reconGraph, markingDict, node):
	"""This function takes as input reconGraph, the cycle checking graph, markingDict, a dictionary that keeps track
	of all the childNodes that are marked, and childNode, the node that we will recurse on. It returns an updated 
	markingDict if there are no cycles, or"""
	print "node:", node
	for child in reconGraph[node]:
		print "child:", child
		if child not in markingDict and child != None:
			markingDict[child] = node
			print "markingDict[child]/node:", node
			childDict = recurseChildren(reconGraph, markingDict, child)
			print "childDict:", childDict
			if childDict is type(dict):
				markingDict.update(childDict)
		elif child != None:
			return "cycle detected!!!!!!!:", child
		print "markingDict:", markingDict
	return markingDict

def deleteTransfer(reconGraph, markingDict, transferList):
	""" """


























	

