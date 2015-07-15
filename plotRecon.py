#plotRecon.py
#Srinidhi Srinivasan, Juliet Forman, Carter Slocum
#July 2015

# This file contains functions for plotting the percentage of points collected
# for each reconciliation vs. the Gene Tree size which is determined by the
# number of leaves for the tree. It mainly uses matplotlib to do this. The 
# main function in this file is called plotRecon and the remaining functions
# are helper functions that are used by plotRecon.py

import matplotlib.pyplot as plt

#file i/o stuff:
def fileConversion(reconFile):
	"""This function takes in a text file with information about the 
	reconciliation and returns a list reconPoints of the information in list 
	form."""
	lines = [line.rstrip('\n') for line in open(reconFile)]
	lines = lines[4:]
	reconPoints = []
	for string in lines[:3]:
		index = 0
		for char in string:
			if char == ":":
				reconPoints.append(float(string[index + 2:]))
			index += 1
	#print reconPoints
	for string in lines[3:]:
		foundTab1 = False
		indexTab1 = 0
		indexTab2 = 0
		for char in string:
			if char == '\t' and foundTab1 == True:
				reconPoints.append(float(string[indexTab1+1:indexTab2]))
			if char == '\t':
				foundTab1 = True
			if foundTab1 == False:
				indexTab1 += 1
			indexTab2 += 1
	return reconPoints

def calcMinandMax(reconList):
	"""This function takes in a list of the lists where each list contains
	information about the reconciliations for each tree and returns the min and
	max size of the trees that will be plotted."""
	pointMin = float("inf")
	pointMax = float("-inf")
	for reconPoints in reconList:
		if reconPoints[0] < pointMin:
			pointMin = reconPoints[0]
		if reconPoints[0] > pointMax:
			pointMax = reconPoints[0]
	return pointMin, pointMax


def plotRecon(reconList):
	"""This function takes in a list of lists where each list contains 
	information about the reconciliations for each tree and plots the graph
	where the y-axis is the percentage of points collected and the x-axis
	is the gene tree size."""
	minSize, maxSize = calcMinandMax(reconList)

	plt.ylabel('Percentage of points collected')
	plt.xlabel('Gene Tree Size')
	plt.axis([minSize-25, maxSize+25, 85, 101])

	for reconPoints in reconList:
		treeSize = reconPoints[0]
		plt.vlines(treeSize, reconPoints[3]/reconPoints[2]*100, 100, \
			color = 'k')
		currentPercentTotal = 0
		for i in range(len(reconPoints[3:])):
			random.seed(time.time())
			totalPoints = reconPoints[2]
			currentReconPoint = reconPoints[i+3]
			percentReconPoint = currentReconPoint/totalPoints*100
			currentPercentTotal += percentReconPoint
			plt.hlines(currentPercentTotal, treeSize-25, treeSize+25, \
				color = (random.random(), random.random(), random.random()))

	plt.show()
