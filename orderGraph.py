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
	for key in dicto:
		for child in recopy[key]:
			if child != None:
				dicto[child] += 1
	place = 0
	for key in dicto:
		if key != None:
			if dicto[key] == 0:
				LonerList.append(key)
	while LonerList:
		for thing in LonerList:
			order[thing] = place
		x = LonerList[0]
		order[x] = place
		place += 1
		for child in recopy[x]:
			if child != None:
				if recopy[child] != None:
					dicto[child] = dicto[child] - 1
					if dicto[child] == 0:
						LonerList.append(child)
			if x in LonerList and x in dicto:
				del LonerList[0]
				del dicto[x]
	if len(dicto) >= 1:
		return None
	for item in Leaves:
		order[item] = len(Leaves)
	return order