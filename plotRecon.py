import matplotlib.pyplot as plt

#reconList = [[5, 2, 37, 7.0, 2.0, 5.0, 13.0, 10.0], [15, 3, 115, 1.0, 7.0, 65.0, 32.0, 4.0, 6.0]]

#file i/o stuff:
def fileConversion(reconFile):
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
		print reconPoints
	print reconPoints

def calcMinandMax(reconList):
	pointMin = float("inf")
	pointMax = float("-inf")
	for reconPoints in reconList:
		if reconPoints[0] < pointMin:
			pointMin = reconPoints[0]
		if reconPoints[0] > pointMax:
			pointMax = reconPoints[0]
	return pointMin, pointMax


def plotRecon(reconList):
	minSize, maxSize = calcMinandMax(reconList)

	plt.ylabel('Percentage of points collected')
	plt.xlabel('Gene Tree Size')
	plt.axis([minSize-10, maxSize+10, 0, 101])

	for reconPoints in reconList:
		treeSize = reconPoints[0]
		plt.vlines(treeSize, reconPoints[3]/reconPoints[2]*100, 100, color = 'k')
		currentPercentTotal = 0
		for i in range(len(reconPoints[3:])):
			totalPoints = reconPoints[2]
			currentReconPoint = reconPoints[i+3]
			percentReconPoint = currentReconPoint/totalPoints*100
			currentPercentTotal += percentReconPoint
			plt.hlines(currentPercentTotal, treeSize-1, treeSize+1, color = 'b')

	plt.show()

	



		
