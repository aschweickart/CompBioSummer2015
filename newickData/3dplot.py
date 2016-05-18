import matplotlib
matplotlib.use("Agg")
import csv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import pylab
import pandas as pd
from scipy.interpolate import griddata

data_avg = [[],[],[]]
data_max = [[],[],[]]
with open('distance3davg.csv', 'rb') as avgfile:
    reader = csv.reader(avgfile)
    for row in reader:
        for i in range(len(row)):
            data_avg[i].append(float(row[i]))
with open('distance3dmax.csv', 'rb') as maxfile:
    reader = csv.reader(maxfile)
    for row in reader:
        for i in range(len(row)):
            data_max[i].append(float(row[i]))

for data, outName in zip([data_avg, data_max], ['avgPlot.png','maxPlot.png']):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel("k")
    ax.set_ylabel("iteration number")
    ax.set_zlabel("% change in aggregate distance")
    ax.set_title("Average distance plot" if 'avg' in outName else "Maximum distance plot")

    x,y,z = data

    x1 = np.linspace(min(x), max(x), 100)
    y1 = np.linspace(min(y), max(y), 100)

    z1 = griddata((x,y), z, (x1[None,:], y1[:,None]), method='cubic')

    xig, yig = np.meshgrid(x1,y1)

    surf = ax.plot_surface(xig, yig, z1, linewidth = 0)

    pylab.savefig(outName)

