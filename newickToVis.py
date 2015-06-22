

from rasmus import treelib1, util
import copy
import sys

def convert(fileName, HostOrder):

    f = open(fileName, 'r')
    contents = f.read()
    f.close()
    H,P,phi = contents.split(";")
    P = P.strip()
    H = H.strip()
    H = H + ';'
    host = treelib1.parse_newick(H, HostOrder)
  
    # for key in HostOrder:
    #     H = H.replace(str(key), str(key) + ':' + str(HostOrder[key]))
    f = open(fileName[:-7]+".stree", 'w')
    write_newick(host, f)
    f.close()
    f = open(fileName[:-7] + '.tree', 'w')
    f.write(P + ";")
    f.close


def write_newick(tree, out=sys.stdout, write_data=None, oneline=False,
                 root_data=False, namefunc=lambda name: name):
    """Write the tree in newick notation"""
    write_newick_node(tree, tree.root, util.open_stream(out, "w"),
                      write_data=write_data, oneline=oneline,
                      root_data=root_data, namefunc=namefunc)


def write_newick_node(tree, node, out=sys.stdout,
                      depth=0, write_data=None, oneline=False,
                      root_data=False, namefunc=lambda name: name):
    """Write the node in newick format to the out file stream"""

    # default data writer
    if write_data is None:
        writeDist = any(node.dist != 0 for node in tree)
        write_data = lambda node: tree.write_data(node, writeDist=writeDist, namefunc=namefunc)

    if not oneline:
        out.write(" " * depth)

    if len(node.children) == 0:
        # leaf
        out.write(str(namefunc(node.name)))
    else:
        # internal node
        if oneline:
            out.write("(")
        else:
            out.write("(\n")
        for child in node.children[:-1]:
            write_newick_node(tree, child, out, depth+1,
                              write_data=write_data, oneline=oneline,
                              namefunc=namefunc)
            if oneline:
                out.write(",")
            else:
                out.write(",\n")
        write_newick_node(tree, node.children[-1], out, depth+1,
                          write_data=write_data, oneline=oneline,
                          namefunc=namefunc)
        if oneline:
            out.write(")")
        else:
            out.write("\n" + (" " * depth) + ")")

    # don't print data for root node
    if depth == 0:
        if root_data:
            out.write(write_data(node))
        if oneline:
            out.write(";")
        else:
            out.write(";\n")
    else:
        out.write(write_data(node))