import os
print "blah"
for fileName in os.listdir("../real.phyml"):
	print fileName
	os.system('python convert2newick.py ' + fileName + ' -s "../real.stree" -S "../real.smap"')
for fileName in os.listdir("../real.phyml"):
	if fileName.endswith(".newick"):
					os.rename(fileName, "../../../TreeLifeData/" + fileName)