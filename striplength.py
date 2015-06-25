import os

for fileName in os.listdir("TreeLifeData"):
	if fileName.endswith('.newick'):
		f = open("TreeLifeData/" + fileName, 'r')
		cont = f.read()
		f.close()
		f = open("TreeLifeData/" + fileName, 'w')
		ignore = False
		trees = 0
		twoTrees = False
		for c in cont:
			if trees >= 2:
				twoTrees = True
			if c == ';':
				trees +=1
			if not twoTrees:
				if not ignore:
					if c  == ':':
						ignore = True
					else:
						f.write(c)
				else:
					if not c in '0123456789.':
						ignore = False
						f.write(c)
			else:
				f.write(c)