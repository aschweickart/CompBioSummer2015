import os
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pylab

def readDataFromDir(directory, ext):
    ''' Given a
        directory - path to a directory containing random data in
                    *.newick.random.out files
        returns a map from file name prefix (the *) to a [TestData]
    '''
    map_ = {}
    for filename in os.listdir(directory):
        index = filename.rindex(ext)
        if index >= 0:
            file_prefix = filename[:index]
            full_file_path = directory + '/' + filename
            map_[file_prefix] = readRandomDataFromFile(full_file_path)
    return map_

def readRandomDataFromFile(filePath):
    ''' Given a
        directory - path to a directory containing random data in
                    *.newick.random.out files
        returns a [TestData]
    '''
    f = open(filePath)

    # This will hold the tests we return
    list_of_tests = []

    # These are temporary for assembly the TestData objects
    k = None
    averages = []
    maxes = []
    for line in f.xreadlines():
        line = line.strip()
        if 'seed = ' in line or 'k = ' in line:
            if len(averages) > 0:
                list_of_tests.append(TestData(k, averages, maxes))
            averages = []
            maxes = []
        if 'seed = ' in line:
            pass
        elif 'k = ' in line:
            k = int(line.split()[2])
        else:
            averages.append(float(line.split()[0]))
            maxes.append(float(line.split()[1]))
    if len(averages) > 0:
        list_of_tests.append(TestData(k, averages, maxes))
    f.close()
    return list_of_tests

class TestData(object):
    ''' Holds the results from a test.
    Namely the k-value, and a list of average and maximum distances
    before start and after each iteration till stability is reached.'''
    def __init__(self,
                 k,
                 averages,
                 maxes):
        self.k = k
        self.averages = averages
        self.maxes = maxes
    def start_ave(self):
        return self.averages[0]
    def end_ave(self):
        return self.averages[-1]
    def start_max(self):
        return self.maxes[0]
    def end_max(self):
        return self.maxes[-1]
    def percent_change_ave(self):
        return (self.end_ave() - self.start_ave()) / self.start_ave()
    def percent_change_max(self):
        return (self.end_max() - self.start_max()) / self.start_max()

rdata = readDataFromDir('rand-data','.newick.random.out')
data = readDataFromDir('data','.newick.out')

# This maps data set name to:
# k -> [%(random_end - random_start),
#  %(points_start - random_start),
#  %(points_end - random_start)]
data_set_to_values = {}

max_k = max(max(test.k for test in rdata[fileName]) for fileName in rdata)

def percent_change(start, end):
    return (end - start) / start

def mean(xs):
    return sum(xs) / float(len(xs))

def transpose(M):
    return [[M[j][i] for j in xrange(len(M))] for i in xrange(len(M[0]))]

for fileName in rdata:
    rtests = rdata[fileName]
    tests = data[fileName]
    k_to_values= {}
    for k in xrange(1, max_k + 1):
        random_start = mean([test.start_ave() for test in rtests if test.k == k])
        random_end = mean([test.end_ave() for test in rtests if test.k == k])
        points_start = [test.start_ave() for test in tests if test.k == k][0]
        points_end = [test.end_ave() for test in tests if test.k == k][0]
        k_to_values[k] = [percent_change(random_start, random_end),
                          percent_change(random_start, points_start),
                          percent_change(random_start, points_end)]
    data_set_to_values[fileName] = k_to_values

def plot3d(data_set_to_values):
    ks = data_set_to_values.values()[0].keys()

    k_means_change = []
    point_change = []
    both_change = []
    i_s = []
    for i, fileName in enumerate(data_set_to_values.keys()):
        i_s.append([i for k in ks])
        k_means_change.append([data_set_to_values[fileName][k][0] * 100 for k in ks])
        point_change.append([data_set_to_values[fileName][k][1] * 100 for k in ks])
        both_change.append([data_set_to_values[fileName][k][2] * 100 for k in ks])


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in xrange(len(i_s)):
        ax.plot(ks, i_s[i],  k_means_change[i], c='r', label='K Means')
        ax.plot(ks, i_s[i], point_change[i], c='g', label='Point Collect')
        ax.plot(ks, i_s[i], both_change[i], c='b', label='Both')
    ax.legend()
    ax.set_xlabel('k')
    ax.set_ylabel('Data Set ID#')
    ax.set_zlabel('% Change in Average Distance relative to Random Representatives')
    plt.title('Percent improvement over random clusters')
    fig.show()
    raw_input()


def plot2d(data_set_to_values):
    ks = data_set_to_values.values()[0].keys()

    k_means_change = []
    point_change = []
    both_change = []
    for fileName in data_set_to_values:
        k_means_change.append([data_set_to_values[fileName][k][0] * 100 for k in ks])
        point_change.append([data_set_to_values[fileName][k][1] * 100 for k in ks])
        both_change.append([data_set_to_values[fileName][k][2] * 100 for k in ks])


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ks, map(mean, transpose(k_means_change)), c='r', label='K Means')
    ax.plot(ks, map(mean, transpose(point_change)), c='g', label='Point Collect')
    ax.plot(ks, map(mean, transpose(both_change)), c='b', label='Both')
    ax.legend()
    ax.set_xlabel('k')
    ax.set_ylabel('% Change in Average Distance relative to Random Representatives')
    plt.title('Percent improvement over random clusters')
    fig.show()
    raw_input()

plot2d(data_set_to_values)
