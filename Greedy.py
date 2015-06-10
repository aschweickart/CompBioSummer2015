

#Team Srinidhi and Juliet

#Our goal is to find the k best reconciliatioins

#We are gien a DTL reconciliation graph in the form of dictionaries

#Dict1: the values of the DTl graphs will be modified to hold the BSFH scores

#Keeping track of bookkeeping

#key: mapping node
#value: List of (0) max (1) where the max came from

BSFH  = {}

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

	 

def bookkeeping(DTL):
	"""This function inputs the DTL graph and then records what the max is at each mapping node and 
	where the max came from so outputs BSFH"""


def greedy(DTL, k):
	"""This function inputs the BSFH, DTL and k, and calls bokkeeping to find the best k reconciliations,
	which is represented in a dictionary. Greedy is also going to reset the BSFH scores to 0 and then call
	bookkeeping with the new DTL. We do this k times""" 

	for i in range(k):
		"""we find the max"""
		BSFH = bookkeeping(DTL)

		bestKey = ''
		bestScore = 0
		for key in BSFH:
			if BSFH[key][0] > bestScore:
				bestKey = key
				bestScore = BSFH[key][0]
			






























