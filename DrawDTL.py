
import turtle

NodeLocations = {}




#tells a turtle to draw a line from start to end and returns to its position before the function call
def connect(Turtle,Start,End):
	loc = Turtle.pos()
	Turtle.penup()
	Turtle.setpos(Start,None)
	Turtle.pendown()
	Turtle.goto(End,None)
	Turtle.stamp()
	Turtle.penup()
	Turtle.goto(loc,None)
	Turtle.pendown()




def DrawDTL(treeMin,DTL):
	Bob = turtle.Turtle()