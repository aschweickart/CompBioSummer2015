import timeit
import Queue
import copy
import operator
import itertools as it

flatten = lambda l: reduce(operator.add, l)

# Nodes in a reconcilliation graph can be of different types.
MAP_NODE      = 'map-node' # A map-node (the rest are subtypes of event-node)
COSPECIATION  = 'S'
LEAF_PAIR     = 'C'        # Leaf-to-leaf mappings have this after them
TRANSFER      = 'T'
DUPLICATION   = 'D'
LOSS          = 'L'

NO_CHILD = (None, None)

class Node(object):
    '''  A node in a reconciliation graph '''
    def __init__(self, ty, mapping = None):
        ''' A node is created with just a type and optional
        (parasite-to-host mapping).

        It maintains both children and parent pointers

        The type is either a map-node, or some type of event, as found at
        the head of the file.
        '''
        self.children = []
        self.c = self.children # shortcut
        self.parents = []
        self.ty = ty
        self.mapping = mapping
    def mc(self,i):
        '''shortcut'''
        return self.c[i].c[0]
    def __repr__(self):
        if self.isMap():
            return '<Node type: %s, mapping: %s, #child: %d, #parent: %d>' % \
                    (self.ty, self.mapping, len(self.children), len(self.parents))
        else:
            return '<Node type: %s, parent mapping:%s, #child: %d>' % \
                    (self.ty, self.parents[0].mapping, len(self.children))
    def isLeaf(self):
        return len(self.children) == 0
    def isRoot(self):
        return len(self.parents) == 0
    def isEvent(self):
        return self.ty != MAP_NODE
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
    ''' A representation of a Reconciliation Graph as a bunch of nodes in
    memory with pointers between them.

    Parent pointers are maintained'''
    def __init__(self, map_node_map):
        # A dictionary which maps (parasite-to-host mappings) to nodes in the
        # graph
        self.map_nodes = {}

        def get_or_make_map_node(mapping):
            '''Gets the node for a parasite-to-host mapping, creating a new
            node for the mapping if needed'''
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
        childrenMaps = flatten(flatten([[children[1:-1] for children in vals \
                if type(children) == type([])] for vals in G.values()]))
        return list(set(G.keys()) - set(childrenMaps))
    def postorder(self):
        ''' Visit the nodes child-first.
        reasonably efficient'''
        return ReconGraphPostorder(self)
    def preorder(self):
        ''' Visit the nodes parent-first.
        Inefficient'''
        return reversed(list(self.postorder()))
    def __len__(self):
        ct = 0
        for n in self.postorder():
            ct += 1
        return ct

class ReconGraphPostorder(object):
    ''' Iterator class for post-order travesals of the Reconciliation Graph '''
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

def dictRecToSetRec(graph, dictRec):
    '''
    Given
        dictRec - a single reconciliation in dictionary form
        graph - a reconciliation graph in nodes-in-memory form

    returns the reconciliation as a set of event nodes in the graph

    dictRec should be a Map<Mapping,Event> where Event = (Type,Child1,Child2)

    As an example:
    {
        ('n50', 'm117') : ['L', ('n49', 'm116'), (None, None)],
        ...
    }
    '''
    roots_in_rec = filter(lambda root: root.mapping in dictRec, graph.roots)
    assert len(roots_in_rec) == 1, '''
        The dictionary form reconciliation %s should have exactly 1 root node
        in the graph %s, but actually had %d {%s}''' % \
                (dictRec, graph, len(roots_in_rec), roots_in_rec)
    setRec = set([])
    map_node_stack = roots_in_rec
    while len(map_node_stack) > 0:
        node = map_node_stack.pop()
        candidate_events = []
        for eventNode in node.children:
            if eventNode.ty == dictRec[node.mapping][0]:
                if set(c.mapping for c in eventNode.children) == \
                   set([s for s in dictRec[node.mapping][1:] if s != (None, None)]):
                    candidate_events.append(eventNode)
        assert len(candidate_events) == 1, \
                'Ambiguity in which event to use. Options: %s' % candidate_events
        event = candidate_events[0]
        setRec.add(event)
        map_node_stack.extend(event.children)
    return setRec


