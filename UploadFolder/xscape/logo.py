#logo design
import matplotlib.pyplot as plt
from shapely.geometry import *
from CostVector import *
from commonAnalytic import *


def logo():
	plt.axis([0.1, 5, 0.1, 5])

	numRegions = 6

	colorMap = [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 0.7, 0), (1, 0, 0), (1, 0, 1)]
	patternsMap = ["*", "o", "-", ".|","x|", "//" ]
	coords = [[(0.1, 0.1),(2, 1.5),(5, 1), (5, 0.1)], [(2, 1.5), (5, 1),(5, 4), (2, 1.5)], [(0.1,0.1), (4.5, 5), (5, 5), (5, 4), (2, 1.5)], [(0.1, 0.1), (1, 3), (2, 5), (4.5, 5)], [(1, 3), (2, 5), (0.5, 5)], [(0.1, 0.1), (1, 3), (0.5, 5), (0.1, 5)]]
	for n in range(len(coords)):
		plt.gca().add_patch(plt.Polygon(coords[n], color = colorMap[n], edgecolor = colorMap[n], fill = False, hatch = patternsMap[n]))
	plt.show()

def main():
	logo()

if __name__ == "__main__": main()