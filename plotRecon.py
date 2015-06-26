import matplotlib.pyplot as plt

minSize = 0
maxSize = 50

xTick = 5

reconPoints = [5, 2, 10, 7.0, 2.0]

#file i/o stuff:
def fileConversion(reconFile):
	lines = [line.rstrip('\n') for line in open(reconFile)]
	lines = lines[2:]
	reconPoints = []
	for string in lines[:3]:
		index = 0
		for char in string:
			if char == ":":
				reconPoints.append(int(string[index + 2:]))
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

def plotRecon(reconPoints):

	
	plt.ylabel('Percentage of points collected')
	plt.xlabel('Gene Tree Size')
	#plt.plot([reconPoints[0]], [reconPoints[3]/reconPoints[2], 'ro')
	plt.axis([minSize, maxSize, 0, 101])
	plt.vlines(reconPoints[0], reconPoints[3]/reconPoints[2]*100, 100, color = 'b')
	plt.hlines(reconPoints[3]/reconPoints[2]*100, xTick -1, xTick + 1, color = 'k')
	plt.hlines(reconPoints[3]/reconPoints[2]*100 + reconPoints[4]/reconPoints[2]*100, xTick-1, xTick + 1, color = 'k')
	plt.show()

	



		
