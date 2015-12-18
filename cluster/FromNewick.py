import sys

# Include the upper level directory in the import search path
sys.path.append('../')

import os
from multiprocessing import Pool
import DP
import Greedy
import KMeans
import newickFormatReader
import copy
import ReconGraph
import random

def run_test(fileName, max_k):
    cache_dir = './cache'
    D = 2.
    T = 3.
    L = 1.

    host, paras, phi = newickFormatReader.getInput(fileName)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        f = open('%s/README' % cache_dir, 'w')
        f.write('This directory holds a cache of reconciliation graph for the TreeLife data set')
        f.close()

    cache_location = '%s/%s.graph' % (cache_dir, os.path.split(fileName)[1])
    if not os.path.isfile(cache_location):
        print >> sys.stderr, 'A reconciliation graph has not been built yet for this newick file'
        print >> sys.stderr, 'Doing so now {%s}...' % cache_location

        DictGraph, numRecon = DP.DP(host, paras, phi, D, T, L)

        f = open(cache_location, 'w+')
        f.write(repr(DictGraph))
        f.close()

    print >> sys.stderr, 'Loading reonciliation graph from cache'
    f = open(cache_location)
    DictGraph = eval(f.read())
    f.close()

    scoresList, dictReps = Greedy.Greedy(DictGraph, paras)

    print >> sys.stderr, 'Found cluster representatives usign point-collecting'

    graph = ReconGraph.ReconGraph(DictGraph)
    setReps = [ReconGraph.dictRecToSetRec(graph, dictRep) for dictRep in dictReps]
    random.seed(0)
    extra_reps = [KMeans.get_template(graph) for i in xrange(max_k)]

    representatives = setReps + extra_reps


    for i in xrange(1, max_k + 1):
        print 'k = %d' % i
        KMeans.k_means(graph, 10, i, 0, representatives[:i])

def doFile(fileName):
    try:
        run_test(fileName, max_k)
    except:
        pass

fileNames = sys.argv[1]
max_k = int(sys.argv[2])
num_processors = 1
if num_processors > 1:
    p = Pool(num_processors)
    p.map(doFile, fileNames.split(','))
else:
    [run_test(fileName, max_k) for fileName in fileNames.split(',')]
