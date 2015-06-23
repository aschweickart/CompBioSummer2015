#JULIET AND SRINIDHI

fDTL = {('p8', 'h2'): [['T', ('p3', 'h2'), ('p4', 'h4'), 1], 1], 
('p7', 'h1'): [['T', ('p1', 'h1'), ('p2', 'h3'), 1], 1], 
('p1', 'h1'): [['C', (None, None), (None, None), 1], 0], 
('p6', 'h7'): [['S', ('p7', 'h1'), ('p8', 'h2'), 1], 2], 
('p3', 'h2'): [['C', (None, None), (None, None), 1], 0], 
('p8', 'h4'): [['T', ('p4', 'h4'), ('p3', 'h2'), 1], 1], 
('p2', 'h3'): [['C', (None, None), (None, None), 1], 0], 
('p6', 'h8'): [['S', ('p7', 'h3'), ('p8', 'h4'), 1], 2], 
('p7', 'h3'): [['T', ('p2', 'h3'), ('p1', 'h1'), 1], 1], 
('p4', 'h4'): [['C', (None, None), (None, None), 1], 0]}



pointList = ['POINT (0.1, 0.2)', 'POINT (0.1, 0.1)', 'POINT (1.3333333333333335, 5.0)', 'POINT (0.1, 1.3)']


def deleteCommas(pointList):
	"""Takes in a list of points, returns the same list except without commas"""
	newList = []
	for point in pointList:
		string = ""
		for i in point:
			if i != ',':
				string = string + i
		newList.append(string)
	return newList

def getDTLvals(pointList):
	""" """
	pointList = deleteCommas(pointList)
	DTLPairs = []
	for point in pointList:
		coordList = point[7:-1].split()
		pair = []
		for i in coordList:
			pair.append(float(i))
		DTLPairs.append(tuple(pair))
	return DTLPairs
