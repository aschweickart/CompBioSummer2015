import copy

def date(recon):
	order = {}
	dicto = {}
	LonerList = []
	recopy = copy.deepcopy(recon)
	for key in recopy:
		if  key != None:
			dicto[key] = 0
		for child in recopy[key]:
			if child != None:
				dicto[child] = 0
	for key in recopy:
		for child in recopy[key]:
			print child
			if child != None:
				dicto[child] += 1
	place = 0
	for key in recopy:
		if key != None:
			if dicto[key] == 0:
				LonerList += key
	while recopy and LonerList:
		x = LonerList[0]
		order[x] = place
		place += 1
		for child in recopy[x]:
			if child != None:
				dicto[child] = dicto[child] - 1
				if dicto[child] == 0:
					LonerList += child
			del LonerList[0]
			del recopy[x]
	if recopy:
		return None
	return order