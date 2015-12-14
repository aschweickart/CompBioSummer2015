# This file holds a function to generate sudo-reconciliation graphs of
#   this form:
#
#   Note : 'M' means Map-node, 'E' means Event-node
#
#        M
#     /     \
#    E       E
#    |       |
#    M       M     |
#   / \     / \    |  This is one layer
#  E   E   E   E   |
#  |   |   |   |   |
#  M   M   M   M   |
#  |   |   |   |   |
#  E   E   E   E   |
#   \ /     \ /
#    M       M     |
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
    middle_nodes_by_layer = [(map_nodes[1 + 2 * i],
                              map_nodes[2 + 2 * i],
                              map_nodes[3 + 2 * i],
                              map_nodes[4 + 2 * i],
                              map_nodes[5 + 2 * i],
                              map_nodes[6 + 2 * i]) for i in xrange(k)]
    middle_nodes_by_layer.append(map_nodes[-3:-1])
    graph_dict[top_node] = [ ['L', middle_nodes_by_layer[0][0]],
                             ['L', middle_nodes_by_layer[0][1]] ]
    N = (None, None)
    K = 0
    for i in xrange(k-1):
        graph_dict[middle_nodes_by_layer[i][0]] = [ ['L', middle_nodes_by_layer[i][2], N, K],
                                                    ['L', middle_nodes_by_layer[i][3], N, K] ]
        graph_dict[middle_nodes_by_layer[i][1]] = [ ['L', middle_nodes_by_layer[i][4], N, K],
                                                    ['L', middle_nodes_by_layer[i][5], N, K] ]
        graph_dict[middle_nodes_by_layer[i][2]] = [ ['L', middle_nodes_by_layer[i+1][0], N, K] ]
        graph_dict[middle_nodes_by_layer[i][3]] = [ ['L', middle_nodes_by_layer[i+1][0], N, K] ]
        graph_dict[middle_nodes_by_layer[i][4]] = [ ['L', middle_nodes_by_layer[i+1][1], N, K] ]
        graph_dict[middle_nodes_by_layer[i][5]] = [ ['L', middle_nodes_by_layer[i+1][1], N, K] ]
    graph_dict[middle_nodes_by_layer[-1][0]] = [ ['L', bottom_node, N, K] ]
    graph_dict[middle_nodes_by_layer[-1][1]] = [ ['L', bottom_node, N, K] ]
    graph_dict[bottom_node] = [ ['C', N, N, K] ]

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
