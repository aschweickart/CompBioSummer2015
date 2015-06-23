# PROF WU VISUALIZATION RECONCILIATION FORMAT CONVERSION
def convert(reconciliation, DTL, ParasiteTree, outputFile, n):
	"""Takes as input a dictionary of a reconciliation between host and parasite trees, a DTL graph, and a string containing the name of a 
	file where it will put the output. The function outputs the same tree converted to brecon format. 
	Note that for losses, the parasite node in the brecon representation is the parent of the given parasite node. 
	This accounts for the brecon format's inability to handle losses"""
	
	D = {'T': 'trans', 'S': 'spec', 'D': 'dup', 'C': 'gene', 'L': 'loss'}
	f = open(outputFile + str(n) + ".mowgli.brecon", 'w')
	event = ""
	pParent = parasiteParentsDict(ParasiteTree)
	freqDict = frequencyDict(DTL, reconciliation)
	for key in reconciliation:
		freq = 0.55
		#if reconciliation[key][0] != 'L':
		event = reconciliation[key][0]
		f.write(key[0] + '\t' + key[1] + '\t' + D[event] + '\t' + str(freq) + '\n')
		#else:
		#	event = reconciliation[key][0]
		#	f.write(pParent[key[0]] + '\t' + key[1] + '\t' + D[event] + '\t' + str(freq) + '\n')
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

































