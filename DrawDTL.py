#DrawDTL.py
#July 2015
#Annalise and Carter

#File uses turtle graphics to render an image of the Total reconciliations graph
import turtle
import math

NodeLocations = {}


#tells a turtle to draw a line from start to end and returns to its position before the function call
def connect(Turtle,Start,End,rad):
    """Takes as input a turtle, starting coordinates, Start, and ending coordinates, End,
        as well as the radius of the nodes, and connects the two locations with a line and arrow"""
    Turtle.speed(0)
    Turtle.pen(pencolor  = "black")
    loc = Turtle.pos()
    hed = Turtle.heading()
    movr = Start[0] < End[0]
    movu = Start[1] < End[1]
    lesserY = min(Start[1],End[1])
    biggerY = max(Start[1],End[1])
    lesserX = min(Start[0],End[0])
    biggerX = max(Start[0],End[0])
    theta = 0

    #find angle of the arrow
    try:
        theta = (math.atan(float(biggerY - lesserY)/float(biggerX - lesserX)))
        if not movr and movu:
            theta = math.pi - theta
        elif not movr and not movu:
            theta = math.pi + theta
        elif movr and not movu:
            theta = (2 * math.pi) - theta
    except:
        theta = (math.pi/2)
        if not movu:
            theta += math.pi

    #adjust start and ending points so as to not draw inside nodes
    Start = (Start[0] + (rad * math.cos(theta)), Start[1])
    Start = (Start[0], Start[1] + (rad * math.sin(theta)))
    End = (End[0] - (rad * math.cos(theta)), End[1])
    End = (End[0], End[1] - (rad * math.sin(theta)))

    Turtle.penup()
    Turtle.radians()
    Turtle.seth(theta)
    Turtle.setpos(Start,None)
    Turtle.pendown()
    Turtle.goto(End,None)
    Turtle.degrees(360)
    Turtle.stamp()
    Turtle.penup()
    Turtle.goto(loc,None)
    Turtle.setheading(hed)
    Turtle.pendown()
    Turtle.ht()

def drawNodes(treeMin, eventDict, depth, nodeDict):
    """Takes as input
        treeMin   - a list of the starting nodes of the best reconciliations
        eventDict - the DTL format dictionary
        depth     - a starting y-coordinate
        nodeDict  - a dictionary of nodes and their coordinates.
    This function recursively draws the nodes of the DTL format dictionary, then
    connects them using the connect function aboves"""
    numTips = 0
    for key in eventDict.keys():
        if eventDict[key][0][0] == "C":
            numTips+=1
    width = numTips * 200
    DISPLACE = width/2
    dip = 15
    if len(eventDict)<25:
        radius = 30
    else:
        radius = 13
        dip = 15
        width = width/2
        DISPLACE = DISPLACE/2
    if treeMin == []:
        for key in nodeDict:
            for item in range(len(nodeDict[key][1:])):
                connect(turtle.Turtle(), nodeDict[key][0], nodeDict[key][item+1], radius)
                for thing in eventDict[key][item][1:-1]:
                    if thing !=(None, None):
                        connect(turtle.Turtle(), nodeDict[key][item+1], nodeDict[thing][0], radius)
        return

    difference = ((len(eventDict))*2)/numTips

    numSols = len(treeMin)
    turtle.speed(0)
    turtle.pen(pencolor = "black")
    eventList = []
    newtreeMin = []
    for x in range(len(treeMin)):
        if not treeMin[x] in nodeDict:
            nodeDict[treeMin[x]] = [((x+1)*width/(numSols + 1)-DISPLACE, depth + radius)]
            turtle.penup()
            turtle.setpos((x+1)*width/(numSols+1)-DISPLACE, depth)
            turtle.pendown()
            turtle.circle(radius)
            turtle.left(130)
            turtle.penup()
            turtle.forward(radius)
            turtle.pendown()
            turtle.right(130)
            turtle.write(treeMin[x], font = ("arial", 12, "normal"))
            for y in eventDict[treeMin[x]]:
                if type(y)== list:
                    eventList.append((y[0], treeMin[x]))
                    if y[1] !=(None, None) and not y[1] in newtreeMin:
                        newtreeMin.append(y[1])
                    if y[2] !=(None, None) and not y[2] in newtreeMin:
                        newtreeMin.append(y[2])
    numEvents = len(eventList)
    for event in range(len(eventList)):
        turtle.penup()
        nodeDict[eventList[event][1]].append(((event+1)*width/(numEvents+1)-DISPLACE, depth -(difference-radius)))
        turtle.setpos(((event+1)*width/(numEvents+1))-DISPLACE, depth - difference)
        turtle.pendown()
        turtle.circle(radius)
        turtle.left(95)
        turtle.penup()
        turtle.forward(radius)
        turtle.pendown()
        turtle.right(95)
        turtle.write(eventList[event][0], font = ("arial", 12, "normal"))
        turtle.ht()
    drawNodes(newtreeMin, eventDict, depth - 2*difference, nodeDict)
