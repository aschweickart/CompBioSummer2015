import MasterReconciliation
import os

for fileName in os.listdir("TreeLifeData"):
	geneName = fileName[:-7]
	numRecon, greedScores, leaves, scoreSum = MasterReconciliation.Reconcile("TreeLifeData/" + fileName, 2 , 3, 1, "all")
	f = open("TreeLifeResults/" + geneName +".rnb")
	f.write(geneName + '\n' + '\n')
	f.write("Frequency Scoring\n\n")
	f.write(leaves + " Leaves\n")
	f.write(numRecon + " Reconciliations\n")
	f.write(scoreSum + "Total Score\n")
	for score in range(len(greedScores)):
		f.write(str(score + 1) + '.\t' + str(greedScores[score] + '\n'))
	f.close()