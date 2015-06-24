
from collections import defaultdict

from rasmus import treelib1, svg, util, stats
from compbio import phylo


def draw_stree(canvas, stree, slayout,
               yscale=100,
               stree_width=.8, 
               stree_color=(.4, .4, 1),
               snode_color=(.2, .2, .4)):

    # draw stree branches
    for node in stree:
        x, y = slayout[node]
        px, py = slayout[node.parent]
        
        # draw branch
        w = yscale * stree_width / 2.0
        canvas.polygon([px, py-w,
                        x, y-w,
                        x, y+w,
                        px, py+w], strokeColor=(0, 0, 0, 0),
                       fillColor=stree_color)


    # draw stree nodes
    for node in stree:
        if not node.is_leaf():
            x, y = slayout[node]
            canvas.line(x, y-w, x, y+w, color=snode_color,
                        style="stroke-dasharray: 1, 1")
    


def draw_tree(tree, brecon, stree,
              xscale=100, yscale=100,
              leaf_padding=10, 
              label_size=None,
              label_offset=None,
              font_size=12,
              stree_font_size=20,
              canvas=None, autoclose=True,
              rmargin=10, lmargin=10, tmargin=0, bmargin=0,
              tree_color=(0, 0, 0),
              tree_trans_color=(0, 0, 0),
              stree_color=(.6, .3, .8),
              snode_color=(.2, .2, .7),
              loss_color = (1,1,1),
              loss_color_border=(.5,.5,.5),
              dup_color=(1, 0, 0),
              dup_color_border=(.5, 0, 0),
              trans_color=(0, 1, 0),
              trans_color_border=(0, .5, 0),
              event_size=10,
              snames=None,
              rootlen=None,
              stree_width=.8,
              filename="tree.svg"
              ):

    # set defaults
    font_ratio = 8. / 11.

    
    if label_size is None:
        label_size = .7 * font_size

    #if label_offset is None:
    #    label_offset = -1

    if sum(x.dist for x in tree.nodes.values()) == 0:
        legend_scale = False
        minlen = xscale

    if snames is None:
        snames = dict((x, x) for x in stree.leaf_names())

    # layout stree
    slayout = treelib1.layout_tree(stree, xscale, yscale)
    if rootlen is None:
        rootlen = .1 * max(l[0] for l in slayout.values())

    # setup slayout
    x, y = slayout[stree.root]
    slayout[None] =  (x - rootlen, y)
    for node, (x, y) in slayout.items():
        slayout[node] = (x + rootlen, y  - .5 * yscale)

    # layout tree
    ylists = defaultdict(lambda: [])
    yorders = {}

    # layout speciations and genes (y)
    for node in tree.preorder():
        for ev in brecon[node]:
            snode, event, frequency = ev
            if event == "spec" or event == "gene" or event == "loss":
                yorders[node] = len(ylists[snode])
                ylists[snode].append(node)
    # layout dups and transfers (y)
    for node in tree.postorder():
        for ev in brecon[node]:
            snode, event, frequency = ev
            if event != "spec" and event != "gene" and event != "loss":
                v = [yorders[child]
                    for child in node.children
                    if brecon[child][-1][0] == snode]
                if len(v) == 0:
                    yorders[node] = 0
                else:
                    yorders[node] = stats.mean(v)

    # layout node (x)
    xorders = {}
    xmax = defaultdict(lambda: 0)
    for node in tree.postorder():
        for ev in brecon[node]:
            snode, event, frequency = ev
            if event == "spec" or event == "gene" or event == "loss":
                xorders[node] = 0
            else:
                v = [xorders[child] for child in node.children
                    if brecon[child][-1][0] == snode]
                if len(v) == 0:
                    xorders[node] = 1
                else:
                    xorders[node] = max(v) + 1
            xmax[snode] = max(xmax[snode], xorders[node])

    # setup layout
    layout = {None: [slayout[brecon[tree.root][-1][0].parent]]}
    for node in tree:
        for ev in brecon[node]:
            snode, event, frequency = ev
            nx, ny = slayout[snode]
            px, py = slayout[snode.parent]

        # calc x
            frac = (xorders[node]) / float(xmax[snode] + 1)
            deltax = nx - px
            x = nx - frac * deltax

        # calc y
            deltay = ny - py
            slope = deltay / float(deltax)
            deltax2 = x - px
            deltay2 = slope * deltax2
            offset = py + deltay2
        
            frac = (yorders[node] + 1) / float(max(len(ylists[snode]), 1) + 1)
            y = offset + (frac - .5) * stree_width * yscale

            if node in layout: layout[node].append((x, y))
            else:
                layout[node] = [(x, y)]
        brecon[node] = orderLoss(node, brecon, layout)
        print "Brecon = ", brecon[node]
        layout[node] = orderLayout(node, layout)
        print "Layout = ", layout[node]
        if y > max(l[1] for l in slayout.values()) + 50:
            print nx, ny
            print px, py
            print offset, frac
            print ylists[snode], yorders[node]
            print brecon[node]
            print node, snode, layout[node]


    # layout label sizes
    max_label_size = max(len(x.name)
        for x in tree.leaves()) * font_ratio * font_size
    max_slabel_size = max(len(x.name)
        for x in stree.leaves()) * font_ratio * stree_font_size

    

    '''
    if colormap == None:
        for node in tree:
            node.color = (0, 0, 0)
    else:
        colormap(tree)
    
    if stree and gene2species:
        recon = phylo.reconcile(tree, stree, gene2species)
        events = phylo.label_events(tree, recon)
        losses = phylo.find_loss(tree, stree, recon)
    else:
        events = None
        losses = None
    
    # layout tree
    if layout is None:
        coords = treelib.layout_tree(tree, xscale, yscale, minlen, maxlen)
    else:
        coords = layout
    '''
    
    xcoords, ycoords = zip(* slayout.values())
    maxwidth = max(xcoords) + max_label_size + max_slabel_size
    maxheight = max(ycoords) + .5 * yscale
    
    
    # initialize canvas
    if canvas is None:
        canvas = svg.Svg(util.open_stream(filename, "w"))
        width = int(rmargin + maxwidth + lmargin)
        height = int(tmargin + maxheight + bmargin)
        
        canvas.beginSvg(width, height)
        canvas.beginStyle("font-family: \"Sans\";")
        
        if autoclose == None:
            autoclose = True
    else:
        if autoclose == None:
            autoclose = False

    canvas.beginTransform(("translate", lmargin, tmargin))
    
    draw_stree(canvas, stree, slayout,
               yscale=yscale,
               stree_width=stree_width, 
               stree_color=stree_color,
               snode_color=snode_color)

    # draw stree leaves
    for node in stree:
        x, y = slayout[node]
        if node.is_leaf():
            canvas.text(snames[node.name], 
                        x + leaf_padding + max_label_size,
                        y+stree_font_size/2., stree_font_size,
                        fillColor=snode_color)


    # draw tree

    for node in tree:
        containsL= containsLoss(node, brecon)
        for n in range(len(brecon[node])):
            # print brecon[node]
            x, y = layout[node][n]
            # print layout[node]
            if containsL == False:
                px, py = layout[node.parent][-1]       
            else:
                if brecon[node][n][1] == "loss":
                    px, py = layout[node.parent][-1]
                else: 
                    px, py = layout[node][n-1]
            

            trans = False

            if node.parent:
                for ev in brecon[node]:
                    snode, event, frequency =  ev
                    psnode = brecon[node.parent][-1][0]
                while snode:
                    if psnode == snode:
                        break
                    snode = snode.parent
                else:
                    trans = True

            if not trans:
                canvas.line(x, y, px, py, color=tree_color)
            else:
                arch = 20
                x2 = (x*.5 + px*.5) - arch
                y2 = (y*.5 + py*.5)
                x3 = (x*.5 + px*.5) - arch
                y3 = (y*.5 + py*.5)
            
                canvas.write("<path d='M%f %f C%f %f %f %f %f %f' %s />\n " %
                         (x, y, x2, y2,
                          x3, y3, px, py,
                          " style='stroke-dasharray: 4, 2' " +
                          svg.colorFields(tree_trans_color, (0,0,0,0))))

    # draw events
    for node in tree:
        for n in range(len(brecon[node])):
            snode, event, frequency =  brecon[node][n]
            x, y = layout[node][n]
            o = event_size / 2.0
            if event == "loss":
                canvas.rect(x - o, y - o, event_size, event_size,
                        fillColor=loss_color,
                        strokeColor=loss_color_border)
                canvas.text(frequency, x-o, y-o, font_size, fillColor = (1,1,1))
	
            if event == "spec":
                canvas.text(frequency, slayout[snode][0]-leaf_padding/2, slayout[snode][1]-font_size, font_size, fillColor = (0,0,0))

            if event == "dup":
                canvas.rect(x - o, y - o, event_size, event_size,
                        fillColor=dup_color,
                        strokeColor=dup_color_border)
                canvas.text(frequency, x-o, y-o, font_size, fillColor=dup_color)
            elif event == "trans":
                canvas.rect(x - o, y - o, event_size, event_size,
                        fillColor=trans_color,
                        strokeColor=trans_color_border)
                canvas.text(frequency, x-o, y-o, font_size, fillColor=trans_color)

    # draw tree leaves
    for node in tree:
        for n in range(len(brecon[node])):
            x, y = layout[node][n]
            if node.is_leaf() and containsLoss(node, brecon) == False:
                canvas.text(node.name, 
                        x + leaf_padding, y+font_size/2., font_size,
                        fillColor=(0, 0, 0))

        
    canvas.endTransform()
    
    if autoclose:
        canvas.endStyle()
        canvas.endSvg()
    
    return canvas

def containsLoss(node, brecon):
    containsL = False
    for n in range(len(brecon[node])):
        if brecon[node][n][1] == "loss":
            containsL = True
    return containsL
def orderLoss(node, brecon, layout):
    eventDict = {}
    for n in range(len(brecon[node])):
        eventDict[str(brecon[node][n])] = layout[node][n]
    return sorted(brecon[node], key=lambda xCoord: eventDict[str(xCoord)][0])

def orderLayout(node, layout):
    return sorted(layout[node], key=lambda xCoord: xCoord[0])



