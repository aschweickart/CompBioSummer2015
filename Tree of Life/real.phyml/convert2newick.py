
# wrapper to create newick file from stree, gtree, gene2species

import os, optparse

from rasmus import util, treelib
from compbio import phylo

#=========================================
# parser

parser = optparse.OptionParser(usage="%prog [options] <gene tree> ...")
parser.add_option("-s", "--stree", dest="stree",
                  metavar="<species tree>",
                  help="species tree file in newick format")
parser.add_option("-S", "--smap", dest="smap",
                  metavar="<gene to species map>",
                  help="species map")
parser.add_option("-I", "--inext", dest="inext",
                  metavar="<tree file extension>",
                  default=".tree",
                  help="tree file extension (default: \".tree\")")
parser.add_option("-O", "--outext", dest="outext",
                  metavar="<xscape newick file extension>",
                  default=".newick",
                  help="xscape newick file extension (default: \".newick\")")

parser.add_option("--rename", dest="rename",
                  default=False, action="store_true",
                  help="set to rename all nodes")
parser.add_option("--gmapext", dest="gmapext",
                  metavar="<gene map file extension>",
                  default=".newick.gmap",
                  help="gene map file extension (default: \".newick.gmap\")")
parser.add_option("--smapext", dest="smapext",
                  metavar="<species map file extension>",
                  default=".newick.smap",
                  help="species map file extension (default: \".newick.smap\")")

options, treefiles = parser.parse_args()

if not (options.stree and options.smap):
    parser.error("--stree and --smap are required")

#=========================================
# rename utilities

def rename_all_nodes(tree, prefix="n"):
    """Rename nodes that all names are strings"""

    # first pass
    mapping = {}
    names = set(tree.nodes)
    for node in list(tree):
        name = node.name
        name2 = tree.new_name()
        name2 = tree.unique_name(name2, names)
        tree.rename(name, name2)
        mapping[name2] = name

    # second pass
    mapping2 = {}
    for i, node in enumerate(list(tree.preorder())):
        name2 = node.name
        name3 = prefix + str(i)
        assert name3 not in tree.nodes, name3
        tree.rename(name2, name3)
        mapping2[mapping[name2]] = name3
        
    return mapping2

def rename_nodes(tree, prefix="n"):
    """Rename nodes that all names are strings"""
    mapping = {}
    for node in list(tree.postorder()):
        name = node.name
        if isinstance(name, int):
            name2 = prefix + str(name)
            assert name2 not in tree.nodes, name2
##            while name2 in tree.nodes:
##                name2 = prefix + str(tree.new_name())
            tree.rename(name, name2)
            mapping[name] = name2
        else:
            mapping[name] = name
    return mapping

if options.rename:
    rename = rename_all_nodes
else:
    rename = rename_nodes

#=========================================
# main

# read and convert species tree
stree = treelib.read_tree(options.stree)
smapping = rename(stree, prefix="m")

# remove bootstraps
for node in stree:
    if "boot" in node.data:
        del node.data["boot"]

# read gene2species mapping
gene2species = phylo.read_gene2species(options.smap)

for gtreefile in treefiles:
    # read and convert gene tree
    gtree = treelib.read_tree(gtreefile)
    gmapping = rename(gtree, prefix="n")
    gmapping2 = util.revdict(gmapping)

    # remove bootstraps
    for node in gtree:
        if "boot" in node.data:
            del node.data["boot"]

    # output
    outfile = util.replace_ext(gtreefile, options.inext, options.outext)
    out = util.open_stream(outfile, "w")
    
    stree.write(out, oneline=True, rootData=True); out.write("\n")
    gtree.write(out, oneline=True, rootData=True); out.write("\n")
    for gname2 in gtree.leaf_names():
        gname = gmapping2[gname2]
        sname = gene2species(gname)
        sname2 = smapping[sname]
        out.write("%s:%s\n" % (gname2, sname2))
    out.close()
    
    if options.rename:
        util.write_dict(util.replace_ext(gtreefile, options.inext, options.gmapext), gmapping)
        util.write_dict(util.replace_ext(gtreefile, options.inext, options.smapext), smapping)        
