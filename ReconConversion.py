# ReconConversion.py
# Juliet Forman, Srinidhi Srinivasan, and Annalise Schweickart
# July 2015

# This file contains the functions for converting DTL reconciliations into 
# mowgli.brecon files to use in vistrans as well as freqSummation to create a 
# file with information to be shown on the website for DTL RnB.


# PROF WU VISUALIZATION RECONCILIATION FORMAT CONVERSION

import newickFormatReader
import DP
import Greedy
import copy
import calcCostscapeScore
import MasterReconciliation
import detectCycles
from sys import argv


def convert(reconciliation, DTL, ParasiteTree, outputFile, n):
    """Takes as input a dictionary of a reconciliation between host and 
    parasite trees, a DTL graph, and a string containing the name of a file 
    where it will put the output. The function outputs the same tree converted 
    to brecon format. Note that for losses, the parasite node in the brecon 
    representation is the parent of the given parasite node. This accounts for
    the brecon format's inability to handle losses."""
    freqSum = 0
    D = {'T': 'trans', 'S': 'spec', 'D': 'dup', 'C': 'gene', 'L': 'loss', \
        'GT': 'gtrans'}
    f = open(outputFile + str(n) + ".mowgli.brecon", 'w')
    event = ""
    pParent = parasiteParentsDict(ParasiteTree)
    newRecon = copy.deepcopy(reconciliation)
    for key in reconciliation.keys():
        if reconciliation[key][0] == 'GT':
            newRecon[key][0] = 'T'
    freqDict = frequencyDict(DTL, newRecon)
    for key in reconciliation:
        freqSum += freqDict[key]
        event = reconciliation[key][0]
        f.write(key[0] + '\t' + key[1] + '\t' + D[event] + '\t' + \
                                                str(freqDict[key]) + '\n')
    f.close()

def freqSummation(argList):
    """Takes as input an argument list containing a newick file of host and 
    parasite trees as well as their phi mapping, duplication, transfer, and 
    loss costs, the type of frequency scoring to be used, as well as switch 
    and loss cost ranges for xscape scoring, and

    returns a file containing the list of scores for each individual
    reconciliation, the sum of the those scores, the total cost of those
    reconciliations and the number of reconciliations of those trees."""
    newickFile = argList[1]
    D = float(argList[2])
    T = float(argList[3])
    L = float(argList[4])
    freqType = argList[5]
    switchLo = float(argList[6])
    switchHi = float(argList[7])
    lossLo = float(argList[8])
    lossHi = float(argList[9])
    fileName = newickFile[:-7]
    f = open(fileName+"freqFile.txt", 'w')
    host, paras, phi = newickFormatReader.getInput(newickFile)
    DTL, numRecon = DP.DP(host, paras, phi, D, T, L)
    if freqType == "Frequency":
        newDTL = DTL
    elif freqType == "xscape":
        newDTL = calcCostscapeScore.newScoreWrapper(newickFile, switchLo, switchHi, lossLo, lossHi, D, T, L)
    elif freqType == "unit":
        newDTL = MasterReconciliation.unitScoreDTL(host, paras, phi, D, T, L)
    scoresList, reconciliation = Greedy.Greedy(newDTL, paras)
    totalSum = 0
    for score in scoresList:
        totalSum +=score
    totalCost = 0
    index = reconciliation[0]
    for key in index:
        if index[key][0] == "L":
            totalCost+=L
        elif index[key][0] == "T":
            totalCost+=T
        elif index[key][0] == "D":
            totalCost+=D
    f.write(str(scoresList)+'\n')
    f.write(str(totalSum)+'\n')
    f.write(str(totalCost)+'\n')
    f.write(str(numRecon))
    f.close()

def frequencyDict(DTL, reconciliation):
    """Takes as input a DTL and a single reconciliation of that DTL and 
    returns a dictionary of the frequencies for each event in the 
    reconciliation."""
    freqDict = {}
    for key in reconciliation:
        events = DTL[key][:-1]
        for event in events:
            if event[0] == reconciliation[key][0] and \
                event[1] == reconciliation[key][1] and \
                event[2] == reconciliation[key][2]:
                freqDict[key] = event[-1]
    return freqDict

def parasiteParentsDict(P):
    """Takes a parasite tree with edges as keys and returns a dictionary with 
    keys which are the bottom nodes of those edges and values which are the 
    top nodes of those edges."""

    parentsDict = {}
    for key in P:
        if key == 'pTop':
            parentsDict[P[key][1]] = P[key][0]
        else:
            parentsDict[key[1]] = P[key][0]
    return parentsDict

def main():
    freqSummation(argv)

if __name__ == "__main__": main()
