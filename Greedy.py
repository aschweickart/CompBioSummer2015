

#Team Srinidhi and Juliet

#Our goal is to find the k best reconciliations

def findRoot(ParasiteTree):
    """This function takes in a parasiteTree and returns a string with the name of
    the root vertex of the tree"""
    ParasiteRoot = ParasiteTree['pTop'][1]
    return ParasiteRoot


def orderDTLwrapper(DTL, ParasiteRoot):
    """This wrapper function uses orderDTL and starts with a level of 0. Returns keysL."""
    orderDTL(DTL, ParasiteRoot, 0)

def orderDTL(DTL, ParasiteRoot, level):
    """This function takes in a DTL dictionary, a ParasiteRoot, and a level that represents the depth of 
    the of a vertex pair. It returns a list, keysL, that includes tuples with the first 
    elements being a mapping node of the form (p, h), and the second element being the depth of that node within 
    the graph. This function loops through the DTL graph and recruses on the two children of each DTL 
    mapping node, adding the results to keysL"""

    keysL = []
    for key in DTL:
        if key[0] == ParasiteRoot:
            for i in range(len(DTL[key]) - 1):          #loop through each event associated with key in DTL
                event = DTL[key][i]
                child1 = event[1]
                child2 = event[2]
                if child1[0] == None and child2[0] == None:    #base case: mapping node (key) is a tip
                    keysL = keysL + [(key, level)]
                elif child2[0] == None:                        #loss case: there is only one child (child1)
                    keysL = keysL + [(key, level)] + [orderDTL(DTL, child1[0], level + 1)]
                else:                                          #loss case: there is only one child (child2)
                    keysL = keysL + [(key, level)] + [orderDTL(DTL, child2[0], level + 1)]
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
                orderedKeysL = [mapping] + orderedKeysL
                levelCounter += 1
    return orderedKeysL


     

def bookkeeping(DTL, ParasiteTree):
    """This function inputs the DTL graph and ParasiteTree, and then records what the max is at each mapping node and 
    where the max came from. It outputs two dictionaries BSFHMap and BSFHEvent, by looping through the keys in orderedKeysL 
    and finding the max score at each mapping node and event node"""

    """We are creating two dictionaries. BSFHMap has keys of the form (p, h) which are the mapping nodes, and values
    which are lists where the first element is a list of events with the max score, and the last element is the max score.
    BSFHEvent is a dictionary with events as keys, and values which are one number which is the max score."""

    #BSFHMap = {(mapping node): [['event', (p, h), (p, h), score], maxScore]}
    #BSFHEvent = {(event node): max}

    TIPSCORE = 1 #this will change depending on how we define the score for tips

    BSFHMap = {}
    BSFHEvent = {}

    BSFHMap[(None, None)] = 0           #BSFH value for empty children is 0

    ParasiteRoot = findRoot(ParasiteTree)

    orderedKeys = postorderDTLsort(DTL, ParasiteRoot)

    for key in orderedKeys:
        if DTL[key[0]][0][0] == 'C':                   #check if the key is a tip
           BSFHMap[key] = [DTL[key][0], TIPSCORE]    #set BSFH of tip to some global variable
        else:                                       #if key isn't a tip:
            maxScore = 0                             #initialize counter
            maxEvent = []                           #initialize variable to keep track of where max came from
            for i in range(length(DTL[key]) - 1):   #iterate through the events associated with the key node
                event = DTL[key][i]
                BSFHEvent[event] = BSFHMap[event[1]] + BSFHMap[event[2]]
                if BSFHEvent[event][-1] > maxScore:  #check if current event has a higher score than current max
                    maxScore = BSFHEvent[event][-1]  #if so, set new max score
                    maxEvent = event                #record where new max came from
                elif BSFHEvent[event][-1] == maxScore: # if event score ties with another event, add both to the dictionary
                    maxEvent.append(event)
            BSFHMap[key] = [maxEvent, maxScore]      #set BSFH value of key

    return BSFHMap, BSFHEvent

        


def greedy(DTL, k):
    """This function inputs the DTL and k, and calls bokkeeping to find BSFHMap and BSFHEvent,
    which are both dictionaries. Greedy is also going to reset the BSFH scores to 0 and then call
    bookkeeping with the new DTL. We do this k times""" 

    for i in range(k):
        """we find the max"""
        BSFHMap, BSFHEvent = bookkeeping(DTL)

        bestKey = ''
        bestScore = 0
        for key in BSFH:
            if BSFH[key][0] > bestScore:
                bestKey = key
                bestScore = BSFH[key][0]
            






























