#scoreComparison.py

#carter: getting input three lists where each element in the list is in
#in the form of a tuple: (total # events, # events unique)


def averageDifferentEvents():
	""" """
	frequencyL, unitL, costscapeL = diffEvents() #input carter's function name
	percentFreqDict = makePercentDict(frequencyL)
	percentUnitDict = makePercentDict(unitL)
	percentCostDict = makePercentDict(costscapeL)
	avgFreqPercent = calcAvgPercent(percentFreqDict)
	avgUnitPercent = calcAvgPercent(percentUnitDict)
	avgCostPercent = calcAvgPercent(percentCostDict)
	return avgFreqPercent, avgUnitPercent, avgCostPercent

def makePercentDict(scoreL):
	"""This function takes in a scoringList where each element in the list is 
	in the form of a tuple: (total # events, # events unique) and returns a 
	dictionary where the keys are tuples and the values are the decimal value 
	difference betweent the unique events and all the events."""
	totalEvents = 0
	uniqueEvents = 0
	scoringDict = {}
	for element in scoreL:
		totalEvents = element[0]
		uniqueEvents = element[1]
		scoringDict[element] = uniqueEvents*1.0/totalEvents
	return scoringDict

def calcAvgPercent(scoreDict):
	""" """
	avgPercent = 0
	totalPercent = 0
	numElements = len(scoreDict)
	for key in percentFreqDict:
		totalPercent += scoreDict[key]

	avgPercent = totalPercent/numElements*100
	return avgPercent

def sumDifferentEvents():
	""" """
	frequencyL, unitL, costscapeL = diffEvents() #input carter's function name
	sumFreqPercent = calcSumPercent(frequencyL)
	sumUnitPercent = calcSumPercent(unitL)
	sumCostPercent = calcSumPercent(costscapeL)
	return sumFreqPercent, sumUnitPercent, sumCostPercent

def calcSumPercent(scoreL):
	""" """
	totalEvents = 0
	uniqueEvents = 0
	sumPercent = 0
	for element in scoreL:
		totalEvents += element[0]
		uniqueEvents += element[1]
	sumPercent = uniqueEvents*1.0/totalEvents*100
	return sumPercent






		


