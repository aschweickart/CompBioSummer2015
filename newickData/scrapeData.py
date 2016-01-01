import os
import csv

avgcsv = open('distance3davg.csv', 'wb')
maxcsv = open('distance3dmax.csv', 'wb')

AVG = 0
MAX = 1
maxNumIterations = 4
valuesOfKTested = 4

def getDistances(f):
    ourFileList = [] #list for this file
    thisKList = []   #one element of above list, for a particular K
    nextLine = f.readline() #this is the 'k = 1' line
    nextLine = f.readline() #this is the first data point
    while (nextLine != ''):
        if 'k =' in nextLine: #time for the next k
            ourFileList.append(thisKList)
            thisKList = []
        else:
            avgD, maxD = [float(x) for x in nextLine[:-1].split(' ')]
            thisKList.append((avgD, maxD))
        nextLine = f.readline()
    ourFileList.append(thisKList)
    return ourFileList

#helper for 2d data generation
def totalChange(k, data, ty):
    if data[k][0][ty] == 0:
        return data[k][-1][ty] != data[k][0][ty]
    return (data[k][-1][ty] - data[k][0][ty])/float(data[k][0][ty])

#helper for 3d data generation
def incrementalChange(k, j, data, ty):
    #if we don't have enough 
    idx = j if j < len(data[k]) else -1
    if data[k][0][ty] == 0:
        return data[k][idx][ty] != data[k][0][ty]
    return (data[k][idx][ty] - data[k][0][ty])/float(data[k][0][ty])


#a list of lists, one for each data set
#each sublist is a list (indexed by k) of lists
#(indexed by the iteration number) of tuples
#representing the average and maximum distance at
#that iteration step
distanceData = []
#eventually, one entry of distanceData may look like:
#distanceData[i] == [ [(36,60)], [(31, 30), (46, 44)] ]
#this would mean that the ith entry in distanceData corresponds
#to a dataset which converged 

filenames = []
for filename in os.listdir("./data"):
    f = open("data/" + filename, 'r')
    filenames.append(filename[7:])
    distanceData.append(getDistances(f))
    f.close()


for i in range(len(distanceData)):
    filedata = distanceData[i]
    for k in range(valuesOfKTested):
        for j in range(1, len(filedata[k])):
            if filedata[k][j-1][AVG] < filedata[k][j][AVG]:
                print filenames[i]


numFiles = len(distanceData)
percentChangeAVG = [0,0,0,0]
percentChangeMAX = [0,0,0,0]

for filedata in distanceData:
    for k in range(valuesOfKTested):
        percentChangeAVG[k] += totalChange(k, filedata, AVG)
        percentChangeMAX[k] += totalChange(k, filedata, MAX)

print "Averages"
for i in range(valuesOfKTested):
    print 100.0*percentChangeAVG[i]/numFiles

print "Maxima"
for i in range(valuesOfKTested):
    print 100.0*percentChangeMAX[i]/numFiles

percentChangeMAX = [maxNumIterations*[0] for x in range(valuesOfKTested)]
percentChangeAVG = [maxNumIterations*[0] for x in range(valuesOfKTested)]

for filedata in distanceData:
    for k in range(valuesOfKTested):
        for j in range(maxNumIterations):
            percentChangeAVG[k][j] += incrementalChange(k, j, filedata, AVG)
            percentChangeMAX[k][j] += incrementalChange(k, j, filedata, MAX)

writer = csv.writer(avgcsv)
for k in range(valuesOfKTested):
    for j in range(maxNumIterations):
        writer.writerow([k+1, j, 100.0*percentChangeAVG[k][j]/numFiles])
writer = csv.writer(maxcsv)
for k in range(valuesOfKTested):
    for j in range(maxNumIterations):
        writer.writerow([k+1, j, 100.0*percentChangeMAX[k][j]/numFiles])

