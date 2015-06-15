#Team Greedy

def findRoot(ParasiteTree):
    """This function takes in a parasiteTree and returns a string with the name of
    the root vertex of the tree"""

    ParasiteRoot = ParasiteTree['pTop'][1]
    return ParasiteRoot


def orderDTLwrapper(DTL, ParasiteRoot):
    """This function takes in a DTL dictionary and a ParasiteRoot, and calls orderDTL with a level of 0. It returns a list, 
    keysL, that contains tuples. Each tuple has two elements. The first is a mapping node of the form (p, h), where p is a 
    parasite node and h is a host node. The second element is a level representing the depth of that mapping node within 
    the tree. This function loops through the DTL graph and recruses on the two children of each DTL mapping node, adding 
    the results to keysL."""

    return orderDTL(DTL, ParasiteRoot, 0)

def initializeMarkingDict(DTL):
    """makes a marking dictionary with all the same keys as DTL, and with all values set to False."""
    markingDict = {}
    for key in DTL:
        markingDict[key] = False
    return markingDict


def orderDTL(DTL, ParasiteRoot, level, markingDict):
    """This function takes in a DTL dictionary, a ParasiteRoot, a level that represents the depth of 
    the of a vertex pair, and a dictionary markingDict that contains all the recursive calls we've already made. It returns a list, keysL, containing two-element tuples. The first element is a 
    mapping node of the form (p, h), where p is a parasite node and h is a host node. The second element is a level 
    representing the depth of that mapping node within the tree. This function loops through the DTL graph and recruses on the two children of each DTL 
    mapping node, adding the results to keysL."""

    keysL = []
    for key in DTL:
        if key[0] == ParasiteRoot:
            for i in range(len(DTL[key]) - 1):          #loop through each event associated with key in DTL
                event = DTL[key][i]
                child1 = event[1]
                child2 = event[2]
                if markingDict[child1] == False and markingDict[child2] == False:
                    if child1[0] == None and child2[0] == None:    #base case: mapping node (key) is a tip
                        markingDict[child1] = True
                        markingDict[child2] = True
                        keysL = keysL + [(key, level)]
                    elif child2[0] == None:                        #loss case: there is only one child (child1)
                        markingDict[child1] = True
                        markingDict[child2] = True
                        keysL = keysL + [(key, level)] + orderDTL(DTL, child1[0], level + 1, markingDict)
                    elif child1[0] == None:                        #loss case: there is only one child (child2)
                        markingDict[child1] = True
                        markingDict[child2] = True
                        keysL = keysL + [(key, level)] + orderDTL(DTL, child2[0], level + 1, markingDict)
                    else:
                        markingDict[child1] = True
                        markingDict[child2] = True
                        keysL = keysL + [(key, level)] + orderDTL(DTL, child1[0], level + 1, markingDict) + orderDTL(DTL, child2[0], level + 1, markingDict)
                elif markingDict[child1] == False:
                    if child1[0] == None:
                        markingDict[child1] = True
                        keysL = keysL + [(key, level)] + orderDTL(DTL, child1[0], level + 1, markingDict)
                    else:
                        markingDict[child1] = True
                        keysL = keysL + [(key, level)]
                elif markingDict[child2] == False:
                    if child2[0] == None:
                        markingDict[child2] = True
                        keysL = keysL + [(key, level)] + orderDTL(DTL, child2[0], level + 1, markingDict)
                    else:
                        markingDict[child2] = True
                        keysL = keysL + [(key, level)]
    return keysL


def postorderDTLsort(DTL, ParasiteRoot):
    """This takes in a DTL dictionary and parasite root and returns a sorted list, orderedKeysL, that is ordered
    by level from largest to smallest, where level 0 is the root and the highest level has tips."""
    
    keysL = orderDTLwrapper(DTL, ParasiteRoot)
    orderedKeysL = []
    levelCounter = 0
    while len(orderedKeysL) < len(keysL):
        for mapping in keysL:
            if mapping[-1] == levelCounter:
                orderedKeysL = [mapping] + orderedKeysL
        levelCounter += 1
    return orderedKeysL


def preorderDTLsort(DTL, ParasiteRoot):
    """This takes in a DTL dictionary and a parasite root and returns a sorted list, orderedKeysL, that is ordered
    by level from smalles to largest, where level 0 is the root and the highest level has tips."""

    keysL = orderDTLwrapper(DTL, ParasiteRoot)
    orderedKeysL = []
    levelCounter = 0
    while len(orderedKeysL) < len(keysL):
        for mapping in keysL:
            if mapping[-1] == levelCounter:
                orderedKeysL = orderedKeysL + [mapping] 
        levelCounter += 1
    return orderedKeysL
     

def bookkeeping(DTL, ParasiteTree):
    """This function takes as inputs a DTL graph and ParasiteTree, and then records what the max is at each mapping node and 
    which event the max came from. It outputs two dictionaries BSFHMap and BSFHEvent, by looping through the keys in 
    a sorted list of mapping nodes and finding the max score at each mapping node and event node. BSFHMap has keys of the 
    form (p, h) which are the mapping nodes, and values which are lists where the first element is a list of events with 
    the max score, and the last element is the max score. BSFHEvent is a dictionary with events as keys, and values which 
    are one number which is the max score."""

    #Example: BSFHMap = {(mapping node): [['event', (p, h), (p, h), score], maxScore]}
    #Example: BSFHEvent = {(event node): max}

    BSFHMap = {}
    BSFHEvent = {}
    ParasiteRoot = findRoot(ParasiteTree)   
    orderedKeysL = postorderDTLsort(DTL, ParasiteRoot)

    for key in orderedKeysL:
        mapNode = key[0]
        if DTL[mapNode][0][0] == 'C':                   #check if the key is a tip
            BSFHMap[mapNode] = [tuple(DTL[mapNode][0]), DTL[mapNode][0][-1]]
        else:                                       #if key isn't a tip:
            maxScore = float("-inf")                #initialize counter
            maxEvent = []                           #initialize variable to keep track of where max came from
            for i in range(len(DTL[mapNode]) - 1):   #iterate through the events associated with the key node
                event = tuple(DTL[mapNode][i])
                BSFHEvent[event] = BSFHMap[event[1]][-1] + BSFHMap[event[2]][-1] + event[-1]
                if BSFHEvent[event] > maxScore:  #check if current event has a higher score than current max
                    maxScore = BSFHEvent[event]  #if so, set new max score
                    maxEvent = event                #record where new max came from
                elif BSFHEvent[event] == maxScore: # if event score ties with another event, add both to the dictionary
                    maxEvent.append(event)
            BSFHMap[mapNode] = [maxEvent, maxScore]      #set BSFH value of key
    return BSFHMap


def TraceChildren(DTL, GreedyOnce, BSFHMap, key):
    """This function takes as input a DTL graph, a dicitonary of a best reconciliation, a BSFHMap dicitonary, and a 
    current key. The function adds the children of that key to the dictionary, resets the scores of the associated events to 0, 
    then recurses on the children. The function returns a dictionary GreedyOnce that contains the best reconciliation, and 
    a dictionary resetDTL containing only keys from DTL whose values were changed when scores were reset."""

    resetDTL = {}
    reset1DTL = {}
    reset2DTL = {}
    child1 = GreedyOnce[key][1]
    child2 = GreedyOnce[key][2]

    if child1 != (None, None):
        GreedyOnce[child1] = BSFHMap[child1][0][0:3]
        for i in range(len(DTL[child1]) - 1):       #this loop resets to 0 all the scores of events that have been used
            if tuple(DTL[child1][i]) == BSFHMap[child1][0]:
                newValue = DTL[child1]
                newValue[i][-1] = 0
                reset1DTL[child1] = newValue
        newGreedyOnce, DTL1 = TraceChildren(DTL, GreedyOnce, BSFHMap, child1)
        reset1DTL.update(DTL1)
        GreedyOnce.update(newGreedyOnce)
    if child2 != (None, None):
        GreedyOnce[child2] = BSFHMap[child2][0][0:3]
        for i in range(len(DTL[child2]) - 1):
            if tuple(DTL[child2][i]) == BSFHMap[child2][0]:
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

    #reset score of the mapping node we used to 0:
    for i in range(len(DTL[bestKey]) - 1):                          #loop through the events associated with DTL
        if tuple(DTL[bestKey][i]) == BSFHMap[bestKey][0]:           #check if the event matches the event that gave the best score
            DTL[bestKey][i][-1] = 0                                 #set the score to 0

    newGreedyOnce, resetDTL = TraceChildren(DTL, GreedyOnce, BSFHMap, bestKey)
    GreedyOnce.update(newGreedyOnce)
    DTL.update(resetDTL)
    return GreedyOnce, DTL


def Greedy(DTL, ParasiteTree, k):
    """This function takes as input a DTL graph, a ParasiteTree, and k, the desired number of best reconciliation trees. 
    It returns TreeList, a list of k dictionaries, each of which represent one of the best trees."""

    TreeList = []
    currentDTL = DTL
    for i in range(k):
        oneTree, currentDTL = greedyOnce(currentDTL, ParasiteTree)
        TreeList.append(oneTree)
    return TreeList