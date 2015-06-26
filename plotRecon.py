import matplotlib.pyplot as plt

minSize = 0
maxSize = 50

xTick = 10

#plt.plot([1,2,3,4], [1,4,9,16], 'ro')
# plt.ylabel('mean percentage of points collected')
# plt.xlabel('Gene Tree Size')
# plt.axis([minSize, maxSize, 0, 101])
# plt.vlines(10, 50, 100, color = 'b')
# plt.hlines(60, xTick -1, xTick + 1, color = 'k')
# plt.hlines(100, xTick-1, xTick + 1, color = 'k')
# plt.show()

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




	



		
