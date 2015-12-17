import sys

# Include the upper level directory in the import search path
sys.path.append('../')

import DP
import Greedy
import KMeans
import newickFormatReader
import copy
import ReconGraph

fileName = sys.argv[1]

D = 2.
T = 3.
L = 1.

host, paras, phi = newickFormatReader.getInput(fileName)
# Default scoring function (if freqtype == Frequency scoring)
DictGraph, numRecon = DP.DP(host, paras, phi, D, T, L)

print 'DP complete, doing greedy'

scoresList, dictReps = Greedy.Greedy(DictGraph, paras)

print 'Found cluster representatives usign point-collecting'
print 'Converting to memory representation'

graph = ReconGraph.ReconGraph(DictGraph)
setReps = [ReconGraph.dictRecToSetRec(graph, dictRep) for dictRep in dictReps]

KMeans.k_means(graph, 10, 3, 0, setReps[:4])
