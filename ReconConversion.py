# PROF WU VISUALIZATION RECONCILIATION FORMAT CONVERSION
def convert(reconciliation):
	"""Takes as input a dictionary of a reconciliation between host and parasite trees, and outputs the same tree converted
	to brecon (gene node, species node, event) format."""

	f = open("testConvert.mowgli.brecon", 'a')
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