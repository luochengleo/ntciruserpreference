import os
from Statis import cate3kappa
fout = open('../data/kapparesult.csv','w')
for f in os.listdir('../data/pair'):
    left,right = f.strip().split('vs')
    lines = open('../data/pair/'+f).readlines()
    annotators = lines[0].strip().split(',')