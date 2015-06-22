H = {('h6', 'h8'): ('h6', 'h8', ('h8', 'h3'), ('h8', 'h4')), 
('h8', 'h3'): ('h8', 'h3', None, None), 
('h6', 'h7'): ('h6', 'h7', ('h7', 'h1'), ('h7', 'h2')), 
'hTop': ('Top', 'h6', ('h6', 'h7'), ('h6', 'h8')), 
('h7', 'h2'): ('h7', 'h2', None, None), 
('h8', 'h4'): ('h8', 'h4', None, None), 
('h7', 'h1'): ('h7', 'h1', None, None)}


P = {('p6', 'p8'): ('p6', 'p8', ('p8', 'p3'), ('p8', 'p4')), 
('p7', 'p2'): ('p7', 'p2', None, None),
('p6', 'p7'): ('p6', 'p7', ('p7', 'p1'), ('p7', 'p2')), 
('p8', 'p4'): ('p8', 'p4', None, None),
('p8', 'p3'): ('p8', 'p3', None, None), 
'pTop': ('Top', 'p6', ('p6', 'p7'), ('p6', 'p8')), 
('p7', 'p1'): ('p7', 'p1', None, None)}

R = {('p8', 'h2'): ['T', ('p3', 'h2'), ('p4', 'h4')], 
('p7', 'h1'): ['T', ('p1', 'h1'), ('p2', 'h3')], 
('p1', 'h1'): ['C', (None, None), (None, None)], 
('p6', 'h7'): ['S', ('p7', 'h1'), ('p8', 'h2')], 
('p3', 'h2'): ['C', (None, None), (None, None)], 
('p2', 'h3'): ['C', (None, None), (None, None)], 
('p4', 'h4'): ['C', (None, None), (None, None)]}

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

def buildReconstruction(HostTree, ParasiteTree, reconciliation):
	"""Takes as input a host tree, a parasite tree, and a reconciliation, and returns a graph where the
	keys are host or parasite nodes, and the values are a list of the children of a particular node. The
	graph represents temporal relationships between events."""

	parents = parentsDict(HostTree, ParasiteTree)
	H = treeFormat(HostTree)
	P = treeFormat(ParasiteTree)
	reconGraph = H
	reconGraph.update(P) 
	for key in reconciliation:
		print "key:", key
		if reconciliation[key][0] == 'T':
			reconGraph[key[0]] = P[key[0]] + [reconciliation[key][1][1], reconciliation[key][2][1]]
			parent1 = parents[reconciliation[key][1][1]]
			parent2 = parents[reconciliation[key][2][1]]
			reconGraph[parent1] = reconGraph[parent1] + [key[0]]
			reconGraph[parent2] = reconGraph[parent2] + [key[0]]

		elif reconciliation[key][0] == 'S':
			parent = parents[key[0]]
			if parent != 'Top':
				reconGraph[parent] = reconGraph[parent] + [key[1]]
			reconGraph[key[1]] = reconGraph[key[1]] + reconGraph[key[0]]
			del reconGraph[key[0]]

		elif reconciliation[key][0] == 'D':
			parent = parents[key[1]]
			reconGraph[parent] = reconGraph[parent] + [key[0]]
			reconGraph[key[0]] = reconGraph[key[0]] + [key[1]]

		elif reconciliation[key][0] == 'C':
			reconGraph[key[1]] = [None]
			reconGraph[key[0]] = [None]

	for key in reconGraph:
		reconGraph[key] = uniquify(reconGraph[key])

	return reconGraph













