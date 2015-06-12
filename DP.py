# DP.py
# Ran Libeskind-Hadas, June 2015
# The basic DP algorithm for reconciling pairs of trees


# A tree is represented as a dictionary of key-value pairs where a key is an
# edge name and the value is a tuple of the form
# (start vertex, end vertex, left child edge name, right child edge name)
# An edge name may be None.  The "dummy" edge leading to the root of the
# parasite tree, denoted e^P in the technical report, must be named "pTop".

import newickFormatReader
import DrawDTLc

H = {('h6', 'h8'): ('h6', 'h8', ('h8', 'h3'), ('h8', 'h4')), ('h8', 'h3'): \
('h8', 'h3', None, None), ('h6', 'h7'): ('h6', 'h7', ('h7', 'h1'), ('h7', 'h2')), 'hTop': \
('Top', 'h6', ('h6', 'h7'), ('h6', 'h8')), ('h7', 'h2'): ('h7', 'h2', None, None), ('h8', 'h4'): \
('h8', 'h4', None, None), ('h7', 'h1'): ('h7', 'h1', None, None)}
P = {('p6', 'p8'): ('p6', 'p8', ('p8', 'p3'), ('p8', 'p4')), ('p7', 'p2'): ('p7', 'p2', None, None), \
('p6', 'p7'): ('p6', 'p7', ('p7', 'p1'), ('p7', 'p2')), ('p8', 'p4'): ('p8', 'p4', None, None), \
('p8', 'p3'): ('p8', 'p3', None, None), 'pTop': ('Top', 'p6', ('p6', 'p7'), ('p6', 'p8')), ('p7', 'p1'): \
('p7', 'p1', None, None)}
phi =  {'p2': 'h3', 'p3': 'h2', 'p1': 'h1', 'p4': 'h4'} 
  

Infinity = float('inf')

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

def DP(hostTree, parasiteTree, phi, D, T, L):
    """ Takes a hostTree, parasiteTree, tip mapping function phi, and
        duplication cost (D), transfer cost (T), and loss cost (L) and
        returns the DP table C. Cospeciation is assumed to cost 0. """

    A = {}
    C = {}
    O = {}
    Dictionary = {}
    BestSwitch = {}
    Minimums = {}
    Obest = {}
    BestSwitchLocations = {}
    BestSwitchLocations

    for ep in postorder(parasiteTree, "pTop"):
        for eh in postorder(hostTree, "hTop"):
            vp = parasiteTree[ep][1]
            vh = hostTree[eh][1]
            ep1 = parasiteTree[ep][2]
            ep2 = parasiteTree[ep][3]
            eh1 = hostTree[eh][2]
            eh2 = hostTree[eh][3]
            Dictionary[(vp, vh)] = []
            Obest[(vp, vh)] = []
            # is vp a tip?
            if ep1 == None: # then ep2 == None too and vp is a tip!
                vpIsATip = True
                pChild1 = None
                pChild2 = None
            else:
                vpIsATip = False
                pChild1 = parasiteTree[ep][2][1]
                pChild2 = parasiteTree[ep][3][1]

            # is vh a tip?
            if eh1 == None: # then eh2 == None too and vh is a tip!
                vhIsATip = True
                hChild1 = None
                hChild2 = None
            else:
                vhIsATip = False
                hChild1 = hostTree[eh][2][1]
                hChild2 = hostTree[eh][3][1]
                
            # Compute A(ep, eh)

            if vhIsATip:
                if vpIsATip and phi[vp] == vh:
                    A[(ep, eh)] = 0
                    Amin = ["C", (None, None), (None, None)] # Contemporary event to be added to Dictionary
                else: 
                    A[(ep, eh)] = Infinity
                    Amin = ["inf"]
            else: #vh is not a tip
                # Compute S and create event list to add to Dictionary
                if not vpIsATip:
                    COepeh = min(C[(ep1, eh1)] + C[(ep2, eh2)], \
                                 C[(ep1, eh2)] + C[(ep2, eh1)])
                    if COepeh == C[(ep2, eh1)]+ C[(ep1, eh2)]:

                        coMin = ["S", (pChild2, hChild1), (pChild1, hChild2)]
                    elif COepeh == C[(ep1, eh1)]+ C[(ep2, eh2)]:
                        coMin = ["S", (pChild1, hChild1), (pChild2, hChild2)]
                    else: coMin = ["S", (pChild2, hChild1), (pChild1, hChild2)]+["S", (pChild1, hChild1), (pChild2, hChild2)]

                else:
                    COepeh = Infinity
                    coMin = ["inf"]
                # Compute L and create event list to add to Dictionary
                LOSSepeh = L + min(C[(ep, eh1)], C[(ep, eh2)])

                if LOSSepeh == L + C[(ep, eh1)]: lossMin = ["L", (ep[1], hChild1), (None, None)]
                elif LOSSepeh == L + C[(ep, eh2)]: lossMin = ["L", (ep[1], hChild2), (None, None)]
                else: lossMin =["L", (ep[1], hChild1), (None, None)] + ["L", (ep[1], hChild2), (None, None)]

                # Determine which event occurs for A[(ep, eh)]
                A[(ep, eh)] = min(COepeh, LOSSepeh)
                if COepeh<LOSSepeh:
                   Amin = coMin
                elif LOSSepeh<COepeh: 
                    Amin = lossMin
                else: Amin = lossMin + coMin

            # Compute C(ep, eh)
            #   First, compute D
            if not vpIsATip:
                DUPepeh = D + C[(ep1, eh)] + C[(ep2, eh)]
            else:
                DUPepeh = Infinity
            #   Next, Compute T and create event list to add to Dictionary using BestSwitchLocations
            if not vpIsATip:
                switchList = []
                SWITCHepeh = T + min(C[(ep1, eh)] + BestSwitch[(ep2, eh)], \
                                     C[(ep2, eh)] + BestSwitch[(ep1, eh)]) 
                if (C[(ep1, eh)] + BestSwitch[(ep2, eh)])<(C[(ep2, eh)] + BestSwitch[(ep1, eh)]):
                    for item in BestSwitchLocations[(pChild2,vh)]:

                        switchList.append(["T", (pChild1, eh[1]), (pChild2, item[1])])
                elif (C[(ep2, eh)] + BestSwitch[(ep1, eh)])<(C[(ep1, eh)] + BestSwitch[(ep2, eh)]): 
                    for item in BestSwitchLocations[(pChild1,vh)]:
                        switchList.append(["T", (pChild2, eh[1]), (pChild1, item[1])])
                else: 
                    for item in BestSwitchLocations[(pChild2, vh)]:
                        switchList.append(["T", (pChild1, eh[1]), (pChild2, item[1])])
                    for item in BestSwitchLocations[(pChild1,vh)]:
                        switchList.append(["T", (pChild2, eh[1]), (pChild1, item[1])])

            else:
                SWITCHepeh = Infinity
                switchList = ["inf"]
            # Compute C[(ep, eh)] and add it's source to the Dictionary
            C[(ep, eh)] = min(A[(ep, eh)], DUPepeh, SWITCHepeh)
            Minimums[(vp, vh)] = C[(ep, eh)]
            if min(A[(ep, eh)], DUPepeh, SWITCHepeh) == DUPepeh:
                dupList = ["D", (pChild1, vh), (pChild2, vh)]
                Dictionary[(vp, vh)].append(dupList)
            if min(A[(ep, eh)], DUPepeh, SWITCHepeh) == SWITCHepeh:
                Dictionary[(vp, vh)].extend(switchList)
            if min(A[(ep, eh)], DUPepeh, SWITCHepeh) == A[(ep, eh)]: Dictionary[(vp, vh)].append(Amin)
            if Minimums[(vp, vh)] == Infinity:
                del Minimums[(vp, vh)]
                del Dictionary[(vp, vh)]
            # Compute O(ep, eh)
            # Compute Obest[(vp, vh)], the source of O(ep, eh)
            if vhIsATip: 
                O[(ep, eh)] = C[(ep, eh)]  
                Obest[(vp, vh)] = [(vp, vh)]              
            else: 
                omin = [C[(ep, eh)], O[(ep, eh1)], O[(ep, eh2)]].index(min(C[(ep, eh)], O[(ep, eh1)], O[(ep, eh2)]))
                if omin == 0:
                    Obest[(vp,vh)].append((vp, vh))
                if omin == 1:
                    Obest[(vp,vh)].extend(Obest[(vp, hChild1)])
                if omin == 2:
                    Obest[(vp,vh)].extend(Obest[(vp, hChild2)])
                O[(ep, eh)] = min(C[(ep, eh)], O[(ep, eh1)], O[(ep, eh2)])

        # Compute BestSwitch values
        BestSwitch[(ep, "hTop")] = Infinity
        BestSwitchLocations[(ep[1], hostTree["hTop"][1])] = [(None,None)]
        for eh in preorder(hostTree, "hTop"):
            vp = parasiteTree[ep][1]
            vh = hostTree[eh][1]
            ep1 = parasiteTree[ep][2]
            ep2 = parasiteTree[ep][3]
            eh1 = hostTree[eh][2]
            eh2 = hostTree[eh][3]
            #is vp a tip?
            if ep1 == None:
                vpIsATip = True
                pChild1 = None
                pChild2 = None
            else:
                vpIsATip = False
                pChild1 = parasiteTree[ep][2][1]
                pChild2 = parasiteTree[ep][3][1]

            # is vh a tip?
            if eh1 == None: # then eh2 == None too and vh is a tip!
                vhIsATip = True
                hChild1 = None
                hChild2 = None
            else:
                vhIsATip = False
                hChild1 = hostTree[eh][2][1]
                hChild2 = hostTree[eh][3][1]
            # find best place for a switch to occur, and the location to which the edge switches    
            if eh1 != None and eh2 != None:
                BestSwitchLocations[(vp, hChild1)] = []
                BestSwitchLocations[(vp, hChild2)] = []
                BestSwitch[(ep, eh1)] = min(BestSwitch[(ep, eh)], O[(ep, eh2)])
                BestSwitch[(ep, eh2)] = min(BestSwitch[(ep, eh)], O[(ep, eh1)])
                if BestSwitch[(ep, eh1)] == BestSwitch[(ep, eh)]:
                    BestSwitchLocations[(vp, hChild1)].extend(BestSwitchLocations[(vp, vh)])
                if BestSwitch[(ep, eh1)] == O[(ep, eh2)]:
                    BestSwitchLocations[(vp, hChild1)].extend(Obest[(vp, hChild2)])
                if BestSwitch[(ep, eh2)] == BestSwitch[(ep, eh)]:
                    BestSwitchLocations[(vp, hChild2)].extend(BestSwitchLocations[(vp, vh)])
                if BestSwitch[(ep, eh2)] == O[(ep, eh1)]:
                    BestSwitchLocations[(vp, hChild2)].extend(Obest[(vp, hChild1)])
    for key in BestSwitchLocations.keys():
        if BestSwitchLocations[key][0] == (None, None):
            BestSwitchLocations[key] = BestSwitchLocations[key][1:]
    #add the costs of each event to the corresponding Dictionary entry
    for key in Dictionary.keys():
        Dictionary[key].append(Minimums[key])
    treeMin = findBest(parasiteTree, Minimums)
    DTL = {}
    DTL = findPath(treeMin, Dictionary, DTL)
    DrawDTLc.drawNodes(treeMin, DTL, 200, {})
    return DTL



def findBest(Parasite, MinimumDict):
    """Takes Parasite Tree and a dictionary of Minimum resolution costs. 
    returns Dictionary of the minimum cost reconciliation tree roots"""
    treeMin = {}
    for key in MinimumDict.keys():
        if key[0] == Parasite['pTop'][1]:
            treeMin[key] = MinimumDict[key]
    minimum = treeMin[treeMin.keys()[0]]
    for key in treeMin.keys():
        if treeMin[key] < minimum:
            minimum = treeMin[key]
    for key in treeMin.keys():
        if treeMin[key] > minimum:
            del treeMin[key]     
    return treeMin.keys()

def findPath(TupleList, eventDict, uniqueDict):
    """Takes the list of minimum reconciliation cost roots, the Dictionary of Events and Children
     for each Node, and the Dictionary of unique vertex mappings. Returns the completed DTL graph as a 
     Dictionary"""
    for Tuple in TupleList:
        if not Tuple in uniqueDict:
            uniqueDict[(Tuple)] = eventDict[(Tuple)]
        for thing1 in eventDict[Tuple]:
            if type(thing1)==list:
                for thing2 in thing1:
                    if type(thing2) == tuple and thing2 != (None, None):
                        findPath([thing2], eventDict, uniqueDict)
    return uniqueDict

def reconcile(fileName, D, T, L):
    """Takes FileName, dupliction cost, transfer cost, and loss cost. Returns DTL reconciliation
     graph of the provided newick file"""
    host, paras, phi = newickFormatReader.getInput(fileName)
    return DP(host, paras, phi, D, T, L)