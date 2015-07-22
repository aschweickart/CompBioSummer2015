#costscape2.py
from CostVector import *
from newickFormatReader2 import *
import reconcile
import plotcostsAnalytic2 as plotcosts
from sys import argv

def outputFile(fileName):
	if fileName[-6:] == "newick":
		return fileName[:-7]
	elif fileName[-4:] =="tree":
		return fileName[:-5]

def getInput2(list):
	# Get input file name and try to open it
    treeFile=list[1]
    switchLo=list[2]
    switchHi=list[3]
    lossLo=list[4]
    lossHi=list[5]
    log=list[6]
    output = str(outputFile(treeFile)) +"costscape.pdf"
    outtext= str(outputFile(treeFile)) + "costscape.txt"
    while True:
        fileName = treeFile
        if fileName.endswith(".newick"):
        	try:
        		fileHandle = open(fileName, 'r')
        		break
        	except IOError:
        		print "Error reading file. Please try again"
                break
        else:
            return False
    hostTree, parasiteTree, phi = newickFormatReader(fileHandle)
    fileHandle.close()

    switchLo = float(switchLo)
    switchHi = float(switchHi)
    lossLo = float(lossLo)
    lossHi = float(lossHi)

    log = log == "True"
    CVlist = reconcile.reconcile(parasiteTree, hostTree, phi, switchLo, switchHi, lossLo, lossHi)

    plotcosts.plotcosts(CVlist, switchLo, switchHi, lossLo, lossHi, output, outtext, log, False)

def main():
	getInput2(argv)



if __name__ == '__main__':
	main()