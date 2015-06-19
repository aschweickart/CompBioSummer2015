import copy

def date(recon):
	order = {}
	dicto = {}
	LonerList = []
	recopy = copy.deepcopy(recon)
	print recopy
	for key in recopy:
		if  key != None:
			dicto[key] = 0
		for child in recopy[key]:
			if child != None:
				dicto[child] = 0
	for key in recopy:
		for child in recopy[key]:
			if child != None:
				dicto[child] += 1
	print dicto
	place = 0
	for key in recopy:
		if key != None:
			if dicto[key] == 0:
				LonerList.append(key)
	while LonerList:
		print LonerList
		x = LonerList[0]
		print x
		order[x] = place
		place += 1
		for child in recopy[x]:
			if child != None:
				dicto[child] = dicto[child] - 1
				if dicto[child] == 0:
					LonerList.append(child)
			if x in LonerList and x in dicto:
				del LonerList[0]
				del dicto[x]
	if len(dicto) >= 1:
		print recopy
		return None
	return order