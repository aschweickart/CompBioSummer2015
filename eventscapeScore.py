#Goal: Use eventscape to find scores for events in a DTL graph.

#need to import xscape to get eventscape

from xscape import *

import csv

#do we need to store the regions?
def csvParse(csvFile):
	""" """
	f = open(csvFile[:-4] + ".txt", 'w')
	with open(csvFile, 'rb') as csvfile:
		Reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in Reader:
			f.write(' '.join(row))
			f.write('\n')
	f.close()

def interpretTextData(txtFile):
	"""takes as input the textFile that was converted from the eventscape output, and outputs a dictionary, eventDict, 
	that has the number of regions as keys and a list of events as values"""
	eventDict = {}
	f = open(txtFile, 'rb')
	text = f.readlines()
	for string in text:
		





