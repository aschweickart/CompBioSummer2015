# PROF WU VISUALIZATION RECONCILIATION FORMAT CONVERSION
def convert(reconciliation, outputFile):
	"""Takes as input a dictionary of a reconciliation between host and parasite trees and a string containing the 
	name of a file where it will put the output. The function outputs the same tree converted to brecon format."""
	
	D = {'T': 'trans', 'S': 'spec', 'D': 'dup', 'C': 'gene'}
	f = open(outputFile + ".mowgli.brecon", 'w')
	event = ""
	for key in reconciliation:
		if reconciliation[key][0] != 'L':
			event = reconciliation[key][0]
			f.write(key[0] + '\t' + key[1] + '\t' + D[event] + '\n')
	f.close()