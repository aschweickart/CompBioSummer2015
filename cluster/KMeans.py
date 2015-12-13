# Alex Ozdemir <aozdemir@hmc.edu>
# December 2015
#
# This file holds the functions for clustering

from StratifiedCounts import sparse_counts_n, counts
from ReconGraph import ReconGraph, MAP_NODE
import random
import operator
from collections import defaultdict

flatten = lambda l: reduce(operator.add, l)

maximize_value_lists = set([])
maximize_parent_lists = set([])
maximize_call_counts = 0

def maximize(graph, value_table, default=0):
    ''' Given a reconciliation graph and a value mapping, returns
    the event set of the reconciliation which maximizes the sum of
    the value function over its nodes '''

    # The value of the best subreconciliation rooted at each node
    best_value = {}
    # The index of the child used to get that subreconciliation
    #  (-1 for all children)
    used_child_index = {}
    ALL_CHILDREN = -1

    def value(node):
        ''' Gets the value of a node '''
        return value_table[node] if node in value_table else default

    # Populate DP tables for the entire graph
    for n in graph.postorder():
        if n.isLeaf():
            used_child_index[n] = ALL_CHILDREN # vacuous
            best_value[n] = value(n)
        elif n.isMap():
            child_values = [best_value[c] for c in n.children]
            best_value[n] = max(child_values)
            used_child_index[n] = child_values.index(best_value[n])
        else: # n is an event node
            best_value[n] = value(n) + sum(best_value[c] for c in n.children)
            used_child_index[n] = ALL_CHILDREN

    # Recover an optimal set of event nodes
    root_values = [best_value[n] for n in graph.roots]
    best_root = graph.roots[root_values.index(max(root_values))]
    q = [best_root]
    event_set = set([])
    while len(q) > 0:
        n = q.pop()
        if used_child_index[n] == ALL_CHILDREN:
            for c in n.children:
                q.append(c)
        else:
            q.append(n.children[used_child_index[n]])
        if not n.isMap():
            event_set.add(n)

    global maximize_value_lists, maximize_call_counts, maximize_parent_lists
    maximize_value_lists.add(tuple(best_value[n] for n in graph.postorder()))
    maximize_parent_lists.add(tuple(used_child_index[n] for n in graph.postorder()))
    maximize_call_counts += 1
    return best_value, used_child_index, event_set

def node_value_maps_symmetric(graph, reps):
    ''' Given a
        graph - reconcilliation graph
        reps  - a list of reconciliations in event-set form
    returns a list of value maps (in the same order as the reps)

    where a value map is a mapping from a node in the reconciliation graph
      to a number (See the 'Computing Weighted Means' section of the paper)
    '''
    counts = sparse_counts_n(graph, reps)
    Ks = [0 for rep in reps]
    for n in graph.roots:
        for pt in counts[n].map:
            minDist = min(pt)
            number = counts[n].map[pt]
            closest_rep_i_s = [i for (i, d) in enumerate(pt) if d == minDist]
            for i in closest_rep_i_s:
                Ks[i] += float(number) / len(closest_rep_i_s)

    value_maps = [defaultdict(float) for rep in reps]
    for n in graph.postorder():
        for pt in counts[n].map:
            minDist = min(pt)
            number = counts[n].map[pt]
            closest_rep_i_s = [i for (i, d) in enumerate(pt) if d == minDist]
            for i in closest_rep_i_s:
                value_maps[i][n] += float(number) / len(closest_rep_i_s)

    for (value_map,K) in zip(value_maps, Ks):
        for n in value_map:
            value_map[n] = 2 * value_map[n] - K

    if not abs(sum(Ks) - sum(counts[graph.roots[0]].map.values())) < 1:
        print 'Reconciliation count by constant: %d' % abs(sum(ks))
        print 'Reconciliation count by roots   : %d' % sum(counts[graph.roots[0]].map.values())
        print 'Should be equal'
        assert False
    return value_maps

def node_value_maps_asymmetric(graph, reps):
    ''' Given a
        graph - reconcilliation graph
        reps  - a list of reconciliations in event-set form
    returns a list of value maps (in the same order as the reps)

    where a value map is a mapping from a node in the reconciliation graph
      to a number (See the 'Computing Weighted Means' section of the paper)
    '''
    counts = sparse_counts_n(graph, reps)
    value_maps = [defaultdict(float) for rep in reps]
    ct = [0, 0]
    amt= [0, 0]
    for n in graph.postorder():
        for pt in counts[n].map:
            minDist = min(pt)
            number = counts[n].map[pt]
            closest_rep_i_s = [i for (i, d) in enumerate(pt) if d == minDist]
            if len(closest_rep_i_s) > 1:
                ct[1] += 1
                amt[1] += float(number)
            else:
                ct[0] += 1
                amt[0] += float(number)
            for i in closest_rep_i_s:
                value_maps[i][n] += float(number) / len(closest_rep_i_s)
    print '%d diff and %d equisdistant dists' % tuple(ct)
    print 'Distinct closest reps got %d weight, and ties got %d' % tuple(amt)
    p = [[value_map[n] for value_map in value_maps] for n in value_maps[0]]
    print 'Number of reconciliations: %d' % sum(counts[graph.roots[0]].map.values())
    return value_maps

def k_means_step(graph, reps):
    ''' Given a
        graph - reconciliation graph
        reps  - a list of reconciliations in event-set form
    returns a new list of representatives.'''
    value_maps = node_value_maps_symmetric(graph, reps)
    res = [maximize(graph, value_map) for value_map in value_maps]
    net = [0.0 for rep in reps]
    for i in xrange(len(net)):
        for n in graph.postorder():
            net[i] += value_maps[i][n]
    print 'Net values by rep they get assigned to: %s' % net
    print 'Rep 1 size: %d  Rep 2 size: %d  Sym Diff: %d' % (len(reps[0]), len(reps[1]), len(reps[0] ^ reps[1]))
    print 'Rep 1 size: %d  Rep 2 size: %d  Sym Diff: %d' % (len(res[0][2]), len(res[1][2]), len(res[0][2] ^ res[1][2]))
    return [r[2] for r in res]

def step_many(step_fn, graph, reps, steps):
    for i in xrange(steps):
        new_reps = step_fn(graph, reps)
        stable = reps == new_reps
        for rep in new_reps:
            if not verify_reconciliation(graph, rep):
                print 'Invalid reconciliation!'
        print 'Stable' if stable else 'Unstable'
        print 'Differences %s' % [len(rep - new_rep) for rep, new_rep in zip(reps, new_reps)]
        reps = new_reps
        if stable:
            print 'Early exit after %d iterations' % (i + 1)
            break
    return reps

def k_means(graph, steps, k, seed=0):
    print '==========================='
    print 'K means starting with k = %d, seed = %d' % (k, seed)
    print 'Size of graph: %d' % len(graph)
    random.seed(seed)
    reps = [get_template(graph) for i in xrange(k)]
    end_reps = step_many(k_means_step, graph, reps, steps)
    return end_reps

def inv_sq(graph, steps, k, seed=0, reps=None):
    print '==========================='
    print 'Inverse Square starting with k = %d, seed = %d' % (k, seed)
    random.seed(seed)
    if reps is None:
        reps = [get_template(graph) for i in xrange(k)]
    end_reps = step_many(inv_sq_step, graph, reps, steps)
    return end_reps

def inv_sq_step(graph, reps):
    return [inv_sq_step_one(graph, rep) for rep in reps]

def inv_sq_step_one(graph, rep):
    ''' Given a
        graph - reconciliation graph
        rep  - a reconciliation in event-set form
    returns a new reconciliation, which is the mean of all the reconciliations
    in the graph, weighted by the inverse square of their distance from the
    original reconciliation. '''
    value_map = node_value_map_inv_sq(graph, rep)
    value_table, trace_table, optimum = maximize(graph, value_map)
    return optimum

def node_value_map_inv_sq(graph, rep):
    ''' Given a
        graph - reconciliation graph
        rep  - a reconciliation in event-set form
    returns a map from event nodes in the graph to ... TODO ... '''
    def weight(distance):
        # return 1 # Constant weight
        # return 0 if distance == 0 else 1 # Constant, but weights the perfect match as 0
        return 1 if distance == 0 else float(distance) ** -2.0 # Inverse Square
    counts = sparse_counts_n(graph, [rep])
    K = 0.0
    for n in graph.roots:
        for pt in counts[n].map:
            assert len(pt) == 1
            distance = pt[0]
            number_at_distance = counts[n].map[pt]
            K += weight(distance) * number_at_distance
    value_map = defaultdict(float)

    for n in graph.postorder():
        for pt in counts[n].map:
            assert len(pt) == 1
            distance = pt[0]
            number_at_distance = counts[n].map[pt]
            value_map[n] += number_at_distance * weight(distance)

    for n in value_map:
        value_map[n] = 2 * value_map[n] - K

    return value_map

f = open('t.g')
G = eval(f.read())
f.close()

GG = ReconGraph(G)

r = GG.roots[0]

def unique(L):
    out = []
    for l in L:
        if l not in out:
            out.append(l)
    return out

def get_root_that_has_child_in(graph, event_set):
    s = set([])
    for r in graph.roots:
        for child in r.children:
            if child in event_set:
                s.add(r)
    return list(s)[0]

def verify_reconciliation(graph, event_set):
    ''' Given a
        graph     - reconociliation graph
        event_set - a set of event nodes from that graph
    returns whether that event_set corresponds to an actual reconciliation
    in the graph. '''
    # We traverse the graph to build a reconciliation, guided by event_set
    # We count how many event nodes we accumulate in the process for comparison
    count = 0
    q = [get_root_that_has_child_in(graph, event_set)]
    while len(q) > 0:
        n = q.pop()
        if n.isMap():
            children_in_set = []
            for child in n.children:
                if child in event_set:
                    children_in_set.append(child)
            if len(children_in_set) != 1:
                return False
            q.extend(children_in_set)
        else:
            count += 1
            q.extend(n.children)
    if count != len(event_set):
        return False
    return True

def reconciliation_sizes(graph):
    sub_sizes = {}
    for n in graph.postorder():
        if n.isLeaf():
            sub_sizes[n] = SparseNDistanceFunction.kronicker((1,))
        elif n.isMap():
            child_sub_sizes = [sub_sizes[c] for c in n.children]
            sub_sizes[n] = reduce(lambda x, y: x.sum(y), child_sub_sizes)
        else:
            child_sub_sizes = [sub_sizes[c] for c in n.children]
            sub_sizes[n] = reduce(lambda x, y: x.convolve(y), child_sub_sizes).shift((1,))
    return reduce(lambda x, y: x.sum(y), [sub_sizes[r] for r in graph.roots])

def get_template(graph):
    ''' Given a reconciliation graph, returns a random reconciliation in
    event-set form '''
    events = set([])
    stack = [random.choice(graph.roots)]
    while len(stack) > 0:
        n = stack.pop()
        if not n.isMap():
            events.add(n)
            for c in n.children:
                stack.append(c)
        else:
            stack.append(random.choice(n.children))
    return events


rep1 = []
# rep1 = k_means(GG, 10, 1)
# rep2s = [k_means(GG, 10, 2, seed) for seed in xrange(1)]
rep2s = [inv_sq(GG, 10, 5, seed) for seed in xrange(5)]
rep3s = [[]]
# rep3s = [k_means(GG, 10, 3, seed) for seed in xrange(1)]
reps = rep1 + flatten(rep2s) + flatten(rep3s)

print '%d distinct representatives out of %d' % (len(unique(reps)), len(reps))
print 'Maximize was called %d times' % maximize_call_counts
print 'Maximize built %d tables' % len(maximize_value_lists)
print 'Maximize built %d parent tables' % len(maximize_parent_lists)
