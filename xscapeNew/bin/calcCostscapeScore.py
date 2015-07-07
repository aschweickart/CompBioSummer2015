#JULIET AND SRINIDHI

from DPJune17 import *
from costscapeScore import *
from sys import argv


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


def getDTLVals(pointList):
	"""Takes in a list of centroids of the costscape regions, and returns a list of tuples 
	containing the T, L costs for each region."""
	pointList = deleteCommas(pointList)
	DTLPairs = []
	for point in pointList:
		coordList = point[7:-1].split()
		pair = []
		for i in coordList:
			pair.append(float(i))
		DTLPairs.append(tuple(pair))
	return DTLPairs

def getCostscapeDTLs(DTLPairs, hostTree, parasiteTree, phi):
	"""takes as input DTLPairs, a list of tuples with T and L costs, and the hostTree, parasiteTree, and phi. 
	It returns a list of DTLs who scores are computed with the T and L values from DTLPairs"""
	DTLList = []
	for i in DTLPairs:
		newDTL = DP(hostTree, parasiteTree, phi, 1, i[0], i[1])
		DTLList.append(newDTL)
	return DTLList

def changeDTLScores(originalDTL, DTLList):
	"""takes as input the originalDTL and a list DTLList of the DTLs from each region in costscape. This function
	calculates a new score for each event in originalDTL, and returns a newDTL with these scores"""
	newDTL = {}
	numDTL = len(DTLList)
	for event in originalDTL:
		counter = 0
		for DTL in DTLList:
			if event in DTL:
				counter += 1
		newScore = 1.0*counter/numDTL
		oldVal = originalDTL[event]
		oldVal[0][-1] = newScore
		newDTL[event] = oldVal
	return newDTL

def newScoreWrapper(newickFile, switchLo, switchHi, lossLo, lossHi, D, T, L):
	"""takes as input hostTree, parasiteTree, phi, D, T, and L, and returns the newDTL whose scores were calculated from
	costscape."""
	# newickFile = argList[1]
	# switchLo = float(argList[2])
	# switchHi = float(argList[3])
	# lossLo = float(argList[4])
	# lossHi = float(argList[5])
	# D = float(argList[6])
	# T = float(argList[7])
	# L = float(argList[8])
	H, P, phi = newickFormatReader(newickFile)
	originalDTL = DP(H, P, phi, D, T, L)
	pointList = findCenters(newickFile, switchLo, switchHi, lossLo, lossHi)
	DTLPairs = getDTLVals(pointList)
	DTLList = getCostscapeDTLs(DTLPairs, H, P, phi)
	newDTL = changeDTLScores(originalDTL, DTLList)
	return newDTL

# def main():
# 	newScoreWrapper(argv)

# if __name__=="__main__": main()




#heliconius output:
{('petiverana_WestCR', 'rosina_WestCR'): [['C', (None, None), (None, None), 1.0], 0], 
('n2', 'm2'): [['S', ('n3', 'm3'), ('n6', 'm6'), 0.6666666666666666], 3], 
('n8', 'm9'): [['S', ('n9', 'm10'), ('petiverana_WestPA', 'rosina_WestPA'), 1.0], 1], 
('emma_EastPE', 'aglaope_EastPE'): [['C', (None, None), (None, None), 1.0], 0], 
('favorinus_EastPE', 'amaryllis_EastPE'): [['C', (None, None), (None, None), 1.0], 0], 
('etylus_EastE', 'ecuadoriensis_EastE'): [['C', (None, None), (None, None), 1.0], 0], 
('lativitta_EastE', 'malleti_EastE'): [['C', (None, None), (None, None), 1.0], 0], 
('n6', 'm7'): [['S', ('erato_EastFG', 'thelxiopeia_EastFG'), ('hydara_EastFG', 'melpomene_EastFG'), 1.0], 0], 
('n10', 'melpomene_WestPA'): [['T', ('hydara_WestPA', 'melpomene_WestPA'), ('hydara_EastT', 'melpomene_EastT'), 1.0], 1], 
('hydara_WestPA', 'melpomene_WestPA'): [['C', (None, None), (None, None), 1.0], 0], 
('n6', 'm6'): [['L', ('n6', 'm7'), (None, None), 0.6666666666666666], 1], 
('petiverana_WestPA', 'rosina_WestPA'): [['C', (None, None), (None, None), 1.0], 0], 
('n7', 'm8'): [['S', ('n8', 'm9'), ('n11', 'm11'), 1.0], 1], 
('cyrbia_WestE', 'cythera_WestE'): [['C', (None, None), (None, None), 1.0], 0], 
('hydara_EastT', 'melpomene_EastT'): [['C', (None, None), (None, None), 1.0], 0], 
('erato_EastFG', 'thelxiopeia_EastFG'): [['C', (None, None), (None, None), 1.0], 0], 
('n5', 'amaryllis_EastPE'): [['T', ('favorinus_EastPE', 'amaryllis_EastPE'), ('etylus_EastE', 'ecuadoriensis_EastE'), 1.0], 1], 
('n11', 'm11'): [['S', ('hydara_EastC', 'melpomene_EastC'), ('cyrbia_WestE', 'cythera_WestE'), 1.0], 0], 
('n9', 'm10'): [['S', ('n10', 'melpomene_WestPA'), ('petiverana_WestCR', 'rosina_WestCR'), 1.0], 1], 
('n3', 'm3'): [['S', ('n4', 'm4'), ('lativitta_EastE', 'm5'), 0.6666666666666666], 2], 
('n4', 'm4'): [['S', ('emma_EastPE', 'aglaope_EastPE'), ('n5', 'amaryllis_EastPE'), 1.0], 1], 
('hydara_EastC', 'melpomene_EastC'): [['C', (None, None), (None, None), 1.0], 0], 
('n1', 'm1'): [['S', ('n2', 'm2'), ('n7', 'm8'), 0.6666666666666666], 4], 
('hydara_EastFG', 'melpomene_EastFG'): [['C', (None, None), (None, None), 1.0], 0], 
('lativitta_EastE', 'm5'): [['L', ('lativitta_EastE', 'malleti_EastE'), (None, None), 0.6666666666666666], 1]}

#vidua output:
{('p4', 'h105'): [['T', ('p7', 'h105'), ('p6', 'h64'), 1.0], 9], 
('p4', 'L._senegala_rhodopsis'): [['T', ('p7', 'L._senegala_rhodopsis'), ('p6', 'h64'), 1.0], 9], 
('p120', 'L._sanguinodorsalis'): [['T', ('V._maryae', 'L._sanguinodorsalis'), ('V._camerunensis', 'L._rara'), 1.0], 1], 
('p33', 'P._melba_citerior'): [['T', ('V._orientalis', 'P._melba_citerior'), ('p37', 'h83'), 1.0], 1], 
('p4', 'h64'): [['T', ('p6', 'h64'), ('p7', 'h105'), 1.0], 9], 
('p29', 'h54'): [['L', ('p29', 'E._astrild'), (None, None), 0.0625], 2], 
('p116', 'C._monteiri'): [['T', ('V._larvaticola', 'C._monteiri'), ('p120', 'L._rara'), 1.0], 2], 
('V._funera', 'L._r._rubricata'): [['C', (None, None), (None, None), 1.0], 0], 
('p13', 'L._rhodopareia'): [['T', ('p21', 'L._rhodopareia'), ('V._funera', 'L._r._rubricata'), 1.0], 3], 
('p26', 'h76'): [['T', ('p28', 'h76'), ('p29', 'E._astrild'), 0.9375], 4], 
('p10', 'L._senegala_rendalii'): [['T', ('p13', 'L._senegala_rendalii'), ('p12', 'h1'), 1.0], ['T', ('p13', 'L._senegala_rendalii'), ('p12', 'C._monteiri'), 0.061224489795918366], ['T', ('p13', 'L._senegala_rendalii'), ('p12', 'L._rara'), 0.061224489795918366], ['T', ('p13', 'L._senegala_rendalii'), ('p12', 'L._rufopicta'), 0.12244897959183673], 8], 
('p12', 'C._monteiri'): [['T', ('p15', 'C._monteiri'), ('p118', 'h1'), 1.0], 4], 
('p5', 'E._erythronotos'): [['T', ('V._hypocherina', 'E._erythronotos'), ('p26', 'h76'), 0.9375], ['T', ('V._hypocherina', 'E._erythronotos'), ('p26', 'E._astrild'), 0.04081632653061224], 5], 
('V._chalybeata_W.', 'L._senegala_rhodopsis'): [['C', (None, None), (None, None), 1.0], 0], 
('p15', 'L._rufopicta'): [['T', ('V._wilsoni', 'L._rufopicta'), ('p116', 'C._monteiri'), 1.0], ['T', ('V._wilsoni', 'L._rufopicta'), ('p116', 'L._rara'), 0.061224489795918366], 3], 
('p107', 'L._senegala_rendalii'): [['T', ('V._chalybeata_S.', 'L._senegala_rendalii'), ('V._codringtoni', 'H._niveoguttatus'), 1.0], 1], 
('p116', 'L._sanguinodorsalis'): [['T', ('p120', 'L._sanguinodorsalis'), ('V._larvaticola', 'C._monteiri'), 1.0], 2], 
('p5', 'E._melpoda'): [['T', ('p26', 'E._melpoda'), ('V._hypocherina', 'E._erythronotos'), 0.9375], 5], 
('p21', 'L._rhodopareia'): [['T', ('V._purpurascens', 'L._rhodopareia'), ('p107', 'H._niveoguttatus'), 1.0], ['T', ('V._purpurascens', 'L._rhodopareia'), ('p107', 'L._senegala_rendalii'), 0.3469387755102041], 2], 
('V._raricola', 'A._subflava'): [['C', (None, None), (None, None), 1.0], 0], 
('V._togoensis', 'P._hypogrammica'): [['C', (None, None), (None, None), 1.0], 0], 
('p3', 'h51'): [['T', ('p5', 'h51'), ('p4', 'h64'), 0.0625], 15], 
('V._interjecta', 'P._phoenicoptera'): [['C', (None, None), (None, None), 1.0], 0], 
('p5', 'h51'): [['S', ('p26', 'h54'), ('V._hypocherina', 'E._erythronotos'), 0.0625], 5], 
('p3', 'E._melpoda'): [['T', ('p5', 'E._melpoda'), ('p4', 'h64'), 0.9375], 15], 
('V._camerunensis', 'L._rara'): [['C', (None, None), (None, None), 1.0], 0], 
('p26', 'h54'): [['T', ('p29', 'h54'), ('p28', 'h76'), 0.0625], ['L', ('p26', 'E._astrild'), (None, None), 0.2653061224489796], 5], 
('p3', 'E._astrild'): [['T', ('p5', 'E._astrild'), ('p4', 'h64'), 0.9375], 15], 
('p3', 'h105'): [['T', ('p4', 'h105'), ('p5', 'h51'), 1.0], ['T', ('p4', 'h105'), ('p5', 'h76'), 0.04081632653061224], 15], 
('p29', 'E._melpoda'): [['T', ('V._macroura_W.', 'E._melpoda'), ('V._macroura_S', 'E._astrild'), 0.9375], 1], 
('p32', 'P._melba_grotei'): [['T', ('V._paradisaea', 'P._melba_grotei'), ('V._obtusa', 'P._afra'), 1.0], 1], 
('p7', 'L._senegala_rhodopsis'): [['T', ('V._chalybeata_W.', 'L._senegala_rhodopsis'), ('p10', 'h105'), 1.0], 8], 
('p13', 'L._senegala_rendalii'): [['T', ('p21', 'L._senegala_rendalii'), ('V._funera', 'L._r._rubricata'), 1.0], 3], 
('p7', 'h91'): [['S', ('p10', 'L._senegala_rendalii'), ('V._chalybeata_W.', 'L._senegala_rhodopsis'), 1.0], 8], 
('V._hypocherina', 'E._erythronotos'): [['C', (None, None), (None, None), 1.0], 0], 
('V._codringtoni', 'H._niveoguttatus'): [['C', (None, None), (None, None), 1.0], 0], 
('p12', 'h1'): [['T', ('p118', 'h1'), ('p15', 'C._monteiri'), 1.0], 4], 
('V._macroura_S', 'E._astrild'): [['C', (None, None), (None, None), 1.0], 0], 
('p6', 'h64'): [['S', ('V._fischeri', 'G._ianthinogaster'), ('V._regia', 'G._granatia'), 1.0], 0], 
('V._chalybeata_S.', 'L._senegala_rendalii'): [['C', (None, None), (None, None), 1.0], 0], 
('p118', 'h1'): [['S', ('V._nigeriae', 'O._atricolis'), ('V._raricola', 'A._subflava'), 1.0], 0], 
('p12', 'L._rufopicta'): [['T', ('p15', 'L._rufopicta'), ('p118', 'h1'), 1.0], 4], 
('V._paradisaea', 'P._melba_grotei'): [['C', (None, None), (None, None), 1.0], 0], 
('p15', 'L._sanguinodorsalis'): [['T', ('p116', 'L._sanguinodorsalis'), ('V._wilsoni', 'L._rufopicta'), 1.0], 3], 
('p5', 'E._astrild'): [['T', ('p26', 'E._astrild'), ('V._hypocherina', 'E._erythronotos'), 0.9375], 5], 
('p5', 'h76'): [['T', ('p26', 'h76'), ('V._hypocherina', 'E._erythronotos'), 0.9375], 5], 
('p3', 'h91'): [['T', ('p4', 'h91'), ('p5', 'h51'), 1.0], ['T', ('p4', 'h91'), ('p5', 'h76'), 0.10204081632653061], 15], 
('p29', 'E._astrild'): [['T', ('V._macroura_S', 'E._astrild'), ('V._macroura_W.', 'E._melpoda'), 1.0], 1], 
('p10', 'h105'): [['S', ('p13', 'L._rhodopareia'), ('p12', 'L._sanguinodorsalis'), 1.0], 7], 
('p26', 'E._melpoda'): [['T', ('p29', 'E._melpoda'), ('p28', 'h76'), 0.9375], 4], 
('p26', 'E._astrild'): [['T', ('p29', 'E._astrild'), ('p28', 'h76'), 1.0], 4], 
('p116', 'L._rara'): [['T', ('p120', 'L._rara'), ('V._larvaticola', 'C._monteiri'), 1.0], 2], 
('V._nigeriae', 'O._atricolis'): [['C', (None, None), (None, None), 1.0], 0], 
('p4', 'h91'): [['T', ('p7', 'h91'), ('p6', 'h64'), 1.0], 9], 
('p3', 'E._erythronotos'): [['T', ('p5', 'E._erythronotos'), ('p4', 'h64'), 0.9375], 15], 
('p15', 'C._monteiri'): [['T', ('p116', 'C._monteiri'), ('V._wilsoni', 'L._rufopicta'), 1.0], 3], 
('V._orientalis', 'P._melba_citerior'): [['C', (None, None), (None, None), 1.0], 0], 
('p12', 'L._rara'): [['T', ('p15', 'L._rara'), ('p118', 'h1'), 1.0], 4], 
('V._macroura_W.', 'E._melpoda'): [['C', (None, None), (None, None), 1.0], 0], 
('p3', 'h76'): [['T', ('p5', 'h76'), ('p4', 'h64'), 0.9375], ['T', ('p5', 'h76'), ('p4', 'h105'), 0.04081632653061224], 15], 
('p107', 'H._niveoguttatus'): [['T', ('V._codringtoni', 'H._niveoguttatus'), ('V._chalybeata_S.', 'L._senegala_rendalii'), 1.0], 1], 
('p28', 'h76'): [['S', ('p32', 'P._melba_grotei'), ('p33', 'P._melba_citerior'), 1.0], 2], 
('p7', 'h105'): [['T', ('p10', 'h105'), ('V._chalybeata_W.', 'L._senegala_rhodopsis'), 1.0], 8], 
('V._maryae', 'L._sanguinodorsalis'): [['C', (None, None), (None, None), 1.0], 0], 
('p21', 'L._senegala_rendalii'): [['T', ('p107', 'L._senegala_rendalii'), ('V._purpurascens', 'L._rhodopareia'), 1.0], 2], 
('V._larvaticola', 'C._monteiri'): [['C', (None, None), (None, None), 1.0], 0], 
('V._obtusa', 'P._afra'): [['C', (None, None), (None, None), 1.0], 0], 
('V._regia', 'G._granatia'): [['C', (None, None), (None, None), 1.0], 0], 
('V._purpurascens', 'L._rhodopareia'): [['C', (None, None), (None, None), 1.0], 0], 
('p15', 'L._rara'): [['T', ('p116', 'L._rara'), ('V._wilsoni', 'L._rufopicta'), 1.0], 3], 
('p12', 'L._sanguinodorsalis'): [['T', ('p15', 'L._sanguinodorsalis'), ('p118', 'h1'), 1.0], 4], 
('p120', 'L._rara'): [['T', ('V._camerunensis', 'L._rara'), ('V._maryae', 'L._sanguinodorsalis'), 1.0], 1], 
('V._wilsoni', 'L._rufopicta'): [['C', (None, None), (None, None), 1.0], 0], 
('p3', 'L._senegala_rhodopsis'): [['T', ('p4', 'L._senegala_rhodopsis'), ('p5', 'h51'), 1.0], ['T', ('p4', 'L._senegala_rhodopsis'), ('p5', 'h76'), 0.04081632653061224], 15], 
('p3', 'h64'): [['T', ('p4', 'h64'), ('p5', 'h51'), 1.0], ['T', ('p4', 'h64'), ('p5', 'h76'), 0.04081632653061224], 15], 
('V._fischeri', 'G._ianthinogaster'): [['C', (None, None), (None, None), 1.0], 0], 
('p37', 'h83'): [['S', ('V._interjecta', 'P._phoenicoptera'), ('V._togoensis', 'P._hypogrammica'), 1.0], 0]}
























