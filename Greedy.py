

#Team Greedy

def findRoot(ParasiteTree):
    """This function takes in a parasiteTree and returns a string with the name of
    the root vertex of the tree"""

    ParasiteRoot = ParasiteTree['pTop'][1]
    return ParasiteRoot


#def orderDTLwrapper(DTL, ParasiteRoot):
    """This function takes in a DTL dictionary and a ParasiteRoot, and calls orderDTL with a level of 0. It returns a list, 
    keysL, that contains tuples. Each tuple has two elements. The first is a mapping node of the form (p, h), where p is a 
    parasite node and h is a host node. The second element is a level representing the depth of that mapping node within 
    the tree. This function loops through the DTL graph and recruses on the two children of each DTL mapping node, adding 
    the results to keysL."""

#    markingDict = initializeMarkingDict(DTL)
#    return orderDTL(DTL, ParasiteRoot, 0, markingDict)


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
    """this function takes a DTL graph, one node, vertex, of the DTL graph, a level, and a dictionary markingDict, and 
    returns a list, keysL, that contains tuples. Each tuple has two elements. The first is a mapping node of the form 
    (p, h), where p is a parasite node and h is a host node. The second element is a level representing the depth of 
    that mapping node within the tree. This function adds the input vertex to keysL and recurses on its children."""

    keysL = []
    for i in range(len(DTL[vertex]) - 1):          #loop through each event associated with key in DTL
        event = DTL[vertex][i]
        child1 = event[1]
        child2 = event[2]
        keysL = keysL + [(vertex, level)]
        if child1[0] != None:
            keysL.extend(orderDTLRoots(DTL, child1, level + 1))
        if child2[0] != None:
            keysL.extend(orderDTLRoots(DTL, child2, level + 1)) 
    return keysL



#def orderDTL(DTL, ParasiteRoot, level, markingDict):
    """This function takes in a DTL dictionary and a ParasiteRoot, and calls orderDTL with a level of 0. It returns a list, 
    keysL, that contains tuples. Each tuple has two elements. The first is a mapping node of the form (p, h), where p is a 
    parasite node and h is a host node. The second element is a level representing the depth of that mapping node within 
    the tree. This function loops through the DTL graph and recruses on the two children of each DTL mapping node, adding 
    the results to keysL."""

    """keysL = []
    for key in DTL:
        if markingDict[key] == False:
            if key[0] == ParasiteRoot:
                for i in range(len(DTL[key]) - 1):          #loop through each event associated with key in DTL
                    event = DTL[key][i]
                    child1 = event[1]
                    child2 = event[2]
                    if child1[0] == None and child2[0] == None:    #base case: mapping node (key) is a tip
                        keysL = keysL + [(key, level)]
                    elif child2[0] == None:                        #loss case: there is only one child (child1)
                        keysL = keysL + [(key, level)] + orderDTL(DTL, child1[0], level + 1, markingDict)
                    elif child1[0] == None:                        #loss case: there is only one child (child2)
                        keysL = keysL + [(key, level)] + orderDTL(DTL, child2[0], level + 1, markingDict)
                    else:
                        keysL = keysL + [(key, level)] + orderDTL(DTL, child1[0], level + 1, markingDict) + orderDTL(DTL, child2[0], level + 1, markingDict)
                markingDict[key] = True
    return keysL"""


def sortHelper(DTL, keysL):
    """This function takes in a list orderedKeysL and deals with duplicate mapping nodes that could potentially have the same level
    or have two different levels, in which case we want to choose the highest level becuase we are using the bottom-up approach"""
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
    #BSFHMap[(None, None)] = [0] 
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
                    #BSFHEvent[event] = BSFHMap[event[1]][-1] + BSFHMap[event[2]][-1] + event[-1]
                if BSFHEvent[event] > maxScore:  #check if current event has a higher score than current max
                    maxScore = BSFHEvent[event]  #if so, set new max score
                    maxEvent = list(event)                #record where new max came from
                elif BSFHEvent[event] == maxScore: # if event score ties with another event, add both to the dictionary
                    maxEvent.append(event)
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



#the one and only Vidua tree.

DTL = {('V._fischeri', 'G._ianthinogaster'): [['C', (None, None), (None, None), 49.0], 0], 
('p33', 'P._melba_citerior'): [['T', ('V._orientalis', 'P._melba_citerior'), ('p37', 'h83'), 115.0], 1], 
('p4', 'h64'): [['T', ('p6', 'h64'), ('p7', 'h105'), 20.0], 9], 
('p29', 'h54'): [['L', ('p29', 'E._astrild'), (None, None), 13.0], 2], 
('p116', 'C._monteiri'): [['T', ('V._larvaticola', 'C._monteiri'), ('p120', 'L._rara'), 9.0], 2], 
('V._funera', 'L._r._rubricata'): [['C', (None, None), (None, None), 49.0], 0], 
('p13', 'L._rhodopareia'): [['T', ('p21', 'L._rhodopareia'), ('V._funera', 'L._r._rubricata'), 34.0], 3], 
('p26', 'h76'): [['T', ('p28', 'h76'), ('p29', 'E._astrild'), 17.0], 4], 
('p10', 'L._senegala_rendalii'): [['T', ('p13', 'L._senegala_rendalii'), ('p12', 'h1'), 3.0], ['T', ('p13', 'L._senegala_rendalii'), ('p12', 'C._monteiri'), 3.0], ['T', ('p13', 'L._senegala_rendalii'), ('p12', 'L._rara'), 3.0], ['T', ('p13', 'L._senegala_rendalii'), ('p12', 'L._rufopicta'), 6.0], 8], 
('p3', 'E._astrild'): [['T', ('p5', 'E._astrild'), ('p4', 'h64'), 2.0], 15], 
('V._nigeriae', 'O._atricolis'): [['C', (None, None), (None, None), 49.0], 0], 
('V._chalybeata_W.', 'L._senegala_rhodopsis'): [['C', (None, None), (None, None), 49.0], 0], 
('p5', 'E._melpoda'): [['T', ('p26', 'E._melpoda'), ('V._hypocherina', 'E._erythronotos'), 2.0], 5], 
('p107', 'L._senegala_rendalii'): [['T', ('V._chalybeata_S.', 'L._senegala_rendalii'), ('V._codringtoni', 'H._niveoguttatus'), 32.0], 1], 
('p116', 'L._sanguinodorsalis'): [['T', ('p120', 'L._sanguinodorsalis'), ('V._larvaticola', 'C._monteiri'), 34.0], 2], 
('p15', 'L._rufopicta'): [['T', ('V._wilsoni', 'L._rufopicta'), ('p116', 'C._monteiri'), 3.0], ['T', ('V._wilsoni', 'L._rufopicta'), ('p116', 'L._rara'), 3.0], 3], 
('p21', 'L._rhodopareia'): [['T', ('V._purpurascens', 'L._rhodopareia'), ('p107', 'H._niveoguttatus'), 17.0], ['T', ('V._purpurascens', 'L._rhodopareia'), ('p107', 'L._senegala_rendalii'), 17.0], 2], 
('V._raricola', 'A._subflava'): [['C', (None, None), (None, None), 49.0], 0], 
('V._togoensis', 'P._hypogrammica'): [['C', (None, None), (None, None), 213.0], 0], 
('p3', 'h51'): [['T', ('p5', 'h51'), ('p4', 'h64'), 4.0], 15], 
('V._interjecta', 'P._phoenicoptera'): [['C', (None, None), (None, None), 213.0], 0], 
('p5', 'h51'): [['S', ('p26', 'h54'), ('V._hypocherina', 'E._erythronotos'), 26.0], 5], 
('p3', 'E._melpoda'): [['T', ('p5', 'E._melpoda'), ('p4', 'h64'), 2.0], 15], 
('V._camerunensis', 'L._rara'): [['C', (None, None), (None, None), 49.0], 0], 
('p26', 'h54'): [['T', ('p29', 'h54'), ('p28', 'h76'), 13.0], ['L', ('p26', 'E._astrild'), (None, None), 13.0], 5], 
('V._wilsoni', 'L._rufopicta'): [['C', (None, None), (None, None), 49.0], 0], 
('p3', 'h105'): [['T', ('p4', 'h105'), ('p5', 'h51'), 4.0], ['T', ('p4', 'h105'), ('p5', 'h76'), 2.0], 15], 
('p7', 'h91'): [['S', ('p10', 'L._senegala_rendalii'), ('V._chalybeata_W.', 'L._senegala_rhodopsis'), 15.0], 8], 
('p29', 'E._melpoda'): [['T', ('V._macroura_W.', 'E._melpoda'), ('V._macroura_S', 'E._astrild'), 2.0], 1], 
('p120', 'L._rara'): [['T', ('V._camerunensis', 'L._rara'), ('V._maryae', 'L._sanguinodorsalis'), 15.0], 1], 
('p32', 'P._melba_grotei'): [['T', ('V._paradisaea', 'P._melba_grotei'), ('V._obtusa', 'P._afra'), 115.0], 1], 
('p7', 'L._senegala_rhodopsis'): [['T', ('V._chalybeata_W.', 'L._senegala_rhodopsis'), ('p10', 'h105'), 6.0], 8], 
('p13', 'L._senegala_rendalii'): [['T', ('p21', 'L._senegala_rendalii'), ('V._funera', 'L._r._rubricata'), 15.0], 3], 
('V._hypocherina', 'E._erythronotos'): [['C', (None, None), (None, None), 49.0], 0], 
('p29', 'E._astrild'): [['T', ('V._macroura_S', 'E._astrild'), ('V._macroura_W.', 'E._melpoda'), 64.0], 1], 
('V._codringtoni', 'H._niveoguttatus'): [['C', (None, None), (None, None), 49.0], 0], 
('p12', 'L._rufopicta'): [['T', ('p15', 'L._rufopicta'), ('p118', 'h1'), 6.0], 4], 
('p12', 'h1'): [['T', ('p118', 'h1'), ('p15', 'C._monteiri'), 3.0], 4], 
('V._macroura_S', 'E._astrild'): [['C', (None, None), (None, None), 130.0], 0], 
('p6', 'h64'): [['S', ('V._fischeri', 'G._ianthinogaster'), ('V._regia', 'G._granatia'), 49.0], 0], 
('V._chalybeata_S.', 'L._senegala_rendalii'): [['C', (None, None), (None, None), 49.0], 0], 
('p118', 'h1'): [['S', ('V._nigeriae', 'O._atricolis'), ('V._raricola', 'A._subflava'), 49.0], 0], 
('p28', 'h76'): [['S', ('p32', 'P._melba_grotei'), ('p33', 'P._melba_citerior'), 66.0], 2], 
('V._paradisaea', 'P._melba_grotei'): [['C', (None, None), (None, None), 164.0], 0], 
('p15', 'L._sanguinodorsalis'): [['T', ('p116', 'L._sanguinodorsalis'), ('V._wilsoni', 'L._rufopicta'), 34.0], 3], 
('p5', 'E._astrild'): [['T', ('p26', 'E._astrild'), ('V._hypocherina', 'E._erythronotos'), 2.0], 5], 
('p5', 'h76'): [['T', ('p26', 'h76'), ('V._hypocherina', 'E._erythronotos'), 15.0], 5], 
('p3', 'h91'): [['T', ('p4', 'h91'), ('p5', 'h51'), 10.0], ['T', ('p4', 'h91'), ('p5', 'h76'), 5.0], 15], 
('V._maryae', 'L._sanguinodorsalis'): [['C', (None, None), (None, None), 49.0], 0], 
('p10', 'h105'): [['S', ('p13', 'L._rhodopareia'), ('p12', 'L._sanguinodorsalis'), 34.0], 7], 
('p26', 'E._astrild'): [['T', ('p29', 'E._astrild'), ('p28', 'h76'), 17.0], 4], 
('p5', 'E._erythronotos'): [['T', ('V._hypocherina', 'E._erythronotos'), ('p26', 'h76'), 2.0], ['T', ('V._hypocherina', 'E._erythronotos'), ('p26', 'E._astrild'), 2.0], 5], 
('p4', 'h91'): [['T', ('p7', 'h91'), ('p6', 'h64'), 15.0], 9], 
('p3', 'E._erythronotos'): [['T', ('p5', 'E._erythronotos'), ('p4', 'h64'), 4.0], 15], 
('p15', 'C._monteiri'): [['T', ('p116', 'C._monteiri'), ('V._wilsoni', 'L._rufopicta'), 6.0], 3], 
('V._orientalis', 'P._melba_citerior'): [['C', (None, None), (None, None), 164.0], 0], 
('p12', 'L._rara'): [['T', ('p15', 'L._rara'), ('p118', 'h1'), 3.0], 4], 
('V._macroura_W.', 'E._melpoda'): [['C', (None, None), (None, None), 130.0], 0], 
('V._larvaticola', 'C._monteiri'): [['C', (None, None), (None, None), 49.0], 0], 
('p3', 'h76'): [['T', ('p5', 'h76'), ('p4', 'h64'), 2.0], ['T', ('p5', 'h76'), ('p4', 'h105'), 2.0], 15], 
('p107', 'H._niveoguttatus'): [['T', ('V._codringtoni', 'H._niveoguttatus'), ('V._chalybeata_S.', 'L._senegala_rendalii'), 17.0], 1], 
('p7', 'h105'): [['T', ('p10', 'h105'), ('V._chalybeata_W.', 'L._senegala_rhodopsis'), 28.0], 8], 
('p116', 'L._rara'): [['T', ('p120', 'L._rara'), ('V._larvaticola', 'C._monteiri'), 6.0], 2], 
('p120', 'L._sanguinodorsalis'): [['T', ('V._maryae', 'L._sanguinodorsalis'), ('V._camerunensis', 'L._rara'), 34.0], 1], 
('p21', 'L._senegala_rendalii'): [['T', ('p107', 'L._senegala_rendalii'), ('V._purpurascens', 'L._rhodopareia'), 15.0], 2], 
('p4', 'L._senegala_rhodopsis'): [['T', ('p7', 'L._senegala_rhodopsis'), ('p6', 'h64'), 6.0], 9], 
('V._obtusa', 'P._afra'): [['C', (None, None), (None, None), 164.0], 0], 
('V._regia', 'G._granatia'): [['C', (None, None), (None, None), 49.0], 0], 
('V._purpurascens', 'L._rhodopareia'): [['C', (None, None), (None, None), 49.0], 0], 
('p15', 'L._rara'): [['T', ('p116', 'L._rara'), ('V._wilsoni', 'L._rufopicta'), 3.0], 3], 
('p37', 'h83'): [['S', ('V._interjecta', 'P._phoenicoptera'), ('V._togoensis', 'P._hypogrammica'), 164.0], 0], 
('p26', 'E._melpoda'): [['T', ('p29', 'E._melpoda'), ('p28', 'h76'), 2.0], 4], 
('p12', 'C._monteiri'): [['T', ('p15', 'C._monteiri'), ('p118', 'h1'), 3.0], 4], 
('p3', 'L._senegala_rhodopsis'): [['T', ('p4', 'L._senegala_rhodopsis'), ('p5', 'h51'), 4.0], ['T', ('p4', 'L._senegala_rhodopsis'), ('p5', 'h76'), 2.0], 15], 
('p3', 'h64'): [['T', ('p4', 'h64'), ('p5', 'h51'), 4.0], ['T', ('p4', 'h64'), ('p5', 'h76'), 2.0], 15], 
('p4', 'h105'): [['T', ('p7', 'h105'), ('p6', 'h64'), 8.0], 9], 
('p12', 'L._sanguinodorsalis'): [['T', ('p15', 'L._sanguinodorsalis'), ('p118', 'h1'), 34.0], 4]}

P = {('p4', 'p6'): ('p4', 'p6', ('p6', 'V._fischeri'), ('p6', 'V._regia')), 
('p5', 'V._hypocherina'): ('p5', 'V._hypocherina', None, None), 
('p6', 'V._regia'): ('p6', 'V._regia', None, None), 
('p7', 'p10'): ('p7', 'p10', ('p10', 'p12'), ('p10', 'p13')), 
('p33', 'p37'): ('p33', 'p37', ('p37', 'V._interjecta'), ('p37', 'V._togoensis')), 
('p15', 'V._wilsoni'): ('p15', 'V._wilsoni', None, None), 
('p107', 'V._chalybeata_S.'): ('p107', 'V._chalybeata_S.', None, None), 
('p6', 'V._fischeri'): ('p6', 'V._fischeri', None, None), 
('p5', 'p26'): ('p5', 'p26', ('p26', 'p28'), ('p26', 'p29')), 
('p28', 'p33'): ('p28', 'p33', ('p33', 'V._orientalis'), ('p33', 'p37')), 
('p118', 'V._nigeriae'): ('p118', 'V._nigeriae', None, None), 
('p13', 'p21'): ('p13', 'p21', ('p21', 'V._purpurascens'), ('p21', 'p107')), 
('p12', 'p15'): ('p12', 'p15', ('p15', 'p116'), ('p15', 'V._wilsoni')), 
('p4', 'p7'): ('p4', 'p7', ('p7', 'p10'), ('p7', 'V._chalybeata_W.')), 
('p37', 'V._togoensis'): ('p37', 'V._togoensis', None, None), 
('p26', 'p28'): ('p26', 'p28', ('p28', 'p32'), ('p28', 'p33')), 
'pTop': ('Top', 'p3', ('p3', 'p4'), ('p3', 'p5')), 
('p32', 'V._obtusa'): ('p32', 'V._obtusa', None, None), 
('p28', 'p32'): ('p28', 'p32', ('p32', 'V._paradisaea'), ('p32', 'V._obtusa')), 
('p3', 'p5'): ('p3', 'p5', ('p5', 'p26'), ('p5', 'V._hypocherina')), 
('p29', 'V._macroura_W.'): ('p29', 'V._macroura_W.', None, None), 
('p7', 'V._chalybeata_W.'): ('p7', 'V._chalybeata_W.', None, None), 
('p116', 'V._larvaticola'): ('p116', 'V._larvaticola', None, None), 
('p120', 'V._camerunensis'): ('p120', 'V._camerunensis', None, None), 
('p10', 'p12'): ('p10', 'p12', ('p12', 'p118'), ('p12', 'p15')), 
('p116', 'p120'): ('p116', 'p120', ('p120', 'V._camerunensis'), ('p120', 'V._maryae')), 
('p26', 'p29'): ('p26', 'p29', ('p29', 'V._macroura_S'), ('p29', 'V._macroura_W.')), 
('p32', 'V._paradisaea'): ('p32', 'V._paradisaea', None, None), 
('p21', 'p107'): ('p21', 'p107', ('p107', 'V._chalybeata_S.'), ('p107', 'V._codringtoni')), 
('p15', 'p116'): ('p15', 'p116', ('p116', 'p120'), ('p116', 'V._larvaticola')), 
('p3', 'p4'): ('p3', 'p4', ('p4', 'p6'), ('p4', 'p7')), 
('p37', 'V._interjecta'): ('p37', 'V._interjecta', None, None), 
('p33', 'V._orientalis'): ('p33', 'V._orientalis', None, None), 
('p10', 'p13'): ('p10', 'p13', ('p13', 'V._funera'), ('p13', 'p21')), 
('p120', 'V._maryae'): ('p120', 'V._maryae', None, None), 
('p12', 'p118'): ('p12', 'p118', ('p118', 'V._nigeriae'), ('p118', 'V._raricola')), 
('p107', 'V._codringtoni'): ('p107', 'V._codringtoni', None, None), 
('p21', 'V._purpurascens'): ('p21', 'V._purpurascens', None, None), 
('p13', 'V._funera'): ('p13', 'V._funera', None, None), 
('p118', 'V._raricola'): ('p118', 'V._raricola', None, None), 
('p29', 'V._macroura_S'): ('p29', 'V._macroura_S', None, None)}
