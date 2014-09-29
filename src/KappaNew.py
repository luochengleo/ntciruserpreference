#coding=utf8

from os import listdir

from Statis import cate3kappaNew

def direction(n):
    if n>0:
        return 1
    if n==0:
        return 0
    if n<0:
        return -1
fout = open('../data/kapparesultnew.csv','w')
for f in listdir('../data/pair'):
    left,right = f.strip().split('vs')
    lines = open('../data/pair/'+f).readlines()
    annotators = lines[0].strip().split(',')
    queryid = 1
    anno0 = list()
    anno1 = list()
    anno2 = list()
    leftbeats = 0
    rightbeats = 0
    tie = 0
    insist = 0
    var = 0
    max_distance_sum = 0.0
    for l in lines[2:]:
        segs = l.strip().split(',')
        if segs[3] == 'S':
            a1 = int(segs[0])
            a2 = int(segs[1])
            a3 = int(segs[2])
            if a1+a2+a3 >0:
                leftbeats +=1
            if a1+a2+a3 ==0:
                tie +=1
            if a1+a2+a3 <0:
                rightbeats +=1
            if (a1>0 and a2>0 and a3>0) or (a1==0 and a2==0 and a3 == 0) or (a1<0 and a2<0 and a3<0):
                insist +=1
            sortedlist = sorted([a1,a2,a3])
            max_distance_sum += sortedlist[2] - sortedlist[0]

            d1 = direction(a1)
            d2 = direction(a2)
            d3 = direction(a3)
            if d1*d2*d3 == 0 and (d1+d2+d3==0):
                var +=1
            anno0.append(int(segs[0]))
            anno1.append(int(segs[1]))
            anno2.append(int(segs[2]))
    fout.write('PAIR:'+','+left+','+right+'\n')
    fout.write('INSIST:,'+str(insist)+' out of '+str(len(anno0))+',insist rate,'+str(float(insist)*100.0/float(len(anno0)))+'%\n')
    fout.write('Various(any two different):,'+str(var)+' out of '+str(len(anno0))+',various rate,'+str(float(var)*100.0/float(len(anno0)))+'%\n')
    fout.write("USER:"+','+','.join(annotators)+'\n')
    fout.write("Kappa1:,"+annotators[0]+'&'+annotators[1]+','+str(cate3kappaNew(anno0,anno1))+'\n')
    fout.write("Kappa2:,"+annotators[0]+'&'+annotators[2]+','+str(cate3kappaNew(anno0,anno2))+'\n')
    fout.write("Kappa3:,"+annotators[1]+'&'+annotators[2]+','+str(cate3kappaNew(anno1,anno2))+'\n')
    fout.write("AvgKappa:,"+str(float(cate3kappaNew(anno0,anno1)+cate3kappaNew(anno0,anno2)+cate3kappaNew(anno1,anno2))/3.0)+'\n')
    fout.write("MaxKappa:,"+str(max([cate3kappaNew(anno0,anno1),cate3kappaNew(anno0,anno2),cate3kappaNew(anno1,anno2)]))+'\n')
    fout.write("MinKappa:,"+str(min([cate3kappaNew(anno0,anno1),cate3kappaNew(anno0,anno2),cate3kappaNew(anno1,anno2)]))+'\n')
    fout.write("AvgMaxDiameter:," + str(max_distance_sum/float(len(anno0)))+'\n')
    fout.write("Left Wins:,"+str(leftbeats)+'\n')
    fout.write("Right Wins:,"+str(rightbeats)+'\n')
    fout.write("Left Right Tie:,"+str(tie)+'\n')
    fout.write('\n')

