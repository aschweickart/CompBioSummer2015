

#Team Srinidhi and Juliet

#Our goal is to find the k best reconciliatioins

#We are given a DTL reconciliation graph in the form of dictionaries

#Dict1: the values of the DTl graphs will be modified to hold the BSFH scores

#Keeping track of bookkeeping

#key: mapping node
#value: List of (0) max (1) where the max came from


def findRoot(parasiteTree):
    """This function takes in a parasiteTree and returns a string with the name of
    the root vertex of the tree"""
    root = parasiteTree['pTop'][1]
    return root


def postorderDTLwrapper(DTL, ParasiteRoot):
    """This wrapper function uses postorderDTL and starts with a level of 0"""
    postorderDTL(DTL, ParasiteTree, 0)

def postorderDTL(DTL, ParasiteRoot, level):
    """This function takes in a DTL dictionary, a ParasiteRoot, and a level that represents the depth of 
    the of a vertex pair. This postorder function returns a list, keysL, that includes tuples with the first 
    elements being a mapping node of the form (p, h), and the second element the depth of that node within 
    the graph. This function loops through the DTL graph and recruses on the two children of the DTL 
    mapping node."""

    keysL = []
    print ParasiteRoot
    for key in DTL:
        if key[0] == ParasiteRoot:
            for i in range(len(DTL[key]) - 1):
                event = DTL[key][i]
                child1 = event[1]
                child2 = event[2]
                if child1[0] == None and child2[0] == None:
                    keysL = keysL + [(key, level)]
                elif child2[0] == None:
                    keysL = keysL + [(key, level)] + [postorderDTL(DTL, child1[0], level + 1)]
                else:
                    keysL = keysL + [(key, level)] + [postorderDTL(DTL, child2[0], level + 1)]

    return keysL

def postorderDTLsort(keysL):
    """This takes in the output list of postorderDTL and returns a sorted list, orderedKeysL, that is ordered
    by level from largest to smallest."""
    orderedKeysL = []
    levelCounter = 0
    while len(orderedKeysL) < len(keysL):
        for mapping in keysL:
            if mapping[-1] == levelCounter:
                orderedKeysL = [mapping] + orderedKeysL

    return orderedKeysL


     

def bookkeeping(DTL, ParasiteRoot):
    """This function inputs the DTL graph and ParasiteTree, and then records what the max is at each mapping node and 
    where the max came from. It outputs two dictionaries BSFHMap, and BSFHEvent, by looping through the keys in orderedKeysL and 
    finding the max score at each mapping node and event node"""

    """We are creating two dictionaries. BSFHMap has keys of the form (p, h) which are the mapping nodes, and values
    which are lists of length """

    #BSFHMap = {(mapping node): [['event', (p, h), (p, h), score], maxScore]}
    #BSFHEvent = {(event node): max}

    #PROBTIP = 1

    BSFHMap = {}
    BSFHEvent = {}

    BSFHMap[None] = 0

    orderedKeys = postorderDTLsort(postorderDTLwrapper(DTL, ParasiteRoot))

    for key in orderedKeys:
        if DTL[key[0]][0][0] == 'C':                   #check if the key is a tip
           BSFHMap[key] = [DTL[key][0], 1]    #set BSFH of tip to some global variable (1 should be PROBTIP)
        else:                                       #if key isn't a tip:
            maxScore = 0                             #initialize counter
            maxEvent = []                           #initialize variable to keep track of where max came from
            for i in range(length(DTL[key]) - 1):   #iterate through the events associated with the key node
                event = DTL[key][i]                 #set variable name that makes sense
                BSFHEvent[event] = BSFHMap[event[1]] + BSFHMap[event[2]]
                if BSFHEvent[event][-1] > maxScore:  #check if current event has a higher prob than current max
                    maxScore = BSFHEvent[event][-1]  #if so, set new max prob
                    maxEvent = event                #record where new max came from
            BSFHMap[key] = [maxEvent, maxScore]      #set BSFH value of key

    return BSFHMap, BSFHEvent

        


def greedy(DTL, k):
    """This function inputs the BSFH, DTL and k, and calls bokkeeping to find the best k reconciliations,
    which is represented in a dictionary. Greedy is also going to reset the BSFH scores to 0 and then call
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
            






























