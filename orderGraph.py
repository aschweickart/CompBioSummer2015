import copy

def findLoner(reco):
	for key in reco:
		if reco[key] == 0:
			return key
	return None

def date(recon):
	order = {}
	recopy = copy.deepcopy(recon)
	dicto = {}
	for key in recopy:
		dicto[key] = 0
	for key in recopy:
		for child in recopy[key]:
			dicto[child] += 1
	place = 0
	while recopy:
		x = findLoner(recopy)
		if x == None:
			return None
		order[x] = place
		place += 1
		for child in recopy[x]:
			dicto[child] = dicto[child] - 1
		del recopy[x]
	return order