# Alex Ozdemir, Michael Sheely
# <aozdemir@hmc.edu>, <msheely@hmc.edu>
# Nov 2015
#
# This file holds classes which represent functions from Z^n -> Z
# In particular the classes can represent functions which are non-zero on only
# a finite set of inputs.
#
# We build functions backed by both python dicitonaries and NumPy arrays
#
# We've empirically determined that for resonable values of n (2-5), the python
# dictionaries win by a long shot

import numpy as np
import Convolve
import copy
from collections import defaultdict

def _vec_sum(v1, v2):
    return tuple(a + b for a, b in zip(v1, v2))

class DistanceFunction(object):
    '''
    Class for representing a [dense] function from Z -> Z
    '''
    def __init__(self):
        self.vector = np.array([])
        self.maxDistance = -1
        self.offset = 0
        #offset is the input that gets mapped to self.vector[0]

    def __repr__(self):
        return ','.join(['%d:%s' % (i + self.offset, item) for (i, item) in enumerate(self.vector)])

    def resetMaxDistance(self):
        self.maxDistance = len(self.vector) + self.offset - 1

    def __call__(self, index):
        if index >= self.offset and index <= self.maxDistance:
            if index - self.offset < len(self.vector):
                return self.vector[index - self.offset]
            else:
                print index, self.offset, self.maxDistance, self.vector
                assert False
        return 0

    def shift(self, i):
        res = copy.deepcopy(self)
        res.offset += i
        res.resetMaxDistance()
        return res

    def convolve(self, other):
        result = DistanceFunction()
        result.offset = self.offset + other.offset
        result.vector = np.convolve(self.vector, other.vector)
        result.resetMaxDistance()
        return result

    def dump(self, s):
        print s, self, self.offset, self.maxDistance, self.vector

    def sum(self, other):
        result = DistanceFunction()
        result.offset = min(self.offset, other.offset)
        maxDist = max(self.maxDistance,other.maxDistance)
        result.vector = np.zeros((maxDist + 1 - result.offset,), np.int64)
        result_self_slice = \
                (slice(0                + self.offset - result.offset,
                       len(self.vector) + self.offset - result.offset),)
        result_other_slice = \
                (slice(0                 + other.offset - result.offset,
                       len(other.vector) + other.offset - result.offset),)
        result.vector[result_self_slice] += self.vector
        result.vector[result_other_slice] += other.vector
        result.resetMaxDistance()
        return result

    @staticmethod
    def kronicker(i):
        res = DistanceFunction()
        res.offset = i
        res.vector = np.array([1])
        res.resetMaxDistance()
        return res

class NDistanceFunction(object):
    ''' class for [dense] functions from Z^n -> N
    backed by NumPy arrays'''
    def __init__(self, dim):
        dimTuple = tuple([0 for i in range(dim)])
        self.vector = np.array([], ndmin=dim)
        self.dim = dim
        #maxDistance and offests are defined for each template
        self.maxDistances = [-1 for i in range(dim)]
        self.offsets = [0 for i in range(dim)]

    def __repr__(self):
        return '%d-dimensional tensor\nvec: %s\noff: %s' \
                % (self.dim, self.vector, self.offsets)

    def resetMaxDistance(self):
        self.maxDistances = [l + o - 1 for (l,o) \
                    in zip(self.vector.shape, self.offsets)]

    def __call__(self, dists):
        for i in range(len(dists)):
            if dists[i] < self.offsets[i] or dists[i] > self.maxDistances[i]:
                return 0
        return self.vector[tuple( d - o for d, o in zip(dists,self.offsets))]

    def convolve(self, other):
        result = NDistanceFunction(self.dim)
        result.offsets = [so + oo for so, oo in zip(self.offsets, other.offsets)]
        result.vector = Convolve.convolve(self.vector, other.vector)
        result.resetMaxDistance()
        return result

    def sum(self, other):
        result = NDistanceFunction(self.dim)
        result.offsets = [min(so, oo) for (so,oo) \
                        in zip(self.offsets, other.offsets)]
        rShape = [max(self.maxDistances[i], other.maxDistances[i]) - \
                  min(self.offsets[i], other.offsets[i]) + 1 \
                  for i in xrange(self.dim)]
        result.maxDistances = [max(self.maxDistances[i] - self.offsets[i], \
                                 other.maxDistances[i] - other.offsets[i]) \
                                for i in xrange(self.dim)]
        result.vector = np.zeros(rShape, dtype=np.int64)

        result_self_slice = \
            tuple(slice(0                    + self.offsets[i] - result.offsets[i],
                        self.vector.shape[i] + self.offsets[i] - result.offsets[i])
                        for i in xrange(self.dim))
        result_other_slice = \
            tuple(slice(0                     + other.offsets[i] - result.offsets[i],
                        other.vector.shape[i] + other.offsets[i] - result.offsets[i])
                        for i in xrange(other.dim))
        result.vector[result_self_slice] += self.vector
        result.vector[result_other_slice] += other.vector

        result.resetMaxDistance()
        return result

    def shift(self, i_s):
        res = copy.deepcopy(self)
        res.offsets = [a + b for a, b in zip(res.offsets, i_s)]
        res.resetMaxDistance()
        return res

    def dump(self, s):
        print s, self, self.offset, self.maxDistance, self.vector

    @staticmethod
    def kronicker(dists):
        res = NDistanceFunction(len(dists))
        res.offsets = dists
        res.vector = np.array([1], ndmin = len(dists))
        res.resetMaxDistance()
        return res

class SparseNDistanceFunction(object):
    ''' Represents functions from Z^n -> Z
    backed by a python dictionary - best option for sparse functions
    (functions that are 0 for a large amount of the interesting domain) '''
    def __init__(self, dim):
        self.dim = dim
        self.map = defaultdict(int)

    @staticmethod
    def kronicker(pt):
        result = SparseNDistanceFunction(len(pt))
        result.map[pt] = 1
        return result

    def sum(self, other):
        result = SparseNDistanceFunction(self.dim)
        for pt in self.map:
            result.map[pt] += self.map[pt]
        for pt in other.map:
            result.map[pt] += other.map[pt]
        return result

    def convolve(self, other):
        result = SparseNDistanceFunction(self.dim)
        for pt1 in self.map:
            for pt2 in other.map:
                result.map[_vec_sum(pt1, pt2)] += self.map[pt1] * other.map[pt2]
        return result

    def shift(self, i_s):
        result = SparseNDistanceFunction(self.dim)
        for pt in self.map:
            result.map[_vec_sum(pt, i_s)] = self.map[pt]
        return result

    def __repr__(self):
        return '{%s}' % ', '.join('%s: %d' % (p, self.map[p]) for p in self.map)

    def __call__(self, pt):
        return self.map[pt]

