import copy

def date(recon):
	order = {}
	dicto = {}
	LonerList = []
	for key in recopy:
		dicto[key] = 0
	for key in recopy:
		for child in recopy[key]:
			dicto[child] += 1
	place = 0
	for key in recon:
		if dicto[key] == 0:
			LonerList += key
	while recopy and LonerList:
		x = LonerList[0]
		order[x] = place
		place += 1
		for child in recopy[x]:
			dicto[child] = dicto[child] - 1
			if dicto[child] == 0:
				LonerList += child
		del LonerList[0]
		del recopy[x]
	if recopy:
		return None
	return order