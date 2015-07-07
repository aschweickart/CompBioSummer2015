# BiasedGenerator.py
# Annalise Schweickart, July 2015


import random
import RandomDP
import newickFormatReader   


def findRoot(Tree):
    """This function takes in a Tree and returns a string with the name of
    the root vertex of the tree"""

    if 'pTop' in Tree:
        return Tree['pTop'][1]
    return Tree['hTop'][1] 


def orderDTL(DTL, ParasiteRoot):
    """This function takes in a DTL graph and the ParasiteRoot. It outputs a
    list, keysL, that contains tuples. Each tuple has two elements. The first
    is a mapping node of the form (p, h), where p is a parasite node and h is
    a host node. The second element is a level representing the depth of that
    mapping node within the tree."""

    keysL = []
    topNodes = []
    for key in DTL:
        if key[0] == ParasiteRoot:
            topNodes.append(key)
    for vertex in topNodes:
        keysL.extend(orderDTLRoots(DTL, vertex, 0))
    return keysL

def orderDTLRoots(DTL, vertex, level):
    """this function takes a DTL graph, one node, vertex, of the DTL graph, 
    and a level, and returns a list, keysL, that contains tuples. Each tuple
    has two elements. The first is a mapping node of the form (p, h), where p
    is a parasite node and h is a host node. The second element is a level 
    representing the depth of that mapping node within the tree. This function
    adds the input vertex to keysL and recurses on its children."""

    keysL = []
    for i in range(len(DTL[vertex]) - 1):      #loop through each event of key
        event = DTL[vertex][i]
        child1 = event[1]
        child2 = event[2]
        keysL = keysL + [(vertex, level)]
        if child1[0] != None:
            keysL.extend(orderDTLRoots(DTL, child1, level + 1))
        if child2[0] != None:
            keysL.extend(orderDTLRoots(DTL, child2, level + 1)) 
    return keysL


def sortHelper(DTL, keysL):
    """This function takes in a list orderedKeysL and deals with duplicate 
    mapping nodes that could potentially have the same level or have two 
    different levels, in which case we want to choose the highest level 
    because we are using the bottom-up approach"""
    
    uniqueKeysL = []
    for key in DTL:
        maxLevel = float("-inf")
        for element in keysL:
            if key == element[0]:
                if element[1] > maxLevel:
                    maxLevel = element[1]
        uniqueKeysL.append((key, maxLevel))
    return uniqueKeysL


def preorderDTLsort(DTL, ParasiteRoot):
    """This takes in a DTL dictionary and parasite root and returns a sorted
    list, orderedKeysL, that is ordered by level from smallest to largest,
    where level 0 is the root and the highest level has tips."""

    keysL = orderDTL(DTL, ParasiteRoot)
    uniqueKeysL = sortHelper(DTL, keysL)
    orderedKeysL = []
    levelCounter = 0
    while len(orderedKeysL) < len(uniqueKeysL):
        for mapping in uniqueKeysL:
            if mapping[-1] == levelCounter:
                orderedKeysL = orderedKeysL + [mapping]
        levelCounter += 1
    return orderedKeysL

def normalizer(DTL):
    """Takes in a DTL graph and normalizes the scores within a key,
    returning a new DTL with normalized scores"""
    for key in DTL.keys():
        totalScore = 0
        for event in DTL[key][:-1]:
            totalScore += event[-1]
        for event in DTL[key][:-1]:
            event[-1] = event[-1]/totalScore
    return DTL

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

def rootGenerator(DTL, parasiteTree):
    """Generates a list of the roots in a DTL graph"""
    parasiteRoot = findRoot(parasiteTree)
    preOrder = preorderDTLsort(DTL, parasiteRoot)
    rootList = []
    for key in preOrder:
        if key[1] == 0:
            rootList.append(key[0])
    return rootList

def biasedChoice(rootList, probList):
    """Takes in a list of vertex pairs and a correspondiing list of their 
    frequencies and returns a vertex pair randomly chosen but weighted by
    its frequency"""
    num = 100
    choices = []
    for n in range(len(rootList)):
        currentProb = probList[n]
        currentRoot = [rootList[n]]
        currentEntry = int(currentProb*num)*currentRoot
        choices.extend(currentEntry)
    return random.choice(choices)

def makeProbList(DTL, root):
    """Takes as input a DTL graph and a root and returns the frequencies 
    associated with the events occuring at that root in a list"""
    probList = []
    for event in DTL[root][:-1]:
        probList.append(event[-1])
    return probList

def randomReconGen(DTL, rootList, randomRecon):
    '''Takes in a DTL graph, a list of vertex pairs, and a dictionary of the
    growing reconciliation and recursively builds the reconciliation using 
    biasedChoice to decide which events will occur'''
    if rootList ==[]:
        return randomRecon  
    newRootL = []   
    for root in rootList:
        probList = makeProbList(DTL, root)
        newChild = biasedChoice(DTL[root][:-1],probList)
        randomRecon[root] = newChild
        if newChild[1] != (None, None) and not newChild[1] in randomRecon and\
        not newChild[1] in newRootL:
            newRootL.append(newChild[1])
        if newChild[2] != (None, None) and not newChild[2] in randomRecon and\
        not newChild[2] in newRootL:
            newRootL.append(newChild[2])
    return randomReconGen(DTL, newRootL, randomRecon)


def biasedReconGenWrapper(fileName, D, T, L):
    '''Takes in a file, and duplication, transfer, and loss costs and returns
    the reconciliation built by randomReconGen starting at the root'''
    H, P, phi = newickFormatReader.getInput(fileName)
    DTL, numRecon, Score = RandomDP.reconcile(fileName, D, T, L)
    normalizedDTL = normalizer(DTL)
    rootList = rootGenerator(normalizedDTL, P)
    scoreList = []
    for root in rootList:
        scoreList.append(Score[root])
    rootScoreList = normalizeList(scoreList)
    startRoot = biasedChoice(rootList,rootScoreList)
    randomRecon = randomReconGen(DTL, [startRoot], {})
    for key in randomRecon.keys():
        randomRecon[key] = randomRecon[key][:-1]
    return randomRecon










