import copy
def date(recon):
	order = {}
	dicto = {}
	Leaves = []
	LonerList = []
	recopy = copy.deepcopy(recon)
	for key in recopy:
		if  key != None:
			dicto[key] = 0
		for child in recopy[key]:
			if child != None:
				if recopy[child][0] != None and recopy[child][1] != None:
					dicto[child] = 0
				else:
					Leaves.append(child)
	for key in Leaves:
		if key in dicto:
			del dicto[key]
	for key in dicto:
		for child in recopy[key]:
			if child != None and child in dicto:
				dicto[child] += 1
	place = 0
	for key in dicto:
		if key != None:
			if dicto[key] == 0:
				LonerList.append(key)
	while LonerList:
		print LonerList
		x = LonerList[0]
		order[x] = place
		for child in recopy[x]:
			if child != None and child[0] != None and not child in Leaves:
				if recopy[child] != None:
					dicto[child] = dicto[child] - 1
					if dicto[child] == 0:
						LonerList.append(child)
		if x in LonerList and x in dicto:
			place += 1
			del LonerList[0]
			del dicto[x]
	if dicto:
		print"Invalid Reconciliation", dicto
		return None
	print Leaves
	for item in Leaves:
		order[item] = len(Leaves)
	print order
	return order