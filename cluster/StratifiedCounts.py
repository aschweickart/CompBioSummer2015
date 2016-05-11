# Alex Ozdemir <aozdemir@hmc.edu>
# December 2015
#
# This file holds the functions for computing stratified counts
#
# For a careful definition of stratified counts, supercounts, and subcounts,
# see the write-up

from ReconGraph import ReconGraph
from DistanceFunction import DistanceFunction, NDistanceFunction, SparseNDistanceFunction

######################################################
### Computing counts with respect to a single template
######################################################

def _subcounts(graph, template_event_set):
    ''' Given
        graph              - a reconciliation graph
        template_event_set - a reconciliation in event-set form
    Computes the stratified symmetric subcounts of every node in the graph
    with respect to the template
    '''
    table = {}
    for n in graph.postorder():
        if n.isLeaf():
            table[n] = DistanceFunction.kronicker(-1)
        elif n.isMap():
            table[n] = reduce(lambda x, y: x.sum(y), \
                                       [table[c] for c in n.children])
        else:
            shift_amount = 1 if n not in template_event_set else -1
            table[n] = reduce(lambda x, y: x.convolve(y), \
                                       [table[c] for c in n.children])
            table[n] = table[n].shift(shift_amount)
    return table

def _supercounts(graph, template_event_set, subcount_table):
    ''' Given
        graph              - a reconciliation graph
        template_event_set - a reconciliation in event-set form
        subcount_table     - a mapping from nodes in the graph to subcounts
    Computes the stratified symmetric supercounts of every node in the graph
    with respect to the template. Relies on pre-computed subcounts
    '''
    table = {}
    for n in graph.preorder():
        if n.isRoot():
            table[n] = DistanceFunction.kronicker(0)
        elif n.isMap():
            def process_parent(event_parent):
                shift_amount = 1 if event_parent not in template_event_set else -1
                parent_super = table[event_parent]
                otherChild = event_parent.otherChild(n)
                convolved = parent_super.convolve(subcount_table[otherChild]) \
                                if otherChild \
                                else parent_super
                return convolved.shift(shift_amount)
            sup_count = reduce(lambda x, y: x.sum(y), map(process_parent, n.parents))
            table[n] = sup_count
        else:
            shift_amount = 1 if n not in template_event_set else -1
            # Event nodes inherit their single parent's super-count.
            # Shallow copy is same because we don't mutatate Fn's
            table[n] = table[n.parents[0]]
    return table

def _counts(graph, template_event_set, subcount_table, supercount_table):
    ''' Given
        graph              - a reconciliation graph
        template_event_set - a reconciliation in event-set form
        subcount_table     - a mapping from nodes in the graph to subcounts
        supercount_table   - a mapping from nodes in the graph to subcounts
    Computes the stratified symmetric counts of every node in the graph
    with respect to the template. Relies on precomputed sub and super counts
    '''
    count_table = {}
    offset = len(template_event_set)
    for n in graph.postorder():
        count_table[n] = \
                subcount_table[n].convolve(supercount_table[n]).shift(offset)
    return count_table

def counts(graph, template_event_set):
    ''' Given
        graph              - a reconciliation graph
        template_event_set - a reconciliation in event-set form
    Computes the stratified symmetric counts of every node in the graph
    with respect to the template.
    '''
    subcount_table = _subcounts(graph, template_event_set)
    supercount_table = _supercounts(graph, template_event_set, subcount_table)
    return _counts(graph, template_event_set, subcount_table, supercount_table)

#########################################################
### Computing counts with respect to a multiple templates
#########################################################

def _subcounts_n(graph, template_event_set_s, fn_class):
    table = {}
    for n in graph.postorder():
        if n.isLeaf():
            table[n] = fn_class.kronicker(
                    tuple(-1 for i in xrange(len(template_event_set_s))))
        elif n.isMap():
            table[n] = reduce(lambda x, y: x.sum(y), \
                                       [table[c] for c in n.children])
        else:
            shift_amount = [1 if n not in template_event_set else -1 for \
                    template_event_set in template_event_set_s]
            table[n] = reduce(lambda x, y: x.convolve(y), \
                                       [table[c] for c in n.children])
            table[n] = table[n].shift(shift_amount)
    return table

def _supercounts_n(graph, template_event_set_s, subcount_table, fn_class):
    table = {}
    for n in graph.preorder():
        if n.isRoot():
            table[n] = fn_class.kronicker(
                    tuple(0 for i in xrange(len(template_event_set_s))))
        elif n.isMap():
            def process_parent(event_parent):
                shift_amount = [1 if event_parent not in template_event_set else -1 for \
                        template_event_set in template_event_set_s]
                parent_super = table[event_parent]
                otherChild = event_parent.otherChild(n)
                convolved = parent_super.convolve(subcount_table[otherChild]) \
                                if otherChild \
                                else parent_super
                return convolved.shift(shift_amount)
            sup_count = reduce(lambda x, y: x.sum(y), map(process_parent, n.parents))
            table[n] = sup_count
        else:
            shift_amount = [1 if n not in template_event_set else -1 for \
                    template_event_set in template_event_set_s]
            # Event nodes inherit their single parent's super-count.
            # Shallow copy is same because we don't mutatate Fn's
            table[n] = table[n.parents[0]]
    return table

def _counts_n(graph, template_event_set_s, subcount_table, supercount_table):
    count_table = {}
    offsets = [len(template_event_set) for template_event_set in template_event_set_s]
    for n in graph.postorder():
        count_table[n] = \
                subcount_table[n].convolve(supercount_table[n]).shift(offsets)
    return count_table

def counts_n(graph, template_event_set_s, fn_class):
    subcount_table = _subcounts_n(graph, template_event_set_s, fn_class)
    supercount_table = _supercounts_n(graph, template_event_set_s, subcount_table, fn_class)
    return _counts_n(graph, template_event_set_s, subcount_table, supercount_table)

def sparse_counts_n(graph, template_event_set_s):
    ''' Computing the counts with respect to many templates using the sparse
    function class '''
    return counts_n(graph, template_event_set_s, SparseNDistanceFunction)

def dense_counts_n(graph, template_event_set_s):
    ''' Computing the counts with respect to many templates using the dense
    function class '''
    return counts_n(graph, template_event_set_s, NDistanceFunction)

