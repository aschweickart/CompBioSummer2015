#Juliet and Srinidhi

#!/usr/bin/env python

# costscape.py
# Ran Libeskind-Hadas, Jessica Yi-Chieh Wu, Mukul Bansal, November 2013

# python libraries
import time
import math

# xscape libraries

from newickFormatReader import *

def getInput(newickFile, switchLo, switchHi, lossLo, lossHi):
    """Takes as input a newick file in the form <filename>.newick, and low and high values
    for costscape for both switches and losses. Returns hostTree, parasiteTree, phi, and the 
    same high and low values for switch and loss."""

    hostTree, parasiteTree, phi = newickFormatReader(newickFile)
    return hostTree, parasiteTree, phi




try:
    import xscape
except ImportError:
    import sys
    from os.path import realpath, dirname, join
    sys.path.append(join(realpath(dirname(dirname(__file__))), "python"))
    import xscape
from xscape.commonAnalytic import *
from xscape.CostVector import *
from xscape import reconcile
from xscape import plotcostsAnalyticNew as plotcosts


import shapely
from shapely.wkt import loads as load_wkt



#coordList eg
[[(0.1, 0.2), (0.1, 1.3), (1.3333333333333335, 5.0), (2.5, 5.0), (0.1, 0.2)], 
[(0.1, 0.1), (0.1, 0.2), (2.5, 5.0), (5.0, 5.0), (5.0, 0.1), (0.1, 0.1)], 
[(1.3333333333333335, 5.0), (0.1, 1.3)], 
[(0.1, 1.3), (0.1, 5.0), (1.3333333333333335, 5.0), (0.1, 1.3)]]


def getNewCoordList(newickFile, switchLo, switchHi, lossLo, lossHi):
    """Takes as input a newick file in the form <filename>.newick, and low and high values
    for costscape for both switches and losses. Returns a list of coordinates in the form of 
    strings."""
    hostTree, parasiteTree, phi = newickFormatReader(newickFile)
    CVlist = reconcile.reconcile(parasiteTree, hostTree, phi, switchLo, switchHi, lossLo, lossHi)
    coordList = plotcosts.plotcosts(CVlist, lossLo, lossHi, switchLo, switchHi, "", False, False)
    newCoordList = []
    for element in coordList:
        string = "POLYGON(("
        for i in element:
            string = string + str(i[0]) + ' ' + str(i[1]) + ','
        string = string[:-1] + '))'
        newCoordList.append(string)
    return newCoordList


#['POINT (1.155097694723539 3.159479316404207)', 'POINT (3.070767123287671 2.28172602739726)', 'POINT (0.716666666667 3.15)', 'POINT (0.51111111111 3.766666666666667)']


def findCenters(newickFile, switchLo, switchHi, lossLo, lossHi):
    """Returns """
    hostTree, parasiteTree, phi = newickFormatReader(newickFile)
    CVlist = reconcile.reconcile(parasiteTree, hostTree, phi, switchLo, switchHi, lossLo, lossHi)
    coordList = plotcosts.plotcosts(CVlist, lossLo, lossHi, switchLo, switchHi, "", False, False)
    polygonList = getNewCoordList(newickFile, switchLo, switchHi, lossLo, lossHi)
    pointList = []
    for i in range(len(polygonList)):
        point = polygonList[i]
        numCommas = 0
        for j in range(len(point)):
            if point[j] == ",":
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
            midx = (x1 + x2)*1.0/2
            midy = (y1 + y2)*1.0/2
            pointList.append("POINT (" + str(midx) + " " + str(midy) + ")")
        else:
            #point case
            pointList.append("POINT " + str(coordList[i][0]))

    return pointList


























