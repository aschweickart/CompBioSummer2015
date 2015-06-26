#Team Greedy

def findRoot(ParasiteTree):
    """This function takes in a parasiteTree and returns a string with the name of
    the root vertex of the tree"""

    ParasiteRoot = ParasiteTree['pTop'][1]
    return ParasiteRoot


def initializeMarkingDict(DTL):
    """makes a marking dictionary with all the same keys as DTL, and with all values set to False."""

    markingDict = {}
    for key in DTL:
        markingDict[key] = False
    markingDict[(None, None)] = False
    return markingDict


def orderDTL(DTL, ParasiteRoot):
    """This function takes in a DTL graph and the ParasiteRoot. It outputs a list, keysL, that contains tuples. Each tuple 
    has two elements. The first is a mapping node of the form (p, h), where p is a parasite node and h is a host node. The 
    second element is a level representing the depth of that mapping node within the tree."""

    keysL = []
    topNodes = []
    for key in DTL:
        if key[0] == ParasiteRoot:
            topNodes.append(key)
    for vertex in topNodes:
        keysL.extend(orderDTLRoots(DTL, vertex, 0))
    return keysL

def orderDTLRoots(DTL, vertex, level):
    """this function takes a DTL graph, one node, vertex, of the DTL graph, a level, and returns a list, keysL, that 
    contains tuples. Each tuple has two elements. The first is a mapping node of the form (p, h), where p is a 
    parasite node and h is a host node. The second element is a level representing the depth of that mapping node 
    within the tree. This function adds the input vertex to keysL and recurses on its children."""

    keysL = []
    for i in range(len(DTL[vertex]) - 1):          #loop through each event associated with key in DTL
        event = DTL[vertex][i]
        child1 = event[1]
        child2 = event[2]
        keysL = keysL + [(vertex, level)]
        if child1[0] != None:
            keysL = keysL + orderDTLRoots(DTL, child1, level + 1)
        if child2[0] != None:
            keysL = keysL + orderDTLRoots(DTL, child2, level + 1)
    return keysL


def sortHelper(DTL, keysL):
    """This function takes in a list orderedKeysL and deals with duplicate mapping nodes that could potentially have the 
    same level or have two different levels, in which case we want to choose the highest level becuase we are using the 
    bottom-up approach"""
    
    uniqueKeysL = []
    for key in DTL:
        maxLevel = float("-inf")
        for element in keysL:
            if key == element[0]:
                if element[1] > maxLevel:
                    maxLevel = element[1]
        uniqueKeysL.append((key, maxLevel))
    return uniqueKeysL


def postorderDTLsort(DTL, ParasiteRoot):
    """This takes in a DTL dictionary and parasite root and returns a sorted list, orderedKeysL, that is ordered
    by level from largest to smallest, where level 0 is the root and the highest level has tips."""

    keysL = orderDTL(DTL, ParasiteRoot)
    uniqueKeysL = sortHelper(DTL, keysL)
    orderedKeysL = []
    levelCounter = 0
    while len(orderedKeysL) < len(uniqueKeysL):
        for mapping in uniqueKeysL:
            if mapping[-1] == levelCounter:
                orderedKeysL = [mapping] + orderedKeysL
        levelCounter += 1
    return orderedKeysL


def bookkeeping(DTL, ParasiteTree):
    """This function takes as inputs a DTL graph and ParasiteTree, and then records what the max is at each mapping node and 
    which event the max came from. It outputs a dictionary BSFHMap by looping through the keys in a sorted list of mapping 
    nodes and finding the max score at each mapping node and event node. BSFHMap has keys of the form (p, h) which are the 
    mapping nodes, and values which are lists where the first element is a list of events with the max score, and the last 
    element is the max score."""

    #Example: BSFHMap = {(mapping node): [['event', (p, h), (p, h), score], maxScore]}
    #Example: BSFHEvent = {(event node): max}

    BSFHMap = {}
    BSFHEvent = {}
    ParasiteRoot = findRoot(ParasiteTree)
    orderedKeysL = postorderDTLsort(DTL, ParasiteRoot)   
    for key in orderedKeysL:
        mapNode = key[0]
        if DTL[mapNode][0][0] == 'C':                   #check if the key is a tip
            BSFHMap[mapNode] = [DTL[mapNode][0], DTL[mapNode][0][-1]]
        else:                                       #if key isn't a tip:
            maxScore = float("-inf")                             #initialize counter
            maxEvent = []                           #initialize variable to keep track of where max came from
            for i in range(len(DTL[mapNode]) - 1):   #iterate through the events associated with the key node
                event = tuple(DTL[mapNode][i])
                BSFHEvent[event] = event[-1]
                if event[1] != (None, None):
                    BSFHEvent[event] = BSFHEvent[event] + BSFHMap[event[1]][-1]
                if event[2] != (None, None):
                    BSFHEvent[event] = BSFHEvent[event] + BSFHMap[event[2]][-1]
                if BSFHEvent[event] > maxScore:  #check if current event has a higher score than current max
                    maxScore = BSFHEvent[event]  #if so, set new max score
                    maxEvent = list(event)                #record where new max came from
            BSFHMap[mapNode] = [maxEvent, maxScore]      #set BSFH value of key
    return BSFHMap


def TraceChildren(DTL, GreedyOnce, BSFHMap, key):
    """This function takes as input a DTL graph, a dicitonary of a best reconciliation, a BSFHMap dicitonary, and a 
    current key, adds the children of that key to the dictionary, resets the scores of the associated events to 0, 
    then recurses on the children. ADD STUFF HERE"""

    resetDTL = {}
    reset1DTL = {}
    reset2DTL = {}
    child1 = GreedyOnce[key][1]
    child2 = GreedyOnce[key][2]
    if child1 != (None, None):
        GreedyOnce[child1] = BSFHMap[child1][0][0:3]
        for i in range(len(DTL[child1]) - 1):       #this loop resets all the scores of events that have been used to 0
            if DTL[child1][i] == BSFHMap[child1][0]:
                #print "DTL[child1][i]:", DTL[child1][i]
                #print "BSFHMap[child1][0]:", BSFHMap[child1][0]
                newValue = DTL[child1]
                newValue[i][-1] = 0
                reset1DTL[child1] = newValue
        newGreedyOnce, DTL1 = TraceChildren(DTL, GreedyOnce, BSFHMap, child1)
        reset1DTL.update(DTL1)
        GreedyOnce.update(newGreedyOnce)
    if child2 != (None, None):
        GreedyOnce[child2] = BSFHMap[child2][0][0:3]
        for i in range(len(DTL[child2]) - 1):
            if DTL[child2][i] == BSFHMap[child2][0]:
                #print "DTL[child2][i]:", DTL[child2][i]
                #print "BSFHMap[child2][0]:", BSFHMap[child2][0]
                newValue = DTL[child2]
                newValue[i][-1] = 0
                reset2DTL[child2] = newValue      
        newGreedyOnce, DTL2 = TraceChildren(DTL, GreedyOnce, BSFHMap, child2)
        reset2DTL.update(DTL2)
        GreedyOnce.update(newGreedyOnce)
    resetDTL.update(reset1DTL)
    resetDTL.update(reset2DTL)
    return GreedyOnce, resetDTL


def greedyOnce(DTL, ParasiteTree):
    """This function takes DTL, ParasiteTree, as inputs and calls bookkeeping to find BSFHMap, which is a dictionary. 
    It returns the reconciliation tree with the highest score in a dictionary called GreedyOnce, and also resets to 0 the scores 
    of the mapping nodes in the best reconciliation. The return dictionary will have keys which are the mapping nodes in the best 
    reconciliation, and values of the form (event, child1, child2)."""

    BSFHMap = bookkeeping(DTL, ParasiteTree)
    ParasiteRoot = findRoot(ParasiteTree)
    GreedyOnce = {}                     #initialize dictionary we will return
    bestKey = ()                        #variable to hold the key with the highers BSFH value
    bestScore = float("-inf")                       #variable to hold the highest BSFH value seen so far
    for key in BSFHMap:                                             #iterate trough all the keys (verteces) in BSFHMap
        if BSFHMap[key][-1] > bestScore and key[0] == ParasiteRoot: #check if key has a score higher than bestScore and includes ParasiteRoot
            bestKey = key
            bestScore = BSFHMap[key][-1]
    GreedyOnce[bestKey] = BSFHMap[bestKey][0][0:3]                  #set value in GreedyOnce of the best key we found
    
    #reset score of the mapping node we used to 0
    for i in range(len(DTL[bestKey]) - 1):                          #loop through the events associated with DTL
        #print "DTL[bestKey][i]:", DTL[bestKey][i]
        #print "BSFHMap[bestKey][0]:", BSFHMap[bestKey][0]
        if DTL[bestKey][i] == BSFHMap[bestKey][0]:           #check if the event matches the event that gave the best score
            newEvent = DTL[bestKey][i][:-1] + [0]
            newValue = DTL[bestKey][:i] + [newEvent] + DTL[bestKey][i + 1:]
            DTL[bestKey] = newValue                                 #set the score to 0

    newGreedyOnce, resetDTL = TraceChildren(DTL, GreedyOnce, BSFHMap, bestKey)
    GreedyOnce.update(newGreedyOnce)
    DTL.update(resetDTL)
    return GreedyOnce, DTL


def Greedy(DTL, numRecon, ParasiteTree, k):
    """This function takes as input a DTL graph, a ParasiteTree, and k, the desired number of best reconciliation trees. 
    It returns TreeList, a list of k dictionaries, each of which represent one of the best trees."""
    TreeList = []
    currentDTL = DTL
    counter = 0

    if k == 'all':
        while counter < numRecon:
            oneTree, currentDTL = greedyOnce(currentDTL, ParasiteTree)
            TreeList.append(oneTree)
            counter += 1

    else:
        for i in range(k):
            oneTree, currentDTL = greedyOnce(currentDTL, ParasiteTree)
            TreeList.append(oneTree)
    return TreeList



#from problemTreeStuff import *









