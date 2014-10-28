__author__ = 'luocheng'
import os
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

if 'split' not in os.listdir('../data/'):
    os.mkdir('../data/split')
else:
    os.system('rm ../data/split/*.csv')
if 'graph' not in os.listdir('../data/'):
    os.mkdir('../data/graph')
else:
    os.system('rm ../data/graph/*.png')
graphconfig = set()
for l in open('../result/tieanalysis.csv').readlines():
    segs= l.strip().split(',')
    mtype = segs[0]
    ptype = segs[1]
    metric = segs[2]
    run1 = segs[3]
    run2 = segs[4]
    tiepre = segs[7]
    tau  = segs[8]
    fout = open('../data/split/'+mtype+'_'+ptype+'_'+run1+'_'+run2+'_'+metric+'.csv','a')
    graphconfig.add((run1,run2))
    fout.write(','.join([metric,tiepre,tau])+'\n')
    fout.close()
m2color = dict()
m2color['D#nDCGat20'] = 'r'
m2color['nDCGat20'] = 'b'
m2color['I-recat20'] = 'g'

for c in graphconfig:
    run1 = c[0]
    run2 = c[1]
    count = 0
    pl.subplots_adjust( hspace=0.4,wspace = 0.6 )

    for mtype in ['fine','coarse']:
        for ptype in ['weak','strong']:
            count +=1
            plt.subplot(int('32'+str(count)))

            for m in ['D#nDCGat20','nDCGat20','I-recat20']:
                x = list()
                y = list()
                for l in open('../data/split/'+mtype+'_'+ptype+'_'+run1+'_'+run2+'_'+m+'.csv'):
                    segs = l.strip().split(',')
                    x.append(float(segs[1]))
                    y.append(float(segs[2]))
                if count ==0:
                    x_=1
                    y_=1
                if count ==1:
                    x_=2
                    y_=1
                if count ==2:
                    x_=1
                    y_=2
                if count ==3:
                    x_=2
                    y_=2
                pl.plot(x, y,m2color[m]+'.-',label=m.replace('at','@'))# use pylab to plot x and y
                plt.title(mtype+'_'+ptype)
                plt.xlabel('tau')
                plt.ylabel("Cohen's Kappa")

    plt.legend(loc='upper right', bbox_to_anchor=(1.0, -0.5))
    pl.savefig('../data/graph/'+'_'.join([run1,run2]))
    pl.close()