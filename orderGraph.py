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
			if child != None:
				dicto[child] += 1
	place = 0
	for key in recopy:
		if key != None:
			if dicto[key] == 0:
				LonerList.append(key)
	while LonerList:
		for thing in LonerList:
			order[thing] = place
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
		return None
	return order

def findnth(order, n):
	for key in order:
		if order[key] == n:
			return key
	return None

def layer(order,recon):
	layers = {}
	dicto = {}
	x = findnth(order, 0)
	layers[x] = 0
	n = 0
	try:
		while True:
			x = findnth(order,n)
			for child in recon[x]:
				if child != None:
					layers[child] = layers[x] + 1
			n += 1
	except:
		return layers



