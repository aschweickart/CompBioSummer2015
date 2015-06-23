#Juliet and Srinidhi

#!/usr/bin/env python

# costscape.py
# Ran Libeskind-Hadas, Jessica Yi-Chieh Wu, Mukul Bansal, November 2013

# python libraries
import time
import math

# xscape libraries
try:
    import xscape
except ImportError:
    import sys
    from os.path import realpath, dirname, join
    sys.path.append(join(realpath(dirname(dirname(__file__))), "python"))
    import xscape
from xscape.commonAnalytic import *
from xscape.CostVector import *
from xscape import getInput
from xscape import reconcile
from xscape import plotcostsAnalyticNew as plotcosts

print "Costscape %s" % xscape.PROGRAM_VERSION_TEXT
hostTree, parasiteTree, phi, switchLo, switchHi, lossLo, lossHi, outfile = \
    getInput.getInput(outputExtension = "pdf", allowEmptyOutfile=True)
log = getInput.boolInput("Display in log coordinates? ")
if outfile == "":
    display = True
else:
    display = getInput.boolInput("Display to screen? ")
print "Reconciling trees..."
startTime = time.time()
CVlist = reconcile.reconcile(parasiteTree, hostTree, phi, \
                                 switchLo, switchHi, lossLo, lossHi)
endTime = time.time()
elapsedTime = endTime- startTime
print "Elapsed time %.2f seconds" % elapsedTime

# plotcosts.plotcosts(CVlist, lossLo, lossHi, switchLo, switchHi, \
#                         outfile, \
#                         log, display)

if outfile != "":
    print "Output written to file: ", outfile

#if __name__ == '__main__': main()


import shapely
from shapely.wkt import loads as load_wkt



#coordList eg
[[(0.1, 0.2), (0.1, 1.3), (1.3333333333333335, 5.0), (2.5, 5.0), (0.1, 0.2)], 
[(0.1, 0.1), (0.1, 0.2), (2.5, 5.0), (5.0, 5.0), (5.0, 0.1), (0.1, 0.1)], 
[(1.3333333333333335, 5.0), (0.1, 1.3)], 
[(0.1, 1.3), (0.1, 5.0), (1.3333333333333335, 5.0), (0.1, 1.3)]]


def getNewCoordList():
    """ """
    coordList = plotcosts.plotcosts(CVlist, lossLo, lossHi, switchLo, switchHi, outfile, log, display)
    newCoordList = []
    for element in coordList:
        string = "POLYGON(("
        for i in element:
            string = string + str(i[0]) + ' ' + str(i[1]) + ','
        string = string[:-1] + '))'
        newCoordList.append(string)
    return newCoordList



# ([(0.1, 0.2), (0.1, 1.3), (1.3333333333333335, 5.0), (2.5, 5.0), (0.1, 0.2)], 3.478333333333333), 
# ([(0.1, 0.1), (0.1, 0.2), (2.5, 5.0), (5.0, 5.0), (5.0, 0.1), (0.1, 0.1)], 18.250000000000007), 
# [(1.3333333333333335, 5.0), (0.1, 1.3)], 
# ([(0.1, 1.3), (0.1, 5.0), (1.3333333333333335, 5.0), (0.1, 1.3)], 2.2816666666666667)

['POLYGON((0.1 0.2,0.1 1.3,1.33333333333 5.0,2.5 5.0,0.1 0.2))', 
'POLYGON((0.1 0.1,0.1 0.2,2.5 5.0,5.0 5.0,5.0 0.1,0.1 0.1))', 
'POLYGON((1.33333333333 5.0,0.1 1.3))', 
'POLYGON((0.1 1.3,0.1 5.0,1.33333333333 5.0,0.1 1.3))']

['POINT (1.155097694723539 3.159479316404207)', 'POINT (3.070767123287671 2.28172602739726)', 'POINT (0.51111111111 3.766666666666667)']

def findCenters():
    """ """
    coordList = plotcosts.plotcosts(CVlist, lossLo, lossHi, switchLo, switchHi, outfile, log, display)
    polygonList = getNewCoordList()
    pointList = []
    for i in range(len(polygonList)):
        point = polygonList[i]
        numCommas = 0
        for j in range(len(point)):
            if point[i] == ",":
                numCommas = numCommas + 1
        if numCommas > 1:
            #polygon case
            region = load_wkt(point)
            pointList.append((region.centroid.wkt))
        elif numCommas == 1:
            #line case
            x1 = coordList[i][0][0]
            y1 = coordList[i][0][1]
            x2 = coordList[i][1][0]
            y2 = coordList[i][1][1]
            midx = math.abs(x1 - x2) + min(x1, x2)
            midy = math.abs(y1 - y2) + min(y1, y2)
            pointList.append("POINT (" + str(midx) + " " + str(midy) + ")")
        else:
            #point case
            pointList.append("POINT " + str(coordList[i][0]))

    return pointList


























