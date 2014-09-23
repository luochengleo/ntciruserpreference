
import os
from Statis import cate3kappa

def direction(n):
    if n>0:
        return 1
    if n==0:
        return 0
    if n<0:
        return -1
fout = open('../data/kapparesult.csv','w')
for f in os.listdir('../data/pair'):
    left,right = f.strip().split('vs')
    lines = open('../data/pair/'+f).readlines()
    annotators = lines[0].strip().split(',')
    queryid = 1
    anno0 = list()
    anno1 = list()
    anno2 = list()
    insist = 0
    for l in lines[2:]:
        segs = l.strip().split(',')
        if segs[3] == 'S':
            a1 = int(segs[0])
            a2 = int(segs[1])
            a3 = int(segs[2])
            if (a1>0 and a2>0 and a3>0) or (a1==0 and a2==0 and a3 == 0) or (a1<0 and a2<0 and a3<0):
                insist +=1

            anno0.append(int(segs[0]))
            anno1.append(int(segs[1]))
            anno2.append(int(segs[2]))
    fout.write('PAIR:'+','+left+','+right+'\n')
    fout.write('INSIST:,'+str(insist)+' out of '+str(len(anno0))+',insist rate,'+str(float(insist)*100.0/float(len(anno0)))+'%\n')
    fout.write("USER:"+','+','.join(annotators)+'\n')
    fout.write("Kappa1:,"+annotators[0]+'&'+annotators[1]+','+str(cate3kappa(anno0,anno1))+'\n')
    fout.write("Kappa2:,"+annotators[0]+'&'+annotators[2]+','+str(cate3kappa(anno0,anno2))+'\n')
    fout.write("Kappa3:,"+annotators[1]+'&'+annotators[2]+','+str(cate3kappa(anno1,anno2))+'\n')
    fout.write("AvgKappa:,"+str(float(cate3kappa(anno0,anno1)+cate3kappa(anno0,anno2)+cate3kappa(anno1,anno2))/3.0)+'\n')
    fout.write("MaxKappa:,"+str(max([cate3kappa(anno0,anno1),cate3kappa(anno0,anno2),cate3kappa(anno1,anno2)]))+'\n')
    fout.write("MinKappa:,"+str(min([cate3kappa(anno0,anno1),cate3kappa(anno0,anno2),cate3kappa(anno1,anno2)]))+'\n')

    fout.write('\n')

