import Queue
import random
import copy
import operator
import itertools as it
from DistanceFunction import DistanceFunction, NDistanceFunction, SparseNDistanceFunction
from collections import defaultdict

flatten = lambda l: reduce(operator.add, l)

MAP_NODE      = 'map-node'
COSPECIATION  = 'S'
LEAF_PAIR     = 'C'
TRANSFER      = 'T'
DUPLICATION   = 'D'
LOSS          = 'L'

NO_CHILD = (None, None)

class Node(object):
    def __init__(self, ty, mapping = None):
        self.children = []
        self.parents = []
        self.ty = ty
        self.mapping = mapping
    def __repr__(self):
        return '<Node type: %s, mapping: %s, #child: %d, #parent: %d>' % \
                (self.ty, self.mapping, len(self.children), len(self.parents))
    def isLeaf(self):
        return len(self.children) == 0
    def isRoot(self):
        return len(self.parents) == 0
    def isMap(self):
        return self.ty == MAP_NODE
    def otherChild(self, child):
        ''' Given a child, returns a child of this node which is not that child.
        Will return None if there is no such other child.
        Uses object id() equality'''
        for c in self.children:
            if not c is child:
                return c
        return None
    def __eq__(self, other):
        if self.mapping:
            return self.mapping == other.mapping
        else:
            if self.ty != other.ty:
                return False
            if set(self.parents) != set(other.parents):
                return False
            return set(self.children) == set(other.children)

class ReconGraph(object):
    def __init__(self, map_node_map):
        # Map mappings (parasite, host) to nodes
        self.map_nodes = {}
        def get_or_make_map_node(mapping):
            if mapping not in self.map_nodes:
                self.map_nodes[mapping] = Node(MAP_NODE, mapping)
            return self.map_nodes[mapping]
        for mapping in map_node_map:
            event_children = map_node_map[mapping][:-1]
            for ty, child1mapping, child2mapping, _ in event_children:
                parent_map_node = get_or_make_map_node(mapping)
                event_node = Node(ty)
                if child1mapping != NO_CHILD:
                    child1 = get_or_make_map_node(child1mapping)
                    event_node.children.append(child1)
                    child1.parents.append(event_node)
                if child2mapping != NO_CHILD:
                    child2 = get_or_make_map_node(child2mapping)
                    event_node.children.append(child2)
                    child2.parents.append(event_node)
                parent_map_node.children.append(event_node)
                event_node.parents.append(parent_map_node)
        self.map_node_map = map_node_map
        self.roots = [self.map_nodes[root] for root in self.get_root_mappings()]
    def get_root_mappings(self):
        G = self.map_node_map
        childrenMaps = flatten(flatten([[children[1:-1] for children in vals if type(children) == type([])] for vals in G.values()]))
        return list(set(G.keys()) - set(childrenMaps))
    def postorder(self):
        return ReconGraphPostorder(self)
    def preorder(self):
        return reversed(list(self.postorder()))

class ReconGraphPostorder(object):
    def __init__(self, G):
        self.G = G
        self.q = G.roots[:]
        self.visited = set([])
    def __iter__(self):
        return self
    def next(self):
        if len(self.q) == 0:
            raise StopIteration
        nxt = self.q.pop()
        new_children = len(filter(lambda c: c not in self.visited, nxt.children))
        if new_children == 0:
            self.visited.add(nxt)
            return nxt
        else:
            self.q.append(nxt)
            for child in nxt.children:
                if child not in self.visited:
                    self.q.append(child)
            return self.next()

def _subcounts(graph, template_event_set):
    table = {}
    for n in graph.postorder():
        if n.isLeaf():
            table[n] = DistanceFunction.kronicker(-1)
        elif n.ty == MAP_NODE:
            table[n] = reduce(lambda x, y: x.sum(y), \
                                       [table[c] for c in n.children])
        else:
            shift_amount = 1 if n not in template_event_set else -1
            table[n] = reduce(lambda x, y: x.convolve(y), \
                                       [table[c] for c in n.children])
            table[n] = table[n].shift(shift_amount)
    return table

def _supercounts(graph, template_event_set, subcount_table):
    table = {}
    for n in graph.preorder():
        if n.isRoot():
            table[n] = DistanceFunction.kronicker(0)
        elif n.ty == MAP_NODE:
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
    count_table = {}
    offset = len(template_event_set)
    for n in graph.postorder():
        count_table[n] = \
                subcount_table[n].convolve(supercount_table[n]).shift(offset)
    return count_table

def counts(graph, template_event_set):
    subcount_table = _subcounts(graph, template_event_set)
    supercount_table = _supercounts(graph, template_event_set, subcount_table)
    return subcount_table, \
            supercount_table, \
            _counts(graph, template_event_set, subcount_table, supercount_table)

def _subcounts_n(graph, template_event_set_s, fn_class):
    table = {}
    for n in graph.postorder():
        if n.isLeaf():
            table[n] = fn_class.kronicker(
                    tuple(-1 for i in xrange(len(template_event_set_s))))
        elif n.ty == MAP_NODE:
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
        elif n.ty == MAP_NODE:
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
    return subcount_table, \
            supercount_table, \
            _counts_n(graph, template_event_set_s, subcount_table, supercount_table)

def sparse_counts_n(graph, template_event_set_s):
    return counts_n(graph, template_event_set_s, SparseNDistanceFunction)

def dense_counts_n(graph, template_event_set_s):
    return counts_n(graph, template_event_set_s, NDistanceFunction)


def get_template(graph):
    events = set([])
    stack = [random.choice(graph.roots)]
    while len(stack) > 0:
        n = stack.pop()
        if n.ty != MAP_NODE:
            events.add(n)
            for c in n.children:
                stack.append(c)
        else:
            stack.append(random.choice(n.children))
    return events

maximize_best_tables = []
maximize_trace_tables = []
maximize_results = []
maximize_calls = 0

def maximize(graph, value_table, default=0):
    ''' Given a reconciliation graph and a value mapping, returns
    the event set of the reconciliation which maximizes the sum of
    the value function over its nodes '''

    # The value of the best subreconciliation rooted at each node
    best_value = {}
    # The index of the child used to get that subreconciliation
    #  (-1 for all)
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
        else:
            best_value[n] = sum(best_value[c] for c in n.children)
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
        event_set.add(n)

    global maximize_calls, maximize_results, maximize_best_tables, maximize_trace_tables
    maximize_calls += 1
    maximize_best_tables.append(best_value)
    maximize_trace_tables.append(used_child_index)
    maximize_results.append(event_set)
    return best_value, used_child_index, event_set

def k_means_step(graph, reps):
    ''' Given a
        graph - reconciliation graph
        reps  - a list of reconciliations in event-set form
    returns a new list of representatives.'''
    _, _, counts = sparse_counts_n(graph, reps)
    value_maps = [defaultdict(float) for rep in reps]
    ct = [0, 0]
    for n in graph.postorder():
        for pt in counts[n].map:
            minDist = min(pt)
            number = counts[n].map[pt]
            closest_rep_i_s = [i for (i, d) in enumerate(pt) if d == minDist]
            if len(closest_rep_i_s) > 1:
                ct[1] += 1
            else:
                ct[0] += 1
            for i in closest_rep_i_s:
                value_maps[i][n] += float(number) / len(closest_rep_i_s)
    print '%d diff and %d equisdistant dists' % tuple(ct)
    p = [[value_map[n] for value_map in value_maps] for n in value_maps[0]]
    print 'Number of reconciliations: %d' % sum(counts[graph.roots[0]].map.values())
    # print p
    res = [maximize(graph, value_map) for value_map in value_maps]
    q = [r[0][graph.roots[0]] for r in res]
    print 'Value of each representative: %s' % q
    print 'Net value: %d' % sum(q)
    return [r[2] for r in res]

def k_means_step_many(graph, reps, steps):
    for i in xrange(steps):
        new_reps = k_means_step(graph, reps)
        stable = reps == new_reps
        print 'Stable' if stable else 'Unstable'
        reps = new_reps
        if stable:
            print 'Early exit after %d iterations' % (i + 1)
            break
    return reps

def k_means(graph, steps, k, seed=0):
    print '==========================='
    print 'K means starting with k = %d, seed = %d' % (k, seed)
    random.seed(seed)
    reps = [get_template(graph) for i in xrange(k)]
    end_reps = k_means_step_many(graph, reps, steps)
    return end_reps

f = open('t.g')
G = eval(f.read())
f.close()

GG = ReconGraph(G)

r = GG.roots[0]

rep1 = []
# rep1 = k_means(GG, 10, 1)
rep2s = [k_means(GG, 10, 2, seed) for seed in xrange(10)]
rep3s = [[]]
rep3s = [k_means(GG, 10, 3, seed) for seed in xrange(4)]
reps = rep1 + flatten(rep2s) + flatten(rep3s)

for r1, r2 in it.product(reps, reps):
    if r1 != r2:
        print 'Different results from 2 K-means'

def unique(L):
    out = []
    for l in L:
        if l not in out:
            out.append(l)
    return out

print 'Maximize was called %d times' % maximize_calls
print 'It returned %d different maximum tables' % len(unique(maximize_best_tables))
print 'It returned %d different trace tables' % len(unique(maximize_trace_tables))
print 'It returned %d different representatives' % len(unique(maximize_results))
