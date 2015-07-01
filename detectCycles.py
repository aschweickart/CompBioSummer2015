# H = {('h2', 'h4'): ('h2', 'h4', None, None), 
# ('h3', 'h7'): ('h3', 'h7', None, None), 
# ('h1', 'h2'): ('h1', 'h2', ('h2', 'h4'), ('h2', 'h5')), 
# ('h1', 'h3'): ('h1', 'h3', ('h3', 'h6'), ('h3', 'h7')), 
# 'hTop': ('Top', 'h1', ('h1', 'h2'), ('h1', 'h3')), 
# ('h2', 'h5'): ('h2', 'h5', None, None), 
# ('h3', 'h6'): ('h3', 'h6', None, None)} 

# P = {('p3', 'p7'): ('p3', 'p7', None, None), 
# ('p1', 'p2'): ('p1', 'p2', ('p2', 'p4'), ('p2', 'p5')), 
# ('p1', 'p3'): ('p1', 'p3', ('p3', 'p6'), ('p3', 'p7')), 
# ('p3', 'p6'): ('p3', 'p6', None, None), 
# ('p2', 'p4'): ('p2', 'p4', None, None), 
# ('p2', 'p5'): ('p2', 'p5', None, None), 
# 'pTop': ('Top', 'p1', ('p1', 'p2'), ('p1', 'p3'))}

# phi = {'p6': 'h4', 'p7': 'h6', 'p4': 'h5', 'p5': 'h7'}

# DTL = {('p3', 'h6'): [['T', ('p7', 'h6'), ('p6', 'h4'), 0.5], 1], 
# ('p2', 'h5'): [['T', ('p4', 'h5'), ('p5', 'h7'), 0.5], 1], 
# ('p2', 'h7'): [['T', ('p5', 'h7'), ('p4', 'h5'), 0.5], 1], 
# ('p7', 'h6'): [['C', (None, None), (None, None), 1.0], 0], 
# ('p5', 'h7'): [['C', (None, None), (None, None), 1.0], 0], 
# ('p3', 'h4'): [['T', ('p6', 'h4'), ('p7', 'h6'), 0.5], 1], 
# ('p6', 'h4'): [['C', (None, None), (None, None), 1.0], 0], 
# ('p1', 'h2'): [['S', ('p3', 'h4'), ('p2', 'h5'), 0.5], 2], 
# ('p1', 'h3'): [['S', ('p3', 'h6'), ('p2', 'h7'), 0.5], 2], 
# ('p4', 'h5'): [['C', (None, None), (None, None), 1.0], 0]}

# R = {('p1', 'h1'): ['S', ('p3', 'h3'), ('p2', 'h2')], 
# ('p2', 'h2'): ['L', ('p2', 'h5'), (None, None)],
# ('p3', 'h3'): ['L', ('p3', 'h6'), (None, None)], 
# ('p3', 'h6'): ['T', ('p7', 'h6'), ('p6', 'h2')], 
# ('p6', 'h2'): ['L', ('p6', 'h4'), (None, None)], 
# ('p2', 'h5'): ['T', ('p4', 'h5'), ('p5', 'h3')], 
# ('p5', 'h3'): ['L', ('p5', 'h7'), (None, None)], 
# ('p6', 'h4'): ['C', (None, None), (None, None)],
# ('p4', 'h5'): ['C', (None, None), (None, None)],
# ('p7', 'h6'): ['C', (None, None), (None, None)],
# ('p5', 'h7'): ['C', (None, None), (None, None)]}

H = {('h2', 'h4'): ('h2', 'h4', ('h4', 'h8'), ('h4', 'h9')), 
('h7', 'h14'): ('h7', 'h14', None, None), 
('h3', 'h6'): ('h3', 'h6', ('h6', 'h12'), ('h6', 'h13')), 
('h3', 'h7'): ('h3', 'h7', ('h7', 'h14'), ('h7', 'h15')), 
('h1', 'h2'): ('h1', 'h2', ('h2', 'h4'), ('h2', 'h5')), 
('h1', 'h3'): ('h1', 'h3', ('h3', 'h6'), ('h3', 'h7')), 
('h5', 'h10'): ('h5', 'h10', None, None), 
'hTop': ('Top', 'h1', ('h1', 'h2'), ('h1', 'h3')), 
('h6', 'h13'): ('h6', 'h13', None, None), 
('h5', 'h11'): ('h5', 'h11', None, None), 
('h4', 'h9'): ('h4', 'h9', None, None), 
('h6', 'h12'): ('h6', 'h12', None, None), 
('h4', 'h8'): ('h4', 'h8', None, None), 
('h2', 'h5'): ('h2', 'h5', ('h5', 'h10'), ('h5', 'h11')), 
('h7', 'h15'): ('h7', 'h15', None, None)} 

P = {('p1', 'p3'): ('p1', 'p3', ('p3', 'p6'), ('p3', 'p7')), 
('p6', 'p13'): ('p6', 'p13', None, None), 
('p3', 'p7'): ('p3', 'p7', ('p7', 'p14'), ('p7', 'p15')), 
('p1', 'p2'): ('p1', 'p2', ('p2', 'p4'), ('p2', 'p5')), 
('p6', 'p12'): ('p6', 'p12', None, None), 
('p4', 'p9'): ('p4', 'p9', None, None), 
('p4', 'p8'): ('p4', 'p8', None, None), 
('p2', 'p5'): ('p2', 'p5', ('p5', 'p10'), ('p5', 'p11')), 
('p2', 'p4'): ('p2', 'p4', ('p4', 'p8'), ('p4', 'p9')), 
('p7', 'p14'): ('p7', 'p14', None, None), 
('p5', 'p10'): ('p5', 'p10', None, None), 
('p3', 'p6'): ('p3', 'p6', ('p6', 'p12'), ('p6', 'p13')), 
('p5', 'p11'): ('p5', 'p11', None, None), 
'pTop': ('Top', 'p1', ('p1', 'p2'), ('p1', 'p3')), 
('p7', 'p15'): ('p7', 'p15', None, None)} 

phi = {'p8': 'h9', 'p9': 'h11', 'p10': 'h8', 'p11': 'h10', 'p12': 'h13', 'p13': 'h15', 'p14': 'h12', 'p15': 'h14'}

R = {('p1', 'h1'): ['S', ('p2', 'h2'), ('p3', 'h3')], 
('p2', 'h2'): ['S', ('p4', 'h4'), ('p5', 'h5')], 
('p4', 'h4'): ['L', ('p4', 'h9'), (None, None)], 
('p4', 'h9'): ['T', ('p8', 'h9'), ('p9', 'h5')], 
('p9', 'h5'): ['L', ('p9', 'h11'), (None, None)], 
('p5', 'h5'): ['L', ('p5', 'h10'), (None, None)], 
('p5', 'h10'): ['T', ('p11', 'h10'), ('p10', 'h4')], 
('p10', 'h4'): ['L', ('p10', 'h8'), (None, None)], 
('p3', 'h3'): ['S', ('p6', 'h6'), ('p7', 'h7')], 
('p6', 'h6'): ['L', ('p6', 'h13'), (None, None)], 
('p6', 'h13'): ['T', ('p12', 'h13'), ('p13', 'h7')], 
('p13', 'h7'): ['L', ('p13', 'h15'), (None, None)], 
('p7', 'h7'): ['L', ('p7', 'h14'), (None, None)], 
('p7', 'h14'): ['T', ('p15', 'h14'), ('p14', 'h6')], 
('p14', 'h6'): ['L', ('p14', 'h12'), (None, None)],
('p10', 'h8'): ['C', (None, None), (None, None)], 
('p8', 'h9'): ['C', (None, None), (None, None)], 
('p11', 'h10'): ['C', (None, None), (None, None)], 
('p9', 'h11'): ['C', (None, None), (None, None)], 
('p14', 'h12'): ['C', (None, None), (None, None)], 
('p12', 'h13'): ['C', (None, None), (None, None)], 
('p15', 'h14'): ['C', (None, None), (None, None)], 
('p13', 'h15'): ['C', (None, None), (None, None)]}




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
		if reconciliation[key][0] == 'T':
			reconGraph[key[0]] = P[key[0]] + [reconciliation[key][1][1], reconciliation[key][2][1]]
			parent1 = parents[reconciliation[key][1][1]]
			parent2 = parents[reconciliation[key][2][1]]
			reconGraph[parent1] = reconGraph[parent1] + [key[0]]
			reconGraph[parent2] = reconGraph[parent2] + [key[0]]
			transferEdge = reconciliation[key][1][1]
			if transferEdge == key[1]:
				transferEdge = reconciliation[key][2][1]
				transferList.append([key[0], parent1, transferEdge])
			else:
				transferList.append([key[0], parent2, transferEdge])

		elif reconciliation[key][0] == 'S':
			parent = parents[key[0]]
			if parent != 'Top':
				reconGraph[parent] = reconGraph[parent] + [key[1]]
			reconGraph[key[1]] = reconGraph[key[1]] + reconGraph[key[0]]

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

transferList = [['p3', 'h3', 'h2'], ['p2', 'h2', 'h3']]
reconGraph = {'p2': ['h3', 'h5', 'p4', 'p5'], 
'p3': ['h2', 'h6', 'p6', 'p7'], 
'p1': ['p2', 'p3'], 
'p6': [None], 'p7': [None], 'p4': [None], 'p5': [None], 
'h2': ['p2', 'h4', 'h5'], 
'h3': ['p3', 'h6', 'h7'], 
'h1': ['h2', 'h3', 'p2', 'p3'], 
'h6': [None], 'h7': [None], 'h4': [None], 'h5': [None]}


markingDict = {'p2': 'p1', 'p3': 'h3', 'p1': 'root', 'p6': 'p3', 'p7': 'p3', 'p4': 'p2', 'p5': 'p2', 'h2': 'p3', 'h3': 'p2', 'h1': 'root', 'h6': 'p3', 'h5': 'p2'}

def detectCycles(HostTree, ParasiteTree, reconciliation):
	"""This function takes as input the cycle checking graph, reconGraph, and returns a new reconGraph where the cycles
	are removed and also keeps track of where the transfers occurred in the reconciliation."""
	markingDict = {}
	reconGraph, transferList = buildReconciliation(H, P, R)
	Hroot = findRoot(H)
	markingDict[Hroot] = ['root', 'tick']
	markingDict, cycleNode = recurseChildren(reconGraph, markingDict, Hroot, [])
	newReconGraph = deleteTransfer(reconGraph, markingDict, transferList, cycleNode)
	while cycleNode != []:
		markingDict, cycleNode = recurseChildren(newReconGraph, {Hroot: ['root', 'tick']}, Hroot, [])
		newReconGraph = deleteTransfer(newReconGraph, markingDict, transferList, cycleNode)

	return newReconGraph


def recurseChildren(reconGraph, markingDict, node, cycleNode):
	"""This function takes as input reconGraph, the cycle checking graph, markingDict, a dictionary that keeps track
	of all the childNodes that are marked, node, the node that we will recurse on, and cycleList, 
	which keeps track of cycles that it finds. It returns an updated markingDict and cycleList"""
	if cycleNode != []:
		return
	for child in reconGraph[node]:
		if child in markingDict and len(markingDict[child]) == 2:
			cycleNode = cycleNode + [child]
			return cycleNode
		elif child not in markingDict and child != None:
			markingDict[child] = [node, 'tick']
			childDict = recurseChildren(reconGraph, markingDict, child, cycleNode)
			markingDict[child] = [node]
			if childDict is type(dict):
				markingDict.update(childDict)
	return markingDict, cycleNode

def deleteTransfer(reconGraph, markingDict, transferList, cycleNode):
	"""This function takes as input the cycle checking graph, markingDict, transferList, and cycleNode, and 
	returns the updated cycle checking graph with the guilty transfers removed."""
	if cycleNode == []:
		return reconGraph
	for transfer in transferList:
		if cycleNode[0] in transfer:
			childList = reconGraph[transfer[1]]
			childList.remove(transfer[0])
			reconGraph[transfer[1]] = childList
			childList = reconGraph[transfer[0]]
			childList.remove(transfer[2])
			reconGraph[transfer[0]] = childList
			break
	return reconGraph



reconGraph2 = {'h8': [None], 'h9': [None], 'h2': ['p5', 'p4', 'h4', 'h5'], 'h3': ['p6', 'h6', 'h7', 'p7'], 'h1': ['h2', 'h3', 'p2', 'p3'], 'h6': ['h12', 'h13'], 'h7': ['h14', 'h15', 'p7'], 'h4': ['h8', 'h9', 'p4'], 'h5': ['h10', 'h11'], 'p10': [None], 'p11': [None], 'p12': [None], 'p13': [None], 'p14': [None], 'p15': [None], 'p2': ['p4', 'p5'], 'p3': ['p6', 'p7'], 'p1': ['p2', 'p3', 'h2', 'h3'], 'p6': ['p12', 'p13', 'h13'], 'p7': ['h14', 'p14', 'p15', 'h6'], 'p4': ['h9', 'p8', 'p9', 'h5'], 'p5': ['p10', 'p11', 'h10'], 'h10': [None], 'h11': [None], 'h12': [None], 'h13': [None], 'h14': [None], 'h15': [None], 'p9': [None], 'p8': [None]}
reconGraph1 = {'h8': [None], 'h9': [None], 'h2': ['p5', 'p4', 'h4', 'h5'], 'h3': ['p6', 'h6', 'h7', 'p7'], 'h1': ['h2', 'h3', 'p2', 'p3'], 'h6': ['h12', 'h13', 'p6'], 'h7': ['h14', 'h15', 'p7'], 'h4': ['h8', 'h9', 'p4'], 'h5': ['h10', 'h11'], 'p10': [None], 'p11': [None], 'p12': [None], 'p13': [None], 'p14': [None], 'p15': [None], 'p2': ['p4', 'p5'], 'p3': ['p6', 'p7'], 'p1': ['p2', 'p3', 'h2', 'h3'], 'p6': ['p12', 'p13', 'h13', 'h7'], 'p7': ['h14', 'p14', 'p15', 'h6'], 'p4': ['h9', 'p8', 'p9', 'h5'], 'p5': ['p10', 'p11', 'h10'], 'h10': [None], 'h11': [None], 'h12': [None], 'h13': [None], 'h14': [None], 'h15': [None], 'p9': [None], 'p8': [None]}
reconGraphOrig = {'h8': [None], 'h9': [None], 'h2': ['p5', 'p4', 'h4', 'h5'], 'h3': ['p6', 'h6', 'h7', 'p7'], 'h1': ['h2', 'h3', 'p2', 'p3'], 'h6': ['h12', 'h13', 'p6'], 'h7': ['h14', 'h15', 'p7'], 'h4': ['h8', 'h9', 'p4'], 'h5': ['h10', 'h11', 'p5'], 'p10': [None], 'p11': [None], 'p12': [None], 'p13': [None], 'p14': [None], 'p15': [None], 'p2': ['p4', 'p5'], 'p3': ['p6', 'p7'], 'p1': ['p2', 'p3', 'h2', 'h3'], 'p6': ['p12', 'p13', 'h13', 'h7'], 'p7': ['h14', 'p14', 'p15', 'h6'], 'p4': ['h9', 'p8', 'p9', 'h5'], 'p5': ['p10', 'p11', 'h10', 'h4'], 'h10': [None], 'h11': [None], 'h12': [None], 'h13': [None], 'h14': [None], 'h15': [None], 'p9': [None], 'p8': [None]}

transferList = [['p4', 'h4', 'h5'], ['p6', 'h6', 'h7'], ['p5', 'h5', 'h4'], ['p7', 'h7', 'h6']]


























	

