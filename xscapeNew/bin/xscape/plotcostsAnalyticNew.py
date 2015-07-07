# plotcostsAnalytic.py
# Ran Libeskind-Hadas, October 2013
# Plots the cost space using a matplotlib/pyplot

# This file contains a function which finds the coordinates of the regions in 
# costscape.

#import matplotlib.pyplot as plt
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

    coordList = []
    
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
        color = colorMap[CVlist.index(cv)]
	pattern = patternsMap[CVlist.index(cv)]
        label = cv_str
        if isinstance(region, Polygon):       # non-degenerate
            coords = list(region.exterior.coords)
            coordList.append(coords)
        elif isinstance(region, LineString):  # degenerate
            coords = list(region.coords)
            coordList.append(coords)
        elif isinstance(region, Point):       # degenerate
            coords = list(region.coords)
            coordList.append(coords)
        else:                                 # non-degenerate (collection)
            try:
                area = 0
                for r in region:
                    if isinstance(r, Polygon):         # non-degenerate
                        coords = list(r.exterior.coords)
                        coordList.append(coords)
                    elif isinstance(r, LineString):    # degenerate
                        coords = list(r.coords)
                        coordList.append(coords)
                    elif isinstance(r, Point):         # degenerate
                        coords = list(r.coords)
                        coordList.append(coords)
                    else:
                         raise Exception("cost vector (%s) has invalid \
                            subregion (%s)" % (str(cv), str(type(r))))
                    area += r.area
            except:
                raise Exception("cost vector (%s) has invalid region (%s)" \
                    % (str(cv), str(type(region))))
    return coordList
    

