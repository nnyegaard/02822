__author__ = 'nnyegaard'

from matplotlib.pyplot import plot


with open("alcohol.txt", "r") as f:
    data = f.readlines()

pdata = []

for e in data:
    pdata.append(e.rstrip("\n").split("|"))

