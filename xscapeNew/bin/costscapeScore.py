#Juliet and Srinidhi

# plotcostsAnalytic.py
# Ran Libeskind-Hadas, October 2013
# Plots the cost space using a matplotlib/pyplot

import matplotlib.pyplot as plt
from shapely.geometry import *
from CostVector import *
from commonAnalytic import *

def plotcosts(CVlist, switchMin, switchMax, lossMin, lossMax, outfile,
              log=False, display=False):
    ''' Plots the cost space for the given CVlist of CostVectors.  The x-axis
        represents loss cost (relative to unit cost for duplication) and
        the y-axis represents switch cost (relative to unit cost for
        duplication).  The x-range is from lossMin to lossMax and the
        y-range is from switchMin to switchMax.'''
    print log
    coordList = []
    if log==True:
        plt.xscale('log')
        plt.yscale('log')
    plt.axis([lossMin, lossMax, switchMin, switchMax])
    plt.xlabel("Loss cost relative to duplication")
    plt.ylabel("Transfer cost relative to duplication")
    
    # color map
    numRegions = len(CVlist)
    colorMap = buildColors(numRegions)
    patternsMap = buildPatterns(numRegions)
    # plot regions
    regions = getRegions(CVlist, switchMin, switchMax, lossMin, lossMax)
    for cv in CVlist:
        cv_str = str(cv)
        if cv_str not in regions:
            continue
        region = regions[cv_str]
        
        # output
        #print "Cost vector ", cv
        color = colorMap[CVlist.index(cv)]
	pattern = patternsMap[CVlist.index(cv)]
        label = cv_str
        if isinstance(region, Polygon):       # non-degenerate
            coords = list(region.exterior.coords)
            plt.gca().add_patch(plt.Polygon(coords,
                                            color = color, label = label, fill=False, hatch=pattern))
            
            coordList.append((coords, region.area))
            #print "  Polygon vertices: ", coords
            #print "  Polygon area: ", region.area
        elif isinstance(region, LineString):  # degenerate
            coords = list(region.coords)
            plt.plot([coords[0][0], coords[1][0]],
                     [coords[0][1], coords[1][1]],
                     linewidth = 4,
                     color = color, label = label)
            coordList.append(coords)
            #print "  Line vertices: ", coords
        elif isinstance(region, Point):       # degenerate
            coords = list(region.coords)
            plt.plot(coords[0][0], coords[0][1],
                     'o', markersize = 4,
                     color = color, label = label)
            #print "  Point vertex: ", coords
            coordList.append(coords)
        else:                                 # non-degenerate (collection)
            try:
                area = 0
                for r in region:
                    if isinstance(r, Polygon):         # non-degenerate
                        coords = list(r.exterior.coords)
                        plt.gca().add_patch(plt.Polygon(coords,
                                                        color = color, label = label, fill = False, hatch = pattern))
                        #print "  Polygon vertices: ", coords
                        #print "  Polygon area: ", r.area
                        coordList.append((coords, r.area))
                    elif isinstance(r, LineString):    # degenerate
                        coords = list(r.coords)
                        plt.plot([coords[0][0], coords[1][0]],
	                         [coords[0][1], coords[1][1]],
                                 linewidth = 4,
                                 color = color, label = label)
                        #print "  Line vertices: ", coords
                        coordList.append(coords)
                    elif isinstance(r, Point):         # degenerate
                        coords = list(r.coords)
                        plt.plot(coords[0][0], coords[0][1],
                                 'o', markersize = 4,
                                 color = color, label = label)
                        #print "  Point vertex: ", coords
                        coordList.append(coords)
                    else:
                         raise Exception("cost vector (%s) has invalid subregion (%s)" % (str(cv), str(type(r))))
                    area += r.area
                    #print "  Total area: ", area
            except:
                raise Exception("cost vector (%s) has invalid region (%s)" % (str(cv), str(type(region))))
        #print coordList
    return coordList
    
    # legend
    leg = plt.legend()
    for i in range(len(leg.legendHandles)):  # adjust legend marker thickness
        leg.legendHandles[i].set_linewidth(2.0)
    plt.title("Costscape:  " + outfile)
    
    if outfile != "":
        plt.savefig(outfile, format="pdf")
    if display:
        plt.show()

#!/usr/bin/env python

# costscape.py
# Ran Libeskind-Hadas, Jessica Yi-Chieh Wu, Mukul Bansal, November 2013

# python libraries
import time

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

def getCoordList():
	""" """
	coordList = plotcosts.plotcosts(CVlist, lossLo, lossHi, switchLo, switchHi, \
                        outfile, \
                        log, display)
	return coordList

