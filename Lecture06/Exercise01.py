__author__ = 'nnyegaard'

from numpy import *

# E1)
# Apply matrix multiplication to a small example (similar to Figure 10-2) that you create yourself.
# Transpose the result. Show that (AB)^T = B^T A^T holds for your example.

m1 = matrix([[7, 8, 1], [3, 5, 1]])
m2 = matrix([[9, 2], [7, 4], [1, 6]])
m1t = m1.transpose()
m2t = m2.transpose()
m1m2 = m1 * m2


print "Matrix 1: "
print m1
print
print "Matrix 2: "
print m2
print
print "Matrix 1 * Matrix 2: "
print m1m2
print
print "Transposing matrix 1 * matrix 2:"
print (m1 * m2).transpose()
print

print "Showing that (AB)^T = B^T A^T"
print m2t * m1t


# E2)
# Explain what happens in Figure 10-6. Explain what a feature is.
#
# Figure 10-6 contains an error and the 2 matrixes can't be multiplied. But it tries to show how you can combine the
# weight matrix with the features matrix to give ....
# A feature is a row of words, that contains the count for the appearance of the given word.