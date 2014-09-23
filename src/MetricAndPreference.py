__author__ = 'Cheng'

from collections import defaultdict
from Statis import cate3kappa

def direction(n):
    if n>0:
        return 1
    if n==0:
        return 0
    if n<0:
        return -1

import os

run2id2finedsharp = defaultdict(lambda:defaultdict(lambda:0))
run2id2coarsedsharp = defaultdict(lambda:defaultdict(lambda:0))
run2finedsharp = dict()
run2coarsedsharp=dict()
id2query =dict()
id2type = dict()
for l in open('../data/queries.txt'):
    segs = l.strip().split(' ')
    id = int(segs[0])
    query = segs[1]
    type = segs[2]
    id2query[id] = query
    id2type[id]=type
for l in open('../data/run2evaluation.txt').readlines()[1:]:
    segs = l.strip().split(' ')
    runname = segs[0]
    coarse = float(segs[1])
    fine = float(segs[2])
    run2finedsharp[runname] = fine
    run2coarsedsharp[runname] = coarse

for l in open('../data/cn.coarse.pertopic.csv').readlines()[1:]:
    segs = l.strip().split(',')
    runname = segs[0]
    queryid = int(segs[1])
    dsharp = float(segs[3])

    run2id2coarsedsharp[runname][queryid] = dsharp
for l in open('../data/cn.fine.pertopic.csv').readlines()[1:]:
    segs = l.strip().split(',')
    runname = segs[0]
    queryid = int(segs[1])
    dsharp = float(segs[3])

    run2id2finedsharp[runname][queryid] = dsharp

detail = open('../data/reverse_detailed.csv','w')
fout = open('../data/metric_preference.csv','w')
for f in os.listdir('../data/pair'):
    left,right = f.strip().split('vs')
    lines = open('../data/pair/'+f).readlines()
    annotators = lines[0].strip().split(',')
    queryid = 0
    anno0 = list()
    anno1 = list()
    anno2 = list()
    annocoarse = list()
    annofine = list()
    fine_insist = 0
    fine_reverse = 0
    coarse_insist = 0
    coarse_reverse = 0
    allpreference = 0
    print left,right
    coarsetypefail = defaultdict(lambda:0)
    finetypefail = defaultdict(lambda:0)
    coarsefailqueries = list()
    finefailqueries = list()
    for l in lines[2:]:
        segs = l.strip().split(',')
        queryid+=1

        if segs[3] == 'S' and queryid<33:
            a1 = int(segs[0])
            a2 = int(segs[1])
            a3 = int(segs[2])

            anno0.append(int(segs[0]))
            anno1.append(int(segs[1]))
            anno2.append(int(segs[2]))
            diff = run2id2coarsedsharp[left][queryid] -run2id2coarsedsharp[right][queryid]
            if diff>0:
                annocoarse.append(1.0)
            if diff==0:
                annocoarse.append(0.0)
            if diff<0:
                annocoarse.append(-1.0)

            diff = run2id2finedsharp[left][queryid] -run2id2finedsharp[right][queryid]
            if diff>0:
                annofine.append(1.0)
            if diff==0:
                annofine.append(0.0)
            if diff<0:
                annofine.append(-1.0)

            sortedlist = sorted([a1,a2,a3])
            overall = a1+a2+a3
            if overall*(run2id2coarsedsharp[left][queryid] - run2id2coarsedsharp[right][queryid])>0:
                coarse_insist +=1
            else:
                detail.write(','.join([str(queryid),'coarse',left,right,id2query[queryid],str(a1),str(a2),str(a3),str(run2id2coarsedsharp[left][queryid]),str(run2id2coarsedsharp[right][queryid])])+'\n')
                print queryid,'coarse reverse',left,right,overall,a1,a2,a3,run2id2coarsedsharp[left][queryid],run2id2coarsedsharp[right][queryid]
                coarse_reverse+=1
                tp = id2type[queryid]
                query = id2query[queryid]
                coarsetypefail[tp]+=1
                coarsefailqueries.append(query)

            if overall*(run2id2finedsharp[left][queryid] - run2id2finedsharp[right][queryid])>0:
                fine_insist +=1
            else:
                detail.write(','.join([str(queryid),'fine',left,right,id2query[queryid],str(a1),str(a2),str(a3),str(run2id2finedsharp[left][queryid]),str(run2id2finedsharp[right][queryid])])+'\n')
                fine_reverse+=1
                tp = id2type[queryid]
                query = id2query[queryid]
                finetypefail[tp]+=1
                finefailqueries.append(query)


            allpreference += overall
    fout.write(left+'&'+right+'\n')
    fout.write('Coarse_insist:,'+str(coarse_insist)+'\n')
    fout.write('Coarse_reverse:,'+str(coarse_reverse)+'\n')
    fout.write('Fine_insist:,'+str(fine_insist)+'\n')
    fout.write('Fine_reverse:'+str(fine_reverse)+'\n')
    if (run2coarsedsharp[left] - run2coarsedsharp[right])*allpreference >0:
        fout.write('Coarse Insist:,True\n')
    else:
        fout.write('Coarse Insist:,False\n')

    if (run2finedsharp[left] - run2finedsharp[right])*allpreference >0:
        fout.write('Fine Insist:,True\n')
    else:
        fout.write('Fine Insist:,False\n')
    fout.write(left+','+'D#nDCG@Coarse,'+str(run2coarsedsharp[left])+',D#nDCG@Fine,'+str(run2finedsharp[left])+',AvgUserPreference,'+str(allpreference/32.0)+'\n')
    fout.write(right+','+'D#nDCG@Coarse,'+str(run2coarsedsharp[right])+',D#nDCG@Fine,'+str(run2finedsharp[right])+',AvgUserPreference,'+str(allpreference/32.0)+'\n')
    fout.write('Fail Stats:\n')
    fout.write('Coarse Reverse Queries:'+','.join(coarsefailqueries)+'\n')
    fout.write('Fine Reverse Queries:'+','.join(coarsefailqueries)+'\n')
    fout.write('Coarse Reverse Type:')
    for k in coarsetypefail:
        fout.write(k+','+str(coarsetypefail[k])+',')
    fout.write('\n')

    fout.write('Fine Reverse Type:')
    for k in finetypefail:
        fout.write(k+','+str(finetypefail[k])+',')
    fout.write('Coarse Kappa:,'+','.join(annotators)+','+','.join([str(cate3kappa(annocoarse,anno0)),str(cate3kappa(annocoarse,anno1)),str(cate3kappa(annocoarse,anno2))])+'\n')
    fout.write('Fine Kappa:,'+','.join(annotators)+','+','.join([str(cate3kappa(annofine,anno0)),str(cate3kappa(annofine,anno1)),str(cate3kappa(annofine,anno2))])+'\n')

    fout.write('\n')




    fout.write('\n')
fout.close()
detail.close()
