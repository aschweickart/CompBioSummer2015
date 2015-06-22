# PROF WU VISUALIZATION RECONCILIATION FORMAT CONVERSION
def convert(reconciliation, DTL, ParasiteTree, outputFile):
	"""Takes as input a dictionary of a reconciliation between host and parasite trees, a DTL graph, and a string containing the name of a 
	file where it will put the output. The function outputs the same tree converted to brecon format. 
	Note that for losses, the parasite node in the brecon representation is the parent of the given parasite node. 
	This accounts for the brecon format's inability to handle losses"""
	
	D = {'T': 'trans', 'S': 'spec', 'D': 'dup', 'C': 'gene', 'L': 'loss'}
	f = open(outputFile + ".mowgli.brecon", 'w') 
	event = ""
	pParent = parasiteParentsDict(ParasiteTree)
	freqDict = frequencyDict(DTL, reconciliation)
	for key in reconciliation:
		if reconciliation[key][0] != 'L':
			event = reconciliation[key][0]
			f.write(key[0] + '\t' + key[1] + '\t' + D[event] + '\t' + str(freqDict[key]) + '\n')
		else:
			event = reconciliation[key][0]
			f.write(pParent[key[0]] + '\t' + key[1] + '\t' + D[event] + '\t' + str(freqDict[key]) + '\n')
	f.close()

def frequencyDict(DTL, reconciliation):
	"""Takes as input a DTL graph and a reconciliation graph and ouputs a dictionary with DTL verteces as keys
	and their frequencies as values."""

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




DTL = {('p8', 'h2'): [['T', ('p3', 'h2'), ('p4', 'h4'), 1], 1], 
('p7', 'h1'): [['T', ('p1', 'h1'), ('p2', 'h3'), 1], 1], 
('p1', 'h1'): [['C', (None, None), (None, None), 1], 0], 
('p6', 'h7'): [['S', ('p7', 'h1'), ('p8', 'h2'), 1], 2], 
('p3', 'h2'): [['C', (None, None), (None, None), 1], 0], 
('p8', 'h4'): [['T', ('p4', 'h4'), ('p3', 'h2'), 1], 1], 
('p2', 'h3'): [['C', (None, None), (None, None), 1], 0], 
('p6', 'h8'): [['S', ('p7', 'h3'), ('p8', 'h4'), 1], 2], 
('p7', 'h3'): [['T', ('p2', 'h3'), ('p1', 'h1'), 1], 1], 
('p4', 'h4'): [['C', (None, None), (None, None), 1], 0]}

R = {('p8', 'h2'): ['T', ('p3', 'h2'), ('p4', 'h4')], 
('p7', 'h1'): ['T', ('p1', 'h1'), ('p2', 'h3')], 
('p1', 'h1'): ['C', (None, None), (None, None)], 
('p6', 'h7'): ['S', ('p7', 'h1'), ('p8', 'h2')], 
('p3', 'h2'): ['C', (None, None), (None, None)], 
('p2', 'h3'): ['C', (None, None), (None, None)], 
('p4', 'h4'): ['C', (None, None), (None, None)]}

P = {('p6', 'p8'): ('p6', 'p8', ('p8', 'p3'), ('p8', 'p4')), 
('p7', 'p2'): ('p7', 'p2', None, None),
('p6', 'p7'): ('p6', 'p7', ('p7', 'p1'), ('p7', 'p2')), 
('p8', 'p4'): ('p8', 'p4', None, None),
('p8', 'p3'): ('p8', 'p3', None, None), 
'pTop': ('Top', 'p6', ('p6', 'p7'), ('p6', 'p8')), 
('p7', 'p1'): ('p7', 'p1', None, None)}





























