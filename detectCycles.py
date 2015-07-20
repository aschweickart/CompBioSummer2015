# detectCycles.py
# Juliet Forman and Srinidhi Srinivasan
# July 2015

# This file contains functions for detecting and marking temporal 
# inconsistencies in reconciliattions. It uses depth first search to find 
# cycles in graphs that represent temporal relationships between nodes in the 
# parasite and host trees. When temporal inconsistencies are found, the 
# reconciliation is updated to mark which transfers are guilty of causing
# temporal inconsistencies. The main function in this file is 
# detectCyclesWrapper, and the rest of the functions are helper functions 
# that are used by detectCyclesWrapper.
import ReconciliationGraph
import copy

def buildReconciliation(HostTree, ParasiteTree, reconciliation):
	"""Takes as input a host tree, a parasite tree, and a reconciliation, 
	and returns a graph where the keys are host or parasite nodes, and the 
	values are a list of the children of a particular node. The graph 
	represents temporal relationships between events."""

	parents = ReconciliationGraph.parentsDict(HostTree, ParasiteTree)
	H = ReconciliationGraph.treeFormat(HostTree)
	P = ReconciliationGraph.treeFormat(ParasiteTree)
	reconGraph = H
	reconGraph.update(P) 
	transferList = []
	for key in reconciliation:
		if reconciliation[key][0] == 'T':
			reconGraph[key[0]] = P[key[0]] + [reconciliation[key][1][1], \
				reconciliation[key][2][1]]
			parent1 = parents[reconciliation[key][1][1]]
			parent2 = parents[reconciliation[key][2][1]]
			reconGraph[parent1] = reconGraph[parent1] + [key[0]]
			reconGraph[parent2] = reconGraph[parent2] + [key[0]]
			transferEdge1 = reconciliation[key][1][1]
			transferEdge2 = reconciliation[key][2][1]
			transferList.append([key[0], parent1, transferEdge1, parent2, \
				transferEdge2])

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
		reconGraph[key] = ReconciliationGraph.uniquify(reconGraph[key])

	return reconGraph, transferList

def detectCycles(HostTree, ParasiteTree, reconciliation):
	"""This function takes as input the cycle checking graph, reconGraph. 
	It returns a new version of reconGraph, newReconGraph, from which the 
	transfer events responsible for the cycles have been removed. It also 
	returns a list, guiltyTransferList, of the guilty transfers."""
	hostTree = ReconciliationGraph.treeFormat(HostTree)
	parasiteTree = ReconciliationGraph.treeFormat(ParasiteTree)
	guiltyTransferList = []
	markingDict = {}
	reconGraph, transferList = buildReconciliation(HostTree, ParasiteTree, \
		reconciliation)
	Hroot = ReconciliationGraph.findRoot(HostTree)
	markingDict[Hroot] = ['check']
	cycleNode = recurseChildren(reconGraph, markingDict, Hroot, parasiteTree)
	markingDict = {}
	newReconGraph, guiltyTransfer, transferList = deleteTransfer(reconGraph, \
		transferList, cycleNode)
	if guiltyTransfer != []:
		guiltyTransferList.append(guiltyTransfer)
	while cycleNode != None:
		markingDict = {Hroot: ['check']}
		cycleNode = recurseChildren(newReconGraph, markingDict, Hroot, parasiteTree)
		if cycleNode == None:  
			for node in newReconGraph:
				if not checked(markingDict, node):
					check(markingDict, node)
					cycleNode = recurseChildren(newReconGraph, markingDict, node, parasiteTree)
		newReconGraph, guiltyTransfer, transferList = deleteTransfer(\
			newReconGraph, transferList, cycleNode)
		if guiltyTransfer != []:
			guiltyTransferList.append(guiltyTransfer)
	return newReconGraph, guiltyTransferList, newReconGraph


def checked(markingDict, node):
	"""This function takes as input a markingDict and a node, and checks the 
	node in markingDict, marking it as visited."""

	return node in markingDict and 'check' in markingDict[node]


def ticked(markingDict, node):
	"""This function takes as input a markingDict and a checked node, and 
	returns True if the node is already ticked, False if it is not."""

	return node in markingDict and 'tick' in markingDict[node]


def tick(markingDict, node):
	"""This function takes as input a markingDict and node which is checked 
	but not ticked, and ticks the node in markingDict."""

	markingDict[node] = markingDict[node] + ['tick']


def untick(markingDict, node):
	"""This function takes as input a markingDict and a ticked node, and 
	unticks the node in markingDict."""

	markingDict[node] = markingDict[node][:1]


def check(markingDict, node):
	"""This function takes as input markingDict and a node, and checks the 
	node in markingDict."""
	markingDict[node] = ['check']


def recurseChildren(reconGraph, markingDict, node, parasiteTree):
	"""This function takes as input the cycle checking graph reconGraph, 
	markingDict, a dictionary that keeps track of all the childNodes that are 
	marked or ticked, and node, the node that we will recurse on. The 
	function updates markingDict and returns the name of a node it finds is 
	in a cycle, or None if it finds no cycles."""

	tick(markingDict, node)
	for child in reconGraph[node]:
		if not checked(markingDict, child) and child != None:
			check(markingDict, child)
			cycleNode = recurseChildren(reconGraph, markingDict, child, parasiteTree)

			if cycleNode != None:
				return cycleNode

		elif child != None and ticked(markingDict, child):
			if child in parasiteTree:
				return child

	untick(markingDict, node)

	return None


def deleteTransfer(newReconGraph, transferList, cycleNode):
	"""This function takes as input the cycle checking graph reconGraph, a 
	dictionary markingDict, a list transferList of all transfers in the 
	reconciliation, and a node cycleNode which is either a node in a cycle or 
	None. The function returns a new cycle checking graph newReconGraph, 
	from which the guilty transfers have been removed."""
	guiltyTransfer = []
	if cycleNode == None:
		return newReconGraph, guiltyTransfer, transferList
	for transfer in transferList:
		if cycleNode in transfer:
			guiltyTransfer = transfer
			transferList.remove(transfer)
			removeChild(newReconGraph, transfer[1], transfer[0])
			removeChild(newReconGraph, transfer[0], transfer[2])
			removeChild(newReconGraph, transfer[0], transfer[4])
			if transfer[1] != transfer[3]:
				removeChild(newReconGraph, transfer[3], transfer[0])
			break
	return newReconGraph, guiltyTransfer, transferList


def removeChild(reconGraph, parent, child):
	"""This function takes as input a graph reconGraph, a parent, and its 
	child. It removes the child from the list of children that is the value 
	associated with parent in reconGraph."""
	
	childList = reconGraph[parent]
	childList.remove(child)
	reconGraph[parent] = childList


def updateReconciliation(guiltyTransferList, HostTree, ParasiteTree, \
		reconciliation):
	"""This function takes as input a list guiltyTransferList of transfers 
	that are responsible for cycles, a host tree and parasite tree, and the 
	original reconciliation of host and parasite. It returns a new 
	reconciliation in which all of the guilty transfers have been marked as a 
	new event 'GT'."""
	parents = ReconciliationGraph.parentsDict(HostTree, ParasiteTree)
	newReconciliation = copy.deepcopy(reconciliation)
	for transfer in guiltyTransferList:
		for key in newReconciliation.keys():
			if reconciliation[key][0] == 'T':
				if transfer[0] == key[0]:
					newReconciliation[key] = ['GT'] + reconciliation[key][1:]
	return newReconciliation


def detectCyclesWrapper(HostTree, ParasiteTree, reconciliation):
	"""This function takes in a host tree, parasite tree, and reconciliation, 
	and returns a new reconciliation where the guilty transfers have been 
	marked."""

	markingDict = {}
	newReconGraph, guiltyTransferList, newRec = detectCycles(HostTree, ParasiteTree, \
		reconciliation)
	newReconciliation = updateReconciliation(guiltyTransferList, HostTree, \
		ParasiteTree, reconciliation)
	return newReconciliation, newRec
