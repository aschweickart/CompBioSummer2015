# orderGraph.py
# Carter Slocum
# July 2015

# This file contains a function for topologically ordering a tree graph and detecting non-acyclic graphs


import copy


def date(recon):
	"""takes a Tree and returns a dictionary representation of the ordering of the tree. 
	If there is a cycle, the function returns None"""
	order = {}
	dicto = {}
	leaves = []
	lonerList = []

	#initialise the dictionary of in-degree's
	for key in recon:
		if  key != None:
			dicto[key] = 0
		for child in recon[key]:
			if child != None:
				dicto[child] = 0
			else:
				leaves.append(child)

	#find every Nodes' in-degree
	for key in dicto:
		for child in recon[key]:
			if child != None and child in dicto:
				dicto[child] += 1
	place = 0

	#Find RootNode
	for key in dicto:
		if key != None:
			if dicto[key] == 0:
				lonerList.append(key)
				del dicto[key]

	# While there is a 0 in-degree node, order it, remove it, and decrement the child nodes
	while lonerList:
		x = lonerList[0]
		order[x] = place
		place += 1
		del lonerList[0]
		for child in recon[x]:
			if child != None and child[0] != None and not child in leaves:
				if recon[child] != None:
					dicto[child] = dicto[child] - 1
					if dicto[child] == 0:
						lonerList.append(child)
						del dicto[child]

	# check for remaining nodes, if there are any, then there is a cycle
	if dicto:
		return None
	for item in leaves:
		order[item] = len(leaves)
	return order

	