import copy

def findLoner(reco):
	dicto = {}
	for key in reco:
		dicto[key] = False
	for key in reco:
		for child in reco[key]:
			dicto[child] = True
	for key in reco:
		if reco[key] == False:
			return key
	return None

def date(recon):
	order = {}
	recopy = copy.deepcopy(recon)
	place = 0
	while recopy:
		x = findLoner(recopy)
		if x == None:
			return None
		order[x] = place
		place += 1
		del recopy[x]
	return order