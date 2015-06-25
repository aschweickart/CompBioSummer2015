#logo design
import matplotlib.pyplot as plt
from shapely.geometry import *
from CostVector import *
from commonAnalytic import *


def logo():
	plt.axis([0.1, 5, 0.1, 5])

	numRegions = 6

	colorMap = [(1, 0, 0), (1, 1, 0), (0, 1, 0), (1, 0, 1), (0, 0, 1), (0, 0, 1)]
	patternsMap = ["*", "o", ".", ".|","x|", "///" ]
	plt.gca().add_patch(plt.Polygon([(0.1, 0.1)(2, 1.5),(5, 1), (5, 0.1)], color = colorMap[1], fill = False, hatch = patternsMap[1]))
	plt.show()

def main():
	logo()

if __name__ == "__main__": main()