import matplotlib.pyplot as plt

minSize = 0
maxSize = 50

xTick = 10

#plt.plot([1,2,3,4], [1,4,9,16], 'ro')
plt.ylabel('mean percentage of points collected')
plt.xlabel('Gene Tree Size')
plt.axis([minSize, maxSize, 0, 101])
plt.vlines(10, 50, 100, color = 'b')
plt.hlines(60, xTick -1, xTick + 1, color = 'k')
plt.hlines(100, xTick-1, xTick + 1, color = 'k')
plt.show()

#file i/o stuff:
def fileConversion(reconFile):
	f = open(reconFile, 'rb')
