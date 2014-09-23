__author__ = 'cheng'

index = list()
index2filename = dict()

lines = open('../data/NTCIR_annotation_result.csv').readlines()
pairnames = lines[0].strip().split(',')
for i in range(0,len(pairnames),1):
    if pairnames[i] != '':
        index.append(i)

annotators = lines[51].strip().replace('\n','').replace('\r','').split(',')

for idx in index:
    fout = open('../data/pair/'+pairnames[idx].replace(' ','').replace('.',''),'w')
    fout.write(','.join([annotators[idx],annotators[idx+1],annotators[idx+2]])+'\n')
    for l in lines[1:51]:
        annotations = l.split(',')
        fout.write(','.join([annotations[idx],annotations[idx+1],annotations[idx+2],annotations[idx+3]])+'\n')
    fout.close()