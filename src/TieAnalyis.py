__author__ = 'cheng'

from collections import defaultdict
import os

def kappa( annoA, annoB):
    if len(annoA) != len(annoB):
        print 'inconsist length'
        return -999.0
    length  = len(annoA)
    matrix = defaultdict(lambda:0)
    for i in range(0,length,1):
        matrix[(annoA[i],annoB[i])] +=1.0

    pa = (matrix[('POS','POS')]+matrix[('NEG','NEG')]+matrix[('MID','MID')])/length
    pe = 0.0
    for curr in ['NEG','MID','POS']:
        pre = 0.0
        fwd = 0.0
        for k in matrix.keys():
            if k[0] == curr:
                pre += matrix[k]
            if k[1] == curr:
                fwd += matrix[k]
        pe += pre/length * fwd/length
    return (pa-pe)/(1-pe)

def tiePercentage(annolist):
    tie = 0
    for item in annolist:
        if item=='MID':
            tie +=1
    return float(tie)/float(len(annolist))

if __name__=='__main__':
    lista = ['NEG','MID','NEG','MID']
    listb = ['NEG','MID','NEG','MID']
    print kappa(lista,listb)

    #  FINE or COARSE/ RUNNAME / TOPICID / MEATRIC
    metric = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0.0))))

    for l in open('../data/cn.fine.pertopic.csv').readlines()[1:]:
        segs = l.strip().split(',')
        runname = segs[0]
        topicid = int(segs[1])

        ndcgat20 = float(segs[2])
        dsharpndcgat20 = float(segs[3])
        irecallat20 = float(segs[4])

        metric['fine'][runname][topicid]['nDCGat20'] = ndcgat20
        metric['fine'][runname][topicid]['D#nDCGat20'] = dsharpndcgat20
        metric['fine'][runname][topicid]['I-recat20'] = irecallat20

    for l in open('../data/cn.coarse.pertopic.csv').readlines()[1:]:
        segs = l.strip().split(',')
        runname = segs[0]
        topicid = int(segs[1])

        ndcgat20 = float(segs[2])
        dsharpndcgat20 = float(segs[3])
        irecallat20 = float(segs[4])

        metric['coarse'][runname][topicid]['nDCGat20'] = ndcgat20
        metric['coarse'][runname][topicid]['D#nDCGat20'] = dsharpndcgat20
        metric['coarse'][runname][topicid]['I-recat20'] = irecallat20
    fout = open('../result/tieanalysis.csv','w')
    for mtype in ['fine','coarse']:
        for pref in ['weak','strong']:
            for met in ['nDCGat20','D#nDCGat20','I-recat20']:
                for tie in range(0,101,1):
                    tie = float(tie)/100.0
                    print 'TIE',tie
                    for f in os.listdir('../data/pairnew/'):
                        annoPref = list()
                        annoMetric = list()
                        run1,run2 = f.strip().replace('.csv','').split('vs')
                        preference = open('../data/pairnew/'+f).readlines()[1:33]
                        tcount = 0
                        for l in preference:
                            tcount +=1
                            segs = l.strip().split(',')
                            plist = [int(segs[0]),int(segs[1]),int(segs[2])]
                            pflag = segs[3]
                            #pflag means if the preference is valid
                            if pflag =='S':
                                p = ''
                                if pref =='weak':
                                    if sum(plist)>0:
                                        p = 'POS'
                                    if sum(plist)==0:
                                        p ='MID'
                                    if sum(plist)<0:
                                        p='NEG'
                                if pref =='strong':
                                    s = 0
                                    for item in plist:
                                        if item <=1 and item >=-1:
                                            s+=0
                                        else:
                                            s += item
                                    if s >0:
                                        p = 'POS'
                                    if s ==0:
                                        p = 'MID'
                                    if s < 0:
                                        p = 'NEG'
                                annoPref.append(p)

                                m1 = metric[mtype][run1][tcount][met]
                                m2 = metric[mtype][run2][tcount][met]
                                # print 'm1 & m2',m1,m2
                                m = ''
                                if abs(m1-m2)<=tie:
                                    m='MID'
                                else:
                                    if m1>m2:
                                        m = 'POS'
                                    if m1<m2:
                                        m = 'NEG'
                                    if m1==m2:
                                        m = 'MID'
                                annoMetric.append(m)
                        # print annoPref
                        # print annoMetric
                        print kappa(annoPref,annoMetric)
                        outputlist = [mtype,pref,met,run1,run2,tie,tiePercentage(annoPref),tiePercentage(annoMetric),kappa(annoPref,annoMetric)]
                        fout.write(','.join([str(item) for item in outputlist])+'\n')
    fout.close()






