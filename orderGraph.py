import copy
def date(recon):
	"""takes a Tree and returns a dictionary representation of the ordering of the tree"""
	order = {}
	dicto = {}
	Leaves = []
	LonerList = []
	for key in recon:
		if  key != None:
			dicto[key] = 0
		for child in recon[key]:
			if child != None:
				if recon[child][0] != None:
					dicto[child] = 0
				else:
					Leaves.append(child)
	for key in Leaves:
		if key in dicto:
			del dicto[key]
	for key in dicto:
		for child in recon[key]:
			if child != None and child in dicto:
				dicto[child] += 1
	place = 0
	for key in dicto:
		if key != None:
			if dicto[key] == 0:
				LonerList.append(key)
	while LonerList:
		x = LonerList[0]
		order[x] = place
		for child in recon[x]:
			if child != None and child[0] != None and not child in Leaves:
				if recon[child] != None:
					dicto[child] = dicto[child] - 1
					if dicto[child] == 0:
						LonerList.append(child)
		if x in LonerList and x in dicto:
			place += 1
			del LonerList[0]
			del dicto[x]
	if dicto:
		return None
	for item in Leaves:
		order[item] = len(Leaves)
	return order