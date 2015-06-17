# PROF WU VISUALIZATION RECONCILIATION FORMAT CONVERSION
def convert(reconciliation, outputFile):
	"""Takes as input a dictionary of a reconciliation between host and parasite trees and the name of a file
	where it will put the output. The function outputs the same tree converted to brecon (gene node, species node, 
	event) format."""

	f = open(outputFile, 'a')
	event = ""
	for key in reconciliation:
		if reconciliation[key][0] == 'T':
			event = "trans"
		elif reconciliation[key][0] == 'S':
			event = "spec"
		elif reconciliation[key][0] == 'L':
			event = "loss"
		else:
			event = "gene"
		f.write(key[0] + '\t' + key[1] + '\t' + "event" + '\n')
	f.close()

