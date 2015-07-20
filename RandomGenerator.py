# RandomGenerator.py
# Annalise Schweickart, July 2015

# This file contains the functions for testing random reconciliations
# and checking for temporal inconsistencies


import random
import newickFormatReader
import orderGraph
import DP
import reconciliationGraph
import os
import copy
import Greedy


def preorderDTLsort(DTLReconGraph, ParasiteRoot):
    """This takes in a DTL dictionary and parasite root and returns a sorted
    list, orderedKeysL, that is ordered by level from smallest to largest,
    where level 0 is the root and the highest level has tips."""

    keysL = Greedy.orderDTL(DTLReconGraph, ParasiteRoot)
    uniqueKeysL = Greedy.sortHelper(DTLReconGraph, keysL)
    orderedKeysL = []
    levelCounter = 0
    while len(orderedKeysL) < len(uniqueKeysL):
        for mapping in uniqueKeysL:
            if mapping[-1] == levelCounter:
                orderedKeysL = orderedKeysL + [mapping]
        levelCounter += 1
    return orderedKeysL

def findTransfers(reconciliation):
    """Takes in a reconciliation graph and returns the number of transfers
    that occur in that reconciliation"""
    numTrans = 0
    for key in reconciliation.keys():
        if reconciliation[key][0] == 'T':
            numTrans +=1
    return numTrans


def normalizer(DTLReconGraph):
    """Takes in a DTL graph and normalizes the scores within a key,
    returning a new DTL with normalized scores"""
    for key in DTLReconGraph.keys():
        totalScore = 0
        for event in DTLReconGraph[key][:-1]:
            totalScore += event[-1]
        for event in DTLReconGraph[key][:-1]:
            event[-1] = event[-1]/totalScore
    return DTLReconGraph

def normalizeList(scoreList):
    """Takes in a list of scores and returns a new list with those scores
    normalized"""
    totalScore = 0
    newScoreList = []
    for score in scoreList:
        totalScore+=score
    for score in scoreList:
        newScoreList.append(score/totalScore)
    return newScoreList

def rootGenerator(DTLReconGraph, parasiteTree):
    """Generates a list of the roots in a DTL graph"""
    parasiteRoot = Greedy.findRoot(parasiteTree)
    preOrder = preorderDTLsort(DTLReconGraph, parasiteRoot)
    rootList = []
    for key in preOrder:
        if key[1] == 0:
            rootList.append(key[0])
    return rootList

def biasedChoice(rootList, probList):
    """Takes in a list of vertex pairs and a correspondiing list of their 
    frequencies and returns a vertex pair randomly chosen but weighted by
    its frequency"""
    scoreSum = 0
    rangeList = []
    for n in range(len(rootList)):
        rangeList.append((scoreSum, scoreSum+probList[n], rootList[n]))
        scoreSum += probList[n]
    choice = random.random()
    for n in rangeList:
        if n[0]<=choice<n[1]:
            return n[2]


def makeProbList(DTLReconGraph, root):
    """Takes as input a DTL graph and a root and returns the frequencies 
    associated with the events occuring at that root in a list"""
    probList = []
    for event in DTLReconGraph[root][:-1]:
        probList.append(event[-1])
    return probList


def uniformRecon(DTLReconGraph, rootList, randomRecon):
    '''Takes as input a DTL graph, a rootList, and a growing reconciliation
    dictionary and recursively builds the reconciliation dictionary, choosing
    random events'''
    if rootList ==[]:
        return randomRecon  
    newRootL = []   
    for root in rootList:
        newChild = random.choice(DTLReconGraph[root][:-1])
        randomRecon[root] = newChild
        if newChild[1] != (None, None) and not newChild[1] in randomRecon and\
        not newChild[1] in newRootL:
            newRootL.append(newChild[1])
        if newChild[2] != (None, None) and not newChild[2] in randomRecon and\
        not newChild[2] in newRootL:
            newRootL.append(newChild[2])
    return uniformRecon(DTLReconGraph, newRootL, randomRecon)


def biasedRecon(DTLReconGraph, rootList, randomRecon):
    '''Takes in a DTL graph, a list of vertex pairs, and a dictionary of the
    growing reconciliation and recursively builds the reconciliation using 
    biasedChoice to decide which events will occur'''
    if rootList ==[]:
        return randomRecon  
    newRootL = []   
    for root in rootList:
        probList = makeProbList(DTLReconGraph, root)
        newChild = biasedChoice(DTLReconGraph[root][:-1],probList)
        randomRecon[root] = newChild
        if newChild[1] != (None, None) and not newChild[1] in randomRecon and\
        not newChild[1] in newRootL:
            newRootL.append(newChild[1])
        if newChild[2] != (None, None) and not newChild[2] in randomRecon and\
        not newChild[2] in newRootL:
            newRootL.append(newChild[2])
    return biasedRecon(DTLReconGraph, newRootL, randomRecon)


def randomReconWrapper(dirName, D, T, L, numSamples, typeGen):
    """Takes in a directory of newick files, dirName, duplication, loss and 
    transfer costs, the number of desired random reconciliations, and the type
    of generator (biased or uniform), and calls those random generators to
    build a file containing the number of temporal inconsistencies found in 
    those randomly generated reconciliations as well as other information 
    relating to the file"""
    totalTimeTravel = 0 # To record total number of time travels in directory
    outOf = 0 # To record total number of reconciliations made
    # loop through files in directory
    for fileName in os.listdir(dirName):
        if fileName.endswith('.newick'):
            f = open(fileName[:-7]+'.txt', 'w')
            f.write(typeGen+" random reconciliations"+"\n")
            hostTree, parasiteTree, phi = newickFormatReader.getInput\
                (dirName+"/"+fileName)
            # find size of parasite and host trees
            parasiteSize = len(parasiteTree)+1
            hostSize = len(hostTree)+1
            DTLReconGraph, numRecon = DP.DP(hostTree, parasiteTree, phi, D, T, L)
            rootList = rootGenerator(DTLReconGraph, parasiteTree)
            randomReconList = []
            for n in range(numSamples):
                timeTravelCount = 0
                startRoot = random.choice(rootList)
                if typeGen == "uniform":
                    currentRecon = uniformRecon(DTLReconGraph, [startRoot], {})
                else: 
                    normalizeDTL = normalizer(DTLReconGraph)
                    currentRecon = biasedRecon(normalizeDTL, [startRoot], {})
                for key in currentRecon.keys():
                    currentRecon[key] = currentRecon[key][:-1]
                randomReconList.append(currentRecon)
            # make sure there are no duplicate reconciliations
            uniqueReconList = []
            for recon in randomReconList:
                if not recon in uniqueReconList:
                    uniqueReconList.append(recon)
            outOf += len(uniqueReconList)
            for recon in uniqueReconList:
                graph = reconciliationGraph.buildReconstruction\
                    (hostTree, parasiteTree, recon)
                currentOrder = orderGraph.date(graph)
                numTrans = findTransfers(recon)
                if currentOrder == 'timeTravel':
                    f.write("Temporal Inconsistency, reconciliation has "+str(numTrans)+" transfers"+"\n")
                    timeTravelCount += 1
                    totalTimeTravel += 1
                else: 
                    f.write("No temporal inconsistencies, reconciliation has "+str(numTrans)+" transfers"+"\n")
            f.write(fileName+" contains "+str(timeTravelCount)+" temporal "+ \
                "inconsistencies out of "+ str(len(uniqueReconList))+ \
                " reconciliations."+"\n"+"Total number of reconciliations: "+\
                str(numRecon)+"\n"+"Host tree size: "+str(hostSize)+"\n"+\
                "Parasite tree size: "+str(parasiteSize)+ "\n")
            f.close()
    print "Total fraction of temporal inconsistencies in directory: ", \
            totalTimeTravel, '/', outOf










