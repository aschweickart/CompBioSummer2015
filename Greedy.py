# Greedy.py
# Srinidhi Srinivasan, Juliet Forman
# June 2015

# This file contains the functions for finding all optimal reconciliations 
# using a DTL reconciliation graph, as well as the scores for each of the events using the
# vertex-based DP algorithm. The main function in this file is called Greedy
# and the remaining functions are helper functions that are used by Greedy.


def findRoot(tree):
    """This function takes in a parasite tree or a host treeand returns a string with the 
    name of the root vertex of the tree"""

    if 'pTop' in tree:
        return tree['pTop'][1]
    return tree['hTop'][1] 

def orderDTLReconGraph(DTLReconGraph, parasiteRoot):
    """This function takes in a DTL reconciliation graph and the parasiteRoot. It outputs a 
    list, keysL, that contains tuples. Each tuple has two elements. The first
    is a mapping node of the form (p, h), where p is a parasite node and h is 
    a host node. The second element is a level representing the depth of that
    mapping node within the tree."""

    keysL = []
    topNodes = []
    for key in DTLReconGraph:
        if key[0] == parasiteRoot:
            topNodes.append(key)
    for vertex in topNodes:
        keysL.extend(orderDTLReconGraphRoots(DTLReconGraph, vertex, 0))
    return keysL

def orderDTLReconGraphRoots(DTLReconGraph, vertex, level):
    """This function takes a DTL reconciliation graph, one node, a vertex, of the DTL reconciliation graph, 
    and level, and returns a list, keysL, that contains tuples. Each tuple has
    two elements. The first is a mapping node of the form (p, h), where p is a
    parasite node and h is a host node. The second element is a level 
    representing the depth of that mapping node within the tree. This function
    adds the input vertex to keysL and recurses on its children."""

    keysL = []
    #loop through each event associated with key in DTLReconGraph
    for event in DTLReconGraph[vertex][:-1]:
        _, child1, child2, _ = event
        keysL = keysL + [(vertex, level)]
        if child1[0] != None:
            keysL.extend(orderDTLReconGraphRoots(DTLReconGraph, child1, level + 1))
        if child2[0] != None:
            keysL.extend(orderDTLReconGraphRoots(DTLReconGraph, child2, level + 1)) 
    return keysL


def sortHelper(DTLReconGraph, keysL):
    """This function takes in a list keysL, where the keys are mapping nodes and the values are the level that represents the depth of that mapping node within the tree, and a DTL reconciliation graph, and returns a new 
    list, uniqueKeysL that has removed duplicate mapping nodes from keysL.
    This function chooses the highest level for each mapping node because we 
    are using the bottom-up approach."""
    
    uniqueKeysL = []
    for key in DTLReconGraph:
        maxLevel = float("-inf")
        for mapping in keysL:
            if key == mapping[0]:
                if mapping[1] > maxLevel:
                    maxLevel = mapping[1]
        uniqueKeysL.append((key, maxLevel))
    return uniqueKeysL


def postorderDTLReconGraphSort(DTLReconGraph, parasiteRoot):
    """This function takes in a DTL reconciliation graph and parasiteRoot, and returns a 
    sorted list, orderedKeysL, that is ordered by level from largest to 
    smallest, where level 0 is the root and the highest level are tips."""

    keysL = orderDTLReconGraph(DTLReconGraph, parasiteRoot)
    uniqueKeysL = sortHelper(DTLReconGraph, keysL)
    orderedKeysL = []
    levelCounter = 0
    while len(orderedKeysL) < len(uniqueKeysL):
        for mapping in uniqueKeysL:
            if mapping[-1] == levelCounter:
                orderedKeysL = [mapping] + orderedKeysL
        levelCounter += 1
    return orderedKeysL


def BSFHAlgorithm(DTLReconGraph, parasiteTree):
    """This function takes as inputs a DTL reconciliation graph and parasiteTree, and then 
    records what the max is at each mapping node and which event the max came 
    from. It outputs a dictionary BSFHMap by looping through the keys in a 
    sorted list of mapping nodes and finding the max score at each mapping 
    node and event node. BSFHMap has keys of the form (p, h) which are the 
    mapping nodes, and values which are lists where the first element is an 
    event with the max score, and the last element is the maxScore. Note that BSFH stands for Best Score From Here"""

    #Example: BSFHMap = {(mapping node): [['event', (p, h), (p, h), score], 
    #                                                               maxScore]}
    #Example: BSFHEvent = {(event node): max}

    BSFHMap = {}
    BSFHEvent = {}
    parasiteRoot = findRoot(parasiteTree)
    orderedKeysL = postorderDTLReconGraphSort(DTLReconGraph, parasiteRoot)   
    for key in orderedKeysL:
        mapNode = key[0]
        #check if the key is a tip:
        if DTLReconGraph[mapNode][0][0] == 'C':              
            BSFHMap[mapNode] = [DTLReconGraph[mapNode][0], DTLReconGraph[mapNode][0][-1]]
        #if the key isn't a tip:
        else: 
            #initialize counter                                    
            maxScore = float("-inf")  
            #initialize variable to keep track of where max came from
            maxEvent = [] 
            #iterate through the events associated with the key node
            for i in range(len(DTLReconGraph[mapNode])-1):
                event = tuple(DTLReconGraph[mapNode][i])
                BSFHEvent[event] = event[-1]
                if event[1] != (None, None):
                    BSFHEvent[event] = BSFHEvent[event]+BSFHMap[event[1]][-1]
                if event[2] != (None, None):
                    BSFHEvent[event] = BSFHEvent[event]+BSFHMap[event[2]][-1]
                #check if current event has a higher score than current max
                if BSFHEvent[event] > maxScore:  
                    maxScore = BSFHEvent[event]  #set new max score
                    maxEvent = list(event)   #record where new max came from
            BSFHMap[mapNode] = [maxEvent, maxScore]  #set BSFH value of key
    return BSFHMap


def traceChildren(DTLReconGraph, GreedyOnce, BSFHMap, key):
    """This function takes as input a DTL reconciliation graph, a dictionary GreedyOnce, 
    containing the root of an optimal reconciliation, a BSFHMap dicitonary, 
    and a current key, and returns the optimal reconciliation and new DTLReconGraph 
    graph, where the scores of the events in the reconciliation are reset to
    0."""

    resetDTLReconGraph = {} #the new DTLReconGraph graph
    reset1DTLReconGraph = {} #this DTLReconGraph graph deals with the recursive call on the child1
    reset2DTLReconGraph = {} #this DTLReconGraph graph deals with the recursive call on the child2
    _, child1, child2 = GreedyOnce[key]
    if child1 != (None, None):
        GreedyOnce[child1] = BSFHMap[child1][0][0:3] #add event to greedyOnce
        #this loop resets all the scores of events that have been used to 0 
        for index in range(len(DTLReconGraph[child1]) - 1):       
            if DTLReconGraph[child1][index] == BSFHMap[child1][0]:
                newValue = DTLReconGraph[child1]
                newValue[index][-1] = 0
                reset1DTLReconGraph[child1] = newValue
        #this recursive call updates GreedyOnce and the DTL reconciliation graph
        newGreedyOnce, DTLReconGraph1 = traceChildren(DTLReconGraph, GreedyOnce, BSFHMap, child1) 
        reset1DTLReconGraph.update(DTLReconGraph1) #update the dictionary to contain info about child1
        GreedyOnce.update(newGreedyOnce) # update the reconciliation
    if child2 != (None, None):
        GreedyOnce[child2] = BSFHMap[child2][0][0:3] #add event to greedyOnce
        #this loop resets all the scores of events that have been used to 0
        for index in range(len(DTLReconGraph[child2]) - 1): 
            if DTLReconGraph[child2][index] == BSFHMap[child2][0]:
                newValue = DTLReconGraph[child2]
                newValue[index][-1] = 0
                reset2DTLReconGraph[child2] = newValue    
        # this recursive call updates GreedyOnce and the DTL reconciliation graph  
        newGreedyOnce, DTLReconGraph2 = traceChildren(DTLReconGraph, GreedyOnce, BSFHMap, child2)
        reset2DTLReconGraph.update(DTLReconGraph2) # update dictionary to contain info about child2
        GreedyOnce.update(newGreedyOnce) #update the reconciliation
    resetDTLReconGraph.update(reset1DTLReconGraph) # update the new DTL reconciliation graph
    resetDTLReconGraph.update(reset2DTLReconGraph) # update the new DTL reconciliation graph
    return GreedyOnce, resetDTLReconGraph


def greedyOnce(DTLReconGraph, parasiteTree):
    """This function takes the DTLReconGraph graph and the parasiteTree as inputs, and 
    calls BSFHAlgorithm to find the dictionary BSFHMap. It returns the 
    reconciliation with the highest score in a dictionary called GreedyOnce, 
    and also resets to 0 the scores of the mapping nodes in the optimal 
    reconciliation. The returned dictionary will have keys which are the 
    mapping nodes in the optimal reconciliation, and values of the form 
    (event, child1, child2)."""

    BSFHMap = BSFHAlgorithm(DTLReconGraph, parasiteTree)
    parasiteRoot = findRoot(parasiteTree)
    GreedyOnce = {}            #initialize dictionary we will return
    bestKey = ()       #variable to hold the key with the highers BSFH value
    bestScore = float("-inf") #variable to hold the highest BSFH value so far
    #iterate trough all the keys (verteces) in BSFHMap
    for key in BSFHMap:   
        #check if key has a score higher than bestScore and includes PRoot
        if BSFHMap[key][-1] > bestScore and key[0] == parasiteRoot: 
            bestKey = key
            bestScore = BSFHMap[key][-1]
    #set value in GreedyOnce of the best key we found
    GreedyOnce[bestKey] = BSFHMap[bestKey][0][0:3]   #index from 0 to 3 because we amputate the score from DTLReconGraph               
    
    #reset score of the mapping node we used to 0:

    #loop through the events associated with DTLReconGraph
    for index in range(len(DTLReconGraph[bestKey]) - 1):  
        #check if the event matches the event that gave the best score                      
        if DTLReconGraph[bestKey][index] == BSFHMap[bestKey][0]:           
            newEvent = DTLReconGraph[bestKey][index][:-1] + [0] #indexing updates event in DTL and puts it back in place
            newValue = DTLReconGraph[bestKey][:index] + [newEvent] + DTLReconGraph[bestKey][index + 1:]
            DTLReconGraph[bestKey] = newValue      #set the score to 0
    newGreedyOnce, resetDTLReconGraph = traceChildren(DTLReconGraph, GreedyOnce, BSFHMap, bestKey)
    GreedyOnce.update(newGreedyOnce)
    DTLReconGraph.update(resetDTLReconGraph)
    return GreedyOnce, DTLReconGraph, bestScore

def Greedy(DTLReconGraph, parasiteTree):
    """This function takes as input a DTL reconciliation graph and a parasiteTree, and 
    returns TreeList, a list of dictionaries, each of which represent one of 
    the optimal reconciliations. This function runs till all the scores have 
    been collected from the DTL reconciliation graph."""
    scores = [] #list of reconciliation scores
    currentDTLReconGraph = DTLReconGraph
    rec = [] #list of reconciliations
    collected = True
    while collected:
        #call greedyOnce if all the points have not been collected yet
        oneTree, currentDTLReconGraph, score = greedyOnce(currentDTLReconGraph, parasiteTree)
        scores.append(score) 
        rec.append(oneTree)
        collected = False #set collected to False
        #iterate to see if more points need to be collected
        for key in currentDTLReconGraph:
            for node in currentDTLReconGraph[key][:-1]:
                if node[-1] != 0:
                    collected = True

    return scores, rec


