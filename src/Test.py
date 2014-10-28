__author__ = 'luocheng'
from TieAnalyis import kappa

list1 = ['NEG','NEG','MID','MID','NEG','NEG','NEG','MID','POS','POS','POS','NEG']
list2 = ['NEG','MID','NEG','MID','NEG','NEG','NEG','NEG','POS','POS','MID','POS']


list1 = ['NEG','NEG','MID','MID','NEG','NEG','NEG','MID','POS','POS','POS','NEG']
list2 = ['NEG','MID','NEG','MID','NEG','NEG','NEG','NEG','POS','POS','MID','POS']
print kappa(list1,list2)


import numpy as np
import pylab as pl
import matplotlib.pyplot as plt


x = [1, 2, 3, 4, 5]# Make an array of x values
y = [1, 4, 9, 16, 25]# Make an array of y values for each x value
labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
legend = plt.legend(labels, loc=(0.0, .0), labelspacing=0.1)

pl.plot(x, y,'r')# use pylab to plot x and y
pl.show()# show the plot on the screen