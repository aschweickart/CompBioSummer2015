H = {('h6', 'h8'): ('h6', 'h8', ('h8', 'h3'), ('h8', 'h4')), ('h8', 'h3'):
('h8', 'h3', None, None), ('h6', 'h7'): ('h6', 'h7', ('h7', 'h1'), ('h7', 'h2')), 'hTop':
('Top', 'h6', ('h6', 'h7'), ('h6', 'h8')), ('h7', 'h2'): ('h7', 'h2', None, None), ('h8', 'h4'):
('h8', 'h4', None, None), ('h7', 'h1'): ('h7', 'h1', None, None)}


P = {('p8', 'p3'): ('p8', 'p3', None, None), 
('p6', 'p8'): ('p6', 'p8', ('p8', 'p2'), ('p8', 'p3')), 
'pTop': ('Top', 'p6', ('p6', 'p1'), ('p6', 'p8')), 
('p6', 'p1'): ('p6', 'p1', None, None), 
('p8', 'p2'): ('p8', 'p2', None, None)}

greedy = {('p8', 'h2'): ['T', ('p7', 'h2'), ('p5', 'h5')], 
('p4', 'h3'): ['C', (None, None), (None, None)], 
('p5', 'h5'): ['C', (None, None), (None, None)], 
('p2', 'h4'): ['C', (None, None), (None, None)], 
('p1', 'h1'): ['C', (None, None), (None, None)], 
('p3', 'h2'): ['C', (None, None), (None, None)], 
('p6', 'h1'): ['T', ('p1', 'h1'), ('p2', 'h4')], 
('p9', 'h6'): ['S', ('p6', 'h1'), ('p8', 'h2')], 
('p7', 'h2'): ['T', ('p3', 'h2'), ('p4', 'h3')]}

def InitDicts(tree):
	"""This function takes as input a tree dictionary and returns a dictionary with all of the bottom nodes 
	of the edges as keys and empty lists as values."""
	treeDict = {}
	parentDict = {}
	for key in tree:
		if key == 'pTop' or key == 'hTop':
			treeDict[key] = []
			parentDict[key] = tree[key][0]
		else:
			treeDict[key[1]] = []
			parentDict[key[1]] = tree[key][0]
	return treeDict, parentDict

def treeFormat(tree):
	"""Takes a tree in the format that it comes out of newickFormatReader and converts it into a dictionary
	with keys which are the bottom nodes of the edge and values which are the children."""

	treeDict, parentDict = InitDicts(tree)
	for key in tree:
		if key == 'pTop' or key == 'hTop':
			if tree[key][-2] == None:
				treeDict[key] = treeDict[key] + [tree[key][-2]]
			else:
				treeDict[key] = treeDict[key] + [tree[key][-2][1]]
			if tree[key][-1] == None:
				treeDict[key] = treeDict[key] + [tree[key][-1]]
			else:
				treeDict[key] = treeDict[key] + [tree[key][-1][1]]
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
			parentsDict[key] = H[key][0]
		else:
			parentsDict[key[1]] = H[key][0]
	for key in P:
		if key == 'pTop':
			parentsDict[key] = P[key][0]
		else:
			parentsDict[key[1]] = P[key][0]
	return parentsDict

def buildReconstruction(HostTree, ParasiteTree, reconciliation):
	""" """

	parents = parentsDict(HostTree, ParasiteTree)
	H = treeFormat(HostTree)
	P = treeFormat(ParasiteTree)
	reconGraph = H
	reconGraph.update(P) 
	for key in reconciliation:
		if reconciliation[key][0] == 'T':
			reconGraph[key[0]] = P[key[0]] + [reconciliation[key][1][1], reconciliation[key][2][1]]
			parent1 = parents[reconciliation[key][1][1]]
			parent2 = parents[reconciliation[key][2][1]]
			reconGraph[parent1] = reconGraph[parent1] + [reconciliation[key][1][1]]
			reconGraph[parent2] = reconGraph[parent2] + [reconciliation[key][2][1]]

		elif reconciliation[key][0] == 'S':
			parent = parents(key[0])
			reconGraph[parent] = reconGraph[parent] + [key[1]]
			reconGraph[key[1]] = reconGraph[key[1]] + reconGraph[key[0]]
			del reconGraph[key[0]]

		elif reconciliation[key][0] == 'D':
			parent = parents[key[1]]
			reconGraph[parent] = reconGraph[parent] + [key[0]]
			reconGraph[key[0]] = reconGraph[key[0]] + [key[1]]

		elif reconciliation[key][0] == 'C':
			reconGraph[key[1]] = ['tip']
	return reconGraph
















