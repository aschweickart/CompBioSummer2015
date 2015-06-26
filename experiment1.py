import MasterReconciliation
import os

for fileName in os.listdir("TreeLifeData"):
	if fileName.endswith('.newick'):
		geneName = fileName[:-7]
		numRecon, leaves, greedScores, consistancies = MasterReconciliation.Reconcile("TreeLifeData/" + fileName, 2 , 3, 1, "all")
		scoreSum = 0
		for score in greedScores:
			scoreSum += score
		f = open("TreeLifeResults/" + geneName +".rnb", 'w')
		f.write(geneName + '\n' + '\n')
		f.write("Frequency Scoring\n\n")
		f.write(str(leaves) + ' Leaves\n')
		f.write(str(numRecon) + " Reconciliations\n")
		f.write(str(scoreSum) + "Total Score\n")
		for score in range(len(greedScores)):
			if consistancies[score]:
				consistant = "No Temporal Inconsistancies"
			else:
				consistant = "Temporal Inconcistancy Present"
			f.write(str(score + 1) + '.\t' + str(greedScores[score]) + '\t' + str(consistant) + '\n')
		f.close()