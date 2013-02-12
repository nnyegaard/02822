__author__ = 'nnyegaard'

import matplotlib.pyplot as plt
import numpy as np
import operator


with open("alcohol.txt", "r") as f:
    data = f.readlines()

lande = []
alco = []
samlet = {}
sorted_lande = []
sorted_alco = []

#Generate list of countries, alcohol %, and a dic of the 2 types
for x in data:
    lande.append(x.split("|")[0])
    alco.append(float(x.split("|")[1].rstrip("\n")))
    samlet[x.split("|")[0]] = float(x.split("|")[1].rstrip("\n"))


#Sort our dic -- Will turn it into a list of tuples
sorted_x = sorted(samlet.iteritems(), key=operator.itemgetter(1), reverse=True)

for x in sorted_x:
    sorted_lande.append(x[0])
    sorted_alco.append(x[1])


def showData():
    print "Our country list is: %r" % lande
    print "Our list of alcohol: %r" % alco
    print "Our dic of the 2 types: %r" % samlet
    print "Our sorted by alcohol list of tuples: %r" % sorted_x
    print "Our sorted countries: %r" % sorted_lande
    print "Our sorted alcohol: %r" % sorted_alco


def linePlot():
    plt.xticks(np.arange(len(sorted_lande)), sorted_lande, rotation=90)
    plt.plot(sorted_alco)
    plt.show()


def barPlot():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(np.arange(len(alco)), alco, width=10.50, color='r')
    plt.show()


def newBarPlot():
    empty = ["", "M countries", ""]
    fig = plt.figure()
    plt.xticks(np.arange(33), sorted_lande[0:15] + empty + sorted_lande[-16:-1], rotation=80)
    ax = fig.add_subplot(111)
    ax.bar(np.arange(33), sorted_alco[0:15] + [0, 0, 0] + sorted_alco[-16:-1], width=1, color='b')
    plt.show()


if __name__ == '__main__':
    #showData()
    #linePlot()
    newBarPlot()


