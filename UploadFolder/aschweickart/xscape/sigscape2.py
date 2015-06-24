#sigscape2.py
from multiprocessing import Process, Queue  # For multiprocessing random trials
import random
import sys
import time


from os.path import realpath, dirname, join
sys.path.append(join(realpath(dirname(dirname(__file__))), "python"))
from common import *
from CostVector import *
import reconcile
import plotsig2
from sys import argv
from newickFormatReader2 import *

DOTS = 100
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
    log=list[6]
    numTrials=list[7]
    numTrials = int(numTrials)
    output = str(outputFile(treeFile)) +"sigscape.pdf"
    outtext= str(outputFile(treeFile)) + "sigscape.txt"
    while True:
        fileName = treeFile
        if fileName.endswith(".newick"):
        	try:
        		fileHandle = open(fileName, 'r')
        		break
        	except IOError:
        		print "Error reading file. Please try again"
        else:
            print "tree"
    hostTree, parasiteTree, phi = newickFormatReader(fileHandle)
    fileHandle.close()

    switchLo = float(switchLo)
    switchHi = float(switchHi)
    lossLo = float(lossLo)
    lossHi = float(lossHi)

    log = log == "True"
    CVlist = reconcile.reconcile(parasiteTree, hostTree, phi, switchLo, switchHi, lossLo, lossHi)

    randomTrialsCVlist = seqTrials(parasiteTree, hostTree, phi, numTrials, switchLo, switchHi, lossLo, lossHi)

    plotsig2.plotsig(CVlist, randomTrialsCVlist, switchLo, switchHi, \
                    lossLo, lossHi, DOTS, output, outtext, log, False)


def seqTrials(parasiteTree, hostTree, phi, numTrials,
              switchLo, switchHi, lossLo, lossHi,
              verbose=True):
    ''' Perform numTrials randomization trials sequentially.  Although
        parTrials could be used to do this too, this function doesn't
        require the multiprocessing package and thus may be preferable
        to some users in some situation.'''
    parasiteTips, hostTips = getTipLists(parasiteTree, hostTree, phi)
    output = []
    for t in range(numTrials):
        if verbose:
            print ".",      # Progress indicator!
        sys.stdout.flush()
        newPhi = randomizeTips(parasiteTips, hostTips)
        output.append(reconcile.reconcile(parasiteTree, hostTree, newPhi,
                                          switchLo, switchHi, lossLo, lossHi))

    if verbose:
        print               # Newline
    return output

def getTipLists(parasiteTree, hostTree, phi):
    ''' Return the lists of tips in the given parasite and host trees.'''
    parasiteTips = phi.keys()
    hostTips = []
    for p in parasiteTips:
        h = phi[p]
        if not h in hostTips: hostTips.append(h)
    return parasiteTips, hostTips

def randomizeTips(parasiteTips, hostTips):
    ''' Takes a list of parasiteTips and a list of hostTips as input and
        returns a random tip mapping dictionary that maps each parasite tip
        to a random host tip such that each host tip gets at least one \
        parasite tip mapped onto it.'''
    random.shuffle(hostTips)        # shuffle hostTips list in place
    random.shuffle(parasiteTips)    # shuffle parasiteTips list in place
    randomPhi = {}
    numPtips = len(parasiteTips)
    numHtips = len(hostTips)
    # Map parasite tips to host tips to ensure that every host tip has
    # an associated parasite tip.
    for i in range(0, numHtips):
        randomPhi[parasiteTips[i]] = hostTips[i]
    # Map the remaining parasite tips at random to the hostTips
    for j in range(numHtips, numPtips):
        randomPhi[parasiteTips[j]] = random.choice(hostTips)
    return randomPhi

def main():
	getInput2(argv)


if __name__ == '__main__':
	main()
