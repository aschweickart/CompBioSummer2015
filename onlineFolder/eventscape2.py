    #eventscape2.py
# python libraries
from collections import *
from operator import itemgetter
from shapely.geometry import *
import csv

# xscape libraries
import sys
from os.path import realpath, dirname, join
sys.path.append(join(realpath(dirname(dirname(__file__))), "python"))
from commonAnalytic import *
import reconcile
from reconcileEvents import *
from newickFormatReader2 import *
from sys import argv

def outputFile(fileName):
	if fileName[-6:] == "newick":
		return fileName[:-7]
	elif filename[-4:] =="tree":
		return fileName[:-5]

def getInput2(list):
	# Get input file name and try to open it
    treeFile=list[1]
    switchLo=list[2]
    switchHi=list[3]
    lossLo=list[4]
    lossHi=list[5]
    UorI=list[6]
    CONFIG.intersection = UorI == "I"
    outfile = str(outputFile(treeFile)) +".csv"
    while True:
        fileName = treeFile
        if fileName.endswith(".newick"):
        	try:
        		fileHandle = open(fileName, 'r')
        		break
        	except IOError:
        		print "Error reading file. Please try again"
    hostTree, parasiteTree, phi = newickFormatReader(fileHandle)
    fileHandle.close()

    switchLo = float(switchLo)
    switchHi = float(switchHi)
    lossLo = float(lossLo)
    lossHi = float(lossHi)

    preCVlist = reconcile.reconcile(parasiteTree, hostTree, phi, switchLo, switchHi, lossLo, lossHi)

    CandidateCVlist.extend(restrict(preCVlist, switchLo, switchHi, lossLo, lossHi))

    CVlist = reconcileEvents(parasiteTree, hostTree, phi, switchLo, switchHi, lossLo, lossHi)

    output(outfile, CVlist, hostTree, lossLo, lossHi, switchLo, switchHi, root=parasiteTree["pTop"][1])


def restrict(CVlist, switchLo, switchHi, lossLo, lossHi, regions=None):
    restrictedList = []

    if regions is None:
        regions = getRegions(CVlist, switchLo, switchHi, lossLo, lossHi)
    for cv in CVlist:
        if str(cv) in regions:
            if cv not in restrictedList:
                restrictedList.append(cv)

    return restrictedList

def output(outfile, CVlist, hostTree, switchMin, switchMax, lossMin, lossMax,
           root="Root", regions=None):
    intersection = CONFIG.intersection
    if not intersection:
        global CVallEvents
    else:
        global CVcommonEvents

    if regions is None:
        regions = getRegions(CVlist, switchMin, switchMax, lossMin, lossMax)

    ofile = open(outfile, "wb")
    writer = csv.writer(ofile, delimiter = ",")
    optimalCVlist = restrict(CVlist, switchMin, switchMax, lossMin, lossMax,
                             regions=regions)

    allEvents = set()  # set of all events in optimal solutions in the cost space
    if not intersection:
        allEventsThisCV = defaultdict(set)  # set of all events in this Pareto CV
    for cv in optimalCVlist:
        outputRow = [cv]
        thisCV = cv.toTupleCDSL()

        if not intersection:
            for eh in hostTree:
                key = ("pTop", eh) + thisCV
                events = CVallEvents[key]
                allEventsThisCV[thisCV] |= events
                allEvents |= events
                for event in events:
                    outputRow.append(displayVersion(event, root))
        else:
            events = CVcommonEvents[thisCV]
            allEvents |= events
            for event in events:
                outputRow.append(displayVersion(event, root))

        writer.writerow(outputRow)

    eventsWithCounts = []
    if not intersection:
        eventsDict = allEventsThisCV
    else:
        eventsDict = CVcommonEvents
    for event in allEvents:
        eventcount = 0
        for bestCV in optimalCVlist:
            if event in eventsDict[bestCV.toTupleCDSL()]:
                eventcount += 1
        eventsWithCounts.append((event, eventcount))
    eventsWithCounts.sort(key = itemgetter(1), reverse = True)
    maxCounts = len(optimalCVlist)
    for count in range(maxCounts, 0, -1):
        row = ["Events in " + str(count) + " regions"]
        row.extend([displayVersion(event[0], root) for event in eventsWithCounts \
                    if event[1] == count])
        writer.writerow(row)

def displayVersion(event, root="Root", sep=" "):
    if event[0] == "pTop": parasiteNode = root
    else: parasiteNode = event[0][1]
    hostNode = event[1][1]
    eventType = event[2]
    if eventType.startswith("loss"):
        eventType = "loss" + sep + eval(eventType[5:].split()[1].strip(")"))
    if eventType.startswith("switch"):
        eventType = "switch" + sep + eval(eventType[10:].split()[1].strip(")"))
    return parasiteNode + sep + hostNode + sep + eventType



def main():
	getInput2(argv)


if __name__ == '__main__':
	main()