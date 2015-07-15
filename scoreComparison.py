# scoreComparison.py
# Srinidhi Srinivasan
# July 2015

# This file contains functions for finding the percent difference between the
# scoring functions. The main functions in this file are the two wrapper 
# functions: averageDifferentEvents, and sumDifferentEvents, and the rest of
# the functions are helper function that are used by the wrapper functions.


def averageDifferentEvents():
	"""This function is a wrapper function that calculates the average percent
	difference between the scoring functions."""
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
	difference between the unique events and all the events."""
	totalEvents = 0
	uniqueEvents = 0
	scoringDict = {}
	for element in scoreL:
		totalEvents = element[0]
		uniqueEvents = element[1]
		scoringDict[element] = uniqueEvents*1.0/totalEvents
	return scoringDict

def calcAvgPercent(scoreDict):
	"""This function takes as input a scoreDict, a dictionary whose keys are
	tuples and whose values are the decimal value difference between the 
	unique events and all the events and returns the average percent
	for a particular comparison."""
	avgPercent = 0
	totalPercent = 0
	numElements = len(scoreDict)
	for key in scoreDict:
		totalPercent += scoreDict[key]

	avgPercent = totalPercent/numElements*100
	return avgPercent

def sumDifferentEvents():
	"""This function is a wrapper function that calculates the sum percent
	difference between the scoring functions."""
	frequencyL, unitL, costscapeL = diffEvents() #input carter's function name
	sumFreqPercent = calcSumPercent(frequencyL)
	sumUnitPercent = calcSumPercent(unitL)
	sumCostPercent = calcSumPercent(costscapeL)
	return sumFreqPercent, sumUnitPercent, sumCostPercent

def calcSumPercent(scoreL):
	"""This function takes as input scoreL, which is a list where each element
	is a tuple that include the total number of events as well as the number 
	of unique events, and returns the sumPercent for that particular
	scoring function comparison."""
	totalEvents = 0
	uniqueEvents = 0
	sumPercent = 0
	for element in scoreL:
		totalEvents += element[0]
		uniqueEvents += element[1]
	sumPercent = uniqueEvents*1.0/totalEvents*100
	return sumPercent






		


