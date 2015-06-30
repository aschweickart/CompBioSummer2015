import MasterReconciliation
import os

for fileName in os.listdir("TreeLifeData"):
	if fileName.endswith('.newick'):
		geneName = fileName[:-7]
		numRecon, leaves, greedScores, consistancies = MasterReconciliation.Reconcile("TreeLifeData/" + fileName, 2 , 3, 1, "all", 0)
		scoreSum = 0
		for score in greedScores:
			scoreSum += score
		f = open("TreeLifeFreqResults/" + geneName +".rnb", 'w')
		f.write(geneName + '\n' + '\n')
		f.write("Frequency Scoring\n\n")
		f.write('Leaves:\t' + str(leaves) + '\n')
		f.write("Reconciliations:\t" + str(numRecon) + '\n')
		f.write("Total Score:\t" + str(scoreSum) + '\n')
		for score in range(len(greedScores)):
			if consistancies[score]:
				consistant = "No Temporal Inconsistancies"
			else:
				consistant = "Temporal Inconcistancy Present"
			f.write(str(score + 1) + '.\t' + str(greedScores[score]) + '\t' + str(consistant) + '\n')
		f.close()