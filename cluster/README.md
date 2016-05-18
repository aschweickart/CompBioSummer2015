# Reconcilliation Clustering

This directory holds code which computes "stratified reconciliation counts" as
described in the write-up, and uses these counts to
   * Cluster reconciliations using the KMeans and InvSq heuristics (the latter
       of our own design)
   * Evaluate the quality of clusterings - agnostic of how they were produced.

For more details on this, read the write up (Prof. Ran should have it)

## Running the Tests

We've hooked up the KMeans clustering tools to be run on newick files. One can
use this like so:

```
python2 FromNewick.py [?.newick,??.newick,...] [number of clusters to produce]
```

For example,

```
python2 FromNewick.py ../TreeLifeData/COG0001.newick 2
```

Note that the first stage in the computation is generating the reconciliation
graph. Because this takes a while and wasn't what we were working on, the
`FromNewick` tool caches these reconciliation graphs in `cache`

## Structure of the Project

### Underlying Data-Structures

`DistanceFunction.py` and `Convolve.py` both hold code which provides functions
from Z^n -> Z which
   * Are non-zero for only a finite set of inputs
   * Support poinwise addition, construction of kronicker functions, and
       convolution.

`ReconGraph.py` holds the Reconciliation Graph data-structure, along with a
constructor which takes in the output from `DP.py:DP` (I don't recall what the
format of this output is right now).

### Stratified Counts

`StratifiedCounts.py` contains function which compute stratified counts with
respect to one of more template reconciliations. While the definition of
stratified counts (see the write-up) seems weird at first, it is key in
implementing clutering heuristics and evaluating cluster quality.

### Clustering Algorithms

`KMeans.py` contains the value maximization code (chooses the reconciliation in
the graph which maximizes the sum of some value function on nodes of the graph
across the nodes in the reconciliation), and uses this maximization procedure
to implement the KMeans clustering algorithm, along with a novel (but nt very
good) custering algorithm, InvSq, as described in the file. This file also
includes a function which evaluates cluster quality.

`FromNewick.py` hooks up all the parts so you can run KMeans on newick files,
in bulk (for performance testing). There is a flag in the file for parallelism.
