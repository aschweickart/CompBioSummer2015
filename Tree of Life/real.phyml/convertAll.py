import os
print "blah"
for fileName in os.listdir("../real.phyml"):
	# print """python convert2newick.py  "real.phyml/" """ + str(fileName) + """ --s "real.stree" -S "real.smap" """
	os.system('python convert2newick.py ' + fileName +   ' -s "../real.stree" -S "../real.smap" ')
