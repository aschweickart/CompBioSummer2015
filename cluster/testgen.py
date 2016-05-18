# This file holds a function to generate sudo-reconciliation graphs of
#   this form:
#
#   Note : 'M' means Map-node, 'E' means Event-node
#
#        M0
#     /     \
#    E       E
#    |       |
#    M1      M2    |
#   / \     / \    |  This is one layer
#  E   E   E   E   |
#  |   |   |   |   |
#  M3  M4  M5  M6  |
#  |   |   |   |   |
#  E   E   E   E   |
#   \ /     \ /
#    M7      M8    |
#   / \     / \    |  Another one
#  E   E   E   E   |
#  |   |   |   |   |
#  M   M   M   M   |
#  |   |   |   |   |
#  E   E   E   E   |
#   \ /     \ /
#        .
#        .
#        .
#    M       M     |
#   / \     / \    |
#  E   E   E   E   |
#  |   |   |   |   |
#  M   M   M   M   | Last one
#  |   |   |   |   |
#  E   E   E   E   |
#   \ /     \ /
#    M       M
#     \     /
#        E
#        |
#        M
#        |
#        E

def apply_iter(format_fn, k):
    return (format_fn(i) for i in xrange(k))

def augment(graph_dict, mapping):
    ''' Given a graph_dict and a mapping to enhance, adds a extra path
    from that mapping to one of its children '''
    f, t = mapping
    # We will create a new path away from our map node by making an
    # intermediate map node and going through with (one loss in, one loss out)
    # That node with have this name:
    extension = (f + 'X', t)
    K = 0
    N = (None, None)
    # Go though each event child of `mapping` to find an event which only one
    # child (A loss)
    for child in graph_dict[mapping][:-1]:
        if child[2] == N:
            # Then map the extra map node to the child of that event
            graph_dict[extension] = [['L', child[1], N, K], K]
            # Then add the extra map to the children of `mapping`
            graph_dict[mapping] = graph_dict[mapping][:1] + \
                                  [['L', extension, N, K]] + \
                                  graph_dict[mapping][1:]
            return graph_dict
    assert False, "Failed: No children with 1 child"

def gen(k):
    ''' Given
        k -  number of layers >= 1
    returns a dictionary representing a reconciliation graph of the above form
    with k layers.'''
    graph_dict = {}
    def i_to_map(i):
        return ('m%d' % i, 'n')
    # 1 for top, 2 per layer, 3 for bottom
    number_of_map_nodes = 1 + 6 * k + 3
    map_nodes = list(apply_iter(i_to_map, number_of_map_nodes))
    top_node = map_nodes[0]
    bottom_node = map_nodes[-1]
    middle_nodes_by_layer = [(map_nodes[1 + 6 * i],
                              map_nodes[2 + 6 * i],
                              map_nodes[3 + 6 * i],
                              map_nodes[4 + 6 * i],
                              map_nodes[5 + 6 * i],
                              map_nodes[6 + 6 * i]) for i in xrange(k)]
    middle_nodes_by_layer.append(map_nodes[-3:-1])
    N = (None, None)
    K = 0

    graph_dict[top_node] = [ ['L', middle_nodes_by_layer[0][0], N, K],
                             ['L', middle_nodes_by_layer[0][1], N, K], K ]

    for i in xrange(k):
        graph_dict[middle_nodes_by_layer[i][0]] = [
                ['L', middle_nodes_by_layer[i][2], N, K],
                ['L', middle_nodes_by_layer[i][3], N, K], K ]
        graph_dict[middle_nodes_by_layer[i][1]] = [
                ['L', middle_nodes_by_layer[i][4], N, K],
                ['L', middle_nodes_by_layer[i][5], N, K], K ]
        graph_dict[middle_nodes_by_layer[i][2]] = [
                ['L', middle_nodes_by_layer[i+1][0], N, K], K ]
        graph_dict[middle_nodes_by_layer[i][3]] = [
                ['L', middle_nodes_by_layer[i+1][0], N, K], K ]
        graph_dict[middle_nodes_by_layer[i][4]] = [
                ['L', middle_nodes_by_layer[i+1][1], N, K], K ]
        graph_dict[middle_nodes_by_layer[i][5]] = [
                ['L', middle_nodes_by_layer[i+1][1], N, K], K ]
    graph_dict[middle_nodes_by_layer[-1][0]] = [ ['L', bottom_node, N, K], K ]
    graph_dict[middle_nodes_by_layer[-1][1]] = [ ['L', bottom_node, N, K], K ]
    graph_dict[bottom_node] = [ ['C', N, N, K], K ]

    return graph_dict

# If so we can use this.
#
#     n0
#    /  \
#   n1   \
#  /  \   \
# n2  n3  n4
# |   |   |
# m2  m3  m4
#  \   \  /
#   \   m1
#    \  /
#     m0
#
#  n0:m0
