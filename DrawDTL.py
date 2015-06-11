
import turtle
import math

NodeLocations = {}




#tells a turtle to draw a line from start to end and returns to its position before the function call
def connect(Turtle,Start,End):
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




def DrawDTL(treeMin,DTL):
	Bob = turtle.Turtle()