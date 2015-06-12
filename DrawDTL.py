
import turtle
import math

NodeLocations = {}


DISPLACE = 500

#tells a turtle to draw a line from start to end and returns to its position before the function call
def connect(Turtle,Start,End):
	Turtle.speed(0)
	Turtle.pen(pencolor  = "black")
	loc = Turtle.pos()
	hed = Turtle.heading()
	movr = Start[0] < End[0]
	movu = Start[1] < End[1]
	lessery = min(Start[1],End[1])
	biggery = max(Start[1],End[1])
	lesserx = min(Start[0],End[0])
	biggerx = max(Start[0],End[0])
	theta = 0
	try:
		theta = (math.atan(float(biggery - lessery)/float(biggerx - lesserx)))
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
	Start = (Start[0] + (30 * math.cos(theta)), Start[1])
	Start = (Start[0], Start[1] + (30 * math.sin(theta)))
	End = (End[0] - (30 * math.cos(theta)), End[1])
	End = (End[0], End[1] - (30 * math.sin(theta)))
	Turtle.penup()
	Turtle.radians()
	Turtle.seth(theta)
	Turtle.setpos(Start,None)
	Turtle.pendown()
	Turtle.goto(End,None)
	Turtle.stamp()
	Turtle.degrees(360)
	Turtle.penup()
	Turtle.goto(loc,None)
	Turtle.setheading(hed)
	Turtle.pendown()
def connectNodes(start, end):
	turtle.penup()
	turtle.setpos(start)
	turtle.pendown()
	turtle.setpos(end)
	turtle.left(135)
	turtle.forward(10)
	turtle.right(180)
	turtle.forward(10)
	turtle.left(90)
	turtle.forward(10)
	turtle.right(180)
	turtle.forward(10)
	turtle.left(135)
	# a = start[0]
	# b = start[1]
	# c = end[0]
	# d = end[1]
	# x = (a-c)/(b-d)
	# rads = math.atan(x)
	# angle = rads * (180/math.pi)
	# turtle.penup()
	# turtle.right(angle)
	# turt
def drawNodes(treeMin, eventDict, depth, nodeDict):
	if treeMin == []:
		return
	for key in eventDict.keys():
		numTips = 0
		if eventDict[key][0][0] == "C":
			numTips+=1
	width = numTips * 1000
	numSols = len(treeMin)
	turtle.speed(0)
	turtle.pen(pencolor = "black")
	eventList = []
	newtreeMin = []
	for x in range(len(treeMin)):
		if not treeMin[x] in nodeDict:
			nodeDict[treeMin[x]] = [((x+1)*width/(numSols+1)-DISPLACE, depth)]
			turtle.penup()
			turtle.setpos((x+1)*width/(numSols+1)-DISPLACE, depth)
			turtle.pendown()
			turtle.circle(30)
			turtle.left(130)
			turtle.penup()
			turtle.forward(30)
			turtle.pendown()
			turtle.right(130)
			turtle.write(treeMin[x], font = ("arial", 12, "normal"))
		# print treeMin[x]
		# print eventDict[treeMin[x]]
			for y in eventDict[treeMin[x]]:
				if type(y)== list:
					eventList.append((y[0], treeMin[x]))

					if y[1] !=(None, None) and not y[1] in newtreeMin:
						newtreeMin.append(y[1])
					if y[2] !=(None, None) and not y[2] in newtreeMin:
						newtreeMin.append(y[2])
			print eventList
	numEvents = len(eventList)
	for event in range(len(eventList)):
		turtle.penup()
		nodeDict[eventList[event][1]].append(((event+1)*width/(numEvents+1)-DISPLACE, depth - 40))
		turtle.setpos((event+1)*width/(numEvents+1)-DISPLACE, depth - 100)
		turtle.pendown()
		turtle.circle(30)
		turtle.left(95)
		turtle.penup()
		turtle.forward(30)
		turtle.pendown()
		turtle.right(95)
		turtle.write(eventList[event][0], font = ("arial", 12, "normal"))
	drawNodes(newtreeMin, eventDict, depth - 200, nodeDict)
# <<<<<<< HEAD
	for key in nodeDict.keys():
		events = eventDict[key]
		for n in range(len(nodeDict[key][1:])):
			connectNodes(nodeDict[key][0], nodeDict[key][n+1])
			if events[n][1] != (None, None):
				connectNodes((nodeDict[key][n+1][0], nodeDict[key][n+1][1]-60), (nodeDict[events[n][1]][0][0],nodeDict[events[n][1]][0][1]+60))
			if events[n][2] != (None, None):	
				connectNodes((nodeDict[key][n+1][0], nodeDict[key][n+1][1]-60), (nodeDict[events[n][2]][0][0],nodeDict[events[n][2]][0][1]+60))
# =======
# 	for key in nodeDict:
# 		for item in nodeDict[key][:-1]:
# 			connect(turtle.Turtle(), nodeDict[key], nodeDict[key][item + 1] )
# >>>>>>> origin/Team_DP-Branch

def DrawDTL(treeMin,DTL):
	Bob = turtle.Turtle()