

#Team Srinidhi and Juliet

#Our goal is to find the k best reconciliatioins

#We are given a DTL reconciliation graph in the form of dictionaries

#Dict1: the values of the DTl graphs will be modified to hold the BSFH scores

#Keeping track of bookkeeping

#key: mapping node
#value: List of (0) max (1) where the max came from


def preorder(Tree, rootEdgeName):
    """ Takes a tree as input (see format description above) and returns
        a list of the edges in that tree in preorder (high edges to low edges)"""

    value = Tree[rootEdgeName]
    leftChildEdgeName = value[2]
    rightChildEdgeName = value[3]
    # base case
    if leftChildEdgeName == None: # then rightChildEdgeName == None also
        return [rootEdgeName]
    else:
        return [rootEdgeName] + \
                preorder(Tree, leftChildEdgeName) + \
                preorder(Tree, rightChildEdgeName)

def postorder(Tree, rootEdgeName):
    """ Takes a tree as input (see format description above) and returns
        a list of the edges in that tree in postorder (low edges to high edges)"""

    value = Tree[rootEdgeName]
    leftChildEdgeName = value[2]
    rightChildEdgeName = value[3]
    # base case
    if leftChildEdgeName == None: # then rightChildEdgeName == None also
        return [rootEdgeName]
    else:
        return postorder(Tree, leftChildEdgeName) + \
               postorder(Tree, rightChildEdgeName) + \
               [rootEdgeName]

def findRoot(Tree):
    root = Tree['pTop'][1]
    return root


def postorderDTLwrapper(DTL, ParasiteRoot):
    postorderDTL(DTL, ParasiteTree, 0)

def postorderDTL(DTL, ParasiteRoot, level):

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
    orderedKeysL = []
    levelCounter = 0
    while len(orderedKeysL) < len(keysL):
        for mapping in keysL:
            if mapping[-1] == levelCounter:
                orderedKeysL = [mapping] + orderedKeysL

    return orderedKeysL


     

def bookkeeping(DTL, ParasiteTree):
    """This function inputs the DTL graph and then records what the max is at each mapping node and 
    where the max came from so outputs BSFH"""

    #BSFHMap = {(mapping node): [['event', (vertex), (vertex), prob], maxProb]}
    #BSFHEvent = {(event node): max}

    #PROBTIP = 1

    BSFHMap = {}
    BSFHEvent = {}

    BSFHMap[None] = 0

    orderedKeys = postorderDTLsort(postorderDTLwrapper(DTL, ParasiteTree))

    for key in orderedKeys:
        if DTL[key[0]][0][0] == 'C':                   #check if the key is a tip
           BSFHMap[key] = [DTL[key][0], 1]    #set BSFH of tip to some global variable (1 should be PROBTIP)
        else:                                       #if key isn't a tip:
            maxProb = 0                             #initialize counter
            maxEvent = []                           #initialize variable to keep track of where max came from
            for i in range(length(DTL[key]) - 1):   #iterate through the events associated with the key node
                event = DTL[key][i]                 #set variable name that makes sense
                BSFHEvent[event] = BSFHMap[event[1]] + BSFHMap[event[2]]
                if BSFHEvent[event][-1] > maxProb:  #check if current event has a higher prob than current max
                    maxProb = BSFHEvent[event][-1]  #if so, set new max prob
                    maxEvent = event                #record where new max came from
            BSFHMap[key] = [maxEvent, maxProb]      #set BSFH value of key

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
            






























