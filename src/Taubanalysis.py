__author__ = 'cheng'
from collections import defaultdict
def taob(annoA, annoB):
    if len(annoA) ==0 or len(annoB) ==0:
        return -1.0
    nc = 0
    nd = 0
    r0 = 0
    r0_ = 0
    if len(annoA) != len(annoB):
        print 'inconsistent length',len(annoA),len(annoB)
        return -99.0
    for i in range(0,len(annoA),1):
        if (annoA[i] == 0 and annoB[i] == 0) or (annoA[i]*annoB[i] >0):
            nc +=1
        else:
            nd +=1
        if annoA[i] == 0:
            r0 +=1
        if annoB[i] == 0:
            r0_ +=1
    return float(nc-nd)/(float((nc+nd+r0)*(nc+nd+r0_)))**0.5
def subanalysis(p,d,n,r):
    print 'call subanalysis',len(p)
    subseq = defaultdict(lambda:defaultdict(lambda:list()))
    for i in range(0,len(p),1):
        segment = abs(int(p[i]/3.0))
        print i,segment

        subseq[segment]['preference'].append(p[i])
        subseq[segment]['dsharp'].append(d[i])
        subseq[segment]['ndcg'].append(n[i])
        subseq[segment]['irecall'].append(r[i])

    result = defaultdict(lambda:defaultdict(lambda:''))
    print subseq[3]['preference']
    print subseq[3]['dsharp']
    for r in subseq.keys():
        for m in ['dsharp','ndcg','irecall']:
            result[m][r] = taob(subseq[r]['preference'],subseq[r][m])
    return result

metric = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:-99.0))))

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
def mean(lt):
    sum = 0.0
    for item in lt:
        sum += item
    return sum/float(len(lt))
import  os
fout = open('../result/tau_b_raw.csv','w')
large = open('../result/tau_b_large.csv','w')
small = open('../result/tau_b_small.csv','w')
for annotype in ['fine','coarse']:
    dsharpndcgat20 = list()
    ndcgat20 = list()
    irecallat20 = list()
    preference = list()
    for f in os.listdir('../data/pairnew'):
        run1,run2 = f.strip().replace('.csv','').split('vs')
        count = 0
        for l in open('../data/pairnew/'+f).readlines()[1:]:
            count+=1
            if count>32:
                break
            segs = l.strip().split(',')
            if segs[3] =='S':
                pref = sum([float(segs[0]),float(segs[1]),float(segs[2])])
                preference.append(pref)
                dsharpndcgat20.append(metric[annotype][run1][count]['D#nDCGat20'] - metric[annotype][run2][count]['D#nDCGat20'])
                ndcgat20.append(metric[annotype][run1][count]['nDCGat20'] - metric[annotype][run2][count]['nDCGat20'])
                irecallat20.append(metric[annotype][run1][count]['I-recat20'] - metric[annotype][run2][count]['I-recat20'])
    # fout = open('../temp/'+annotype+'.csv','w')
    # for i in range(0,len(preference),1):
    #     fout.write(','.join([str(preference[i]),str(dsharpndcgat20[i]),str(ndcgat20[i])])+'\n')
    print annotype,taob(preference,dsharpndcgat20),taob(preference,ndcgat20),taob(preference,irecallat20)
    print len(preference)



    r = subanalysis(preference,dsharpndcgat20,ndcgat20,irecallat20)
    fout.write(annotype+',raw\n')
    fout.write(','.join(['','0~1','1~2','2~3','3~4','4~5'])+'\n')
    fout.write('D#nDCG@20,'+','.join(str(item) for item in [r['dsharp'][0],r['dsharp'][1],r['dsharp'][2],r['dsharp'][3],r['dsharp'][4]])+'\n')
    fout.write('nDCG@20,'+','.join(str(item) for item in [r['ndcg'][0],r['ndcg'][1],r['ndcg'][2],r['ndcg'][3],r['ndcg'][4]])+'\n')
    fout.write('I-rec@20,'+','.join(str(item) for item in [r['irecall'][0],r['irecall'][1],r['irecall'][2],r['irecall'][3],r['irecall'][4]])+'\n')
    fout.write('\n')
    fout.write('\n')

    large.write(annotype+',large\n')
    large.write(','.join(['','0~1','1~2','2~3','3~4','4~5'])+'\n')
    small.write(annotype+',small\n')
    small.write(','.join(['','0~1','1~2','2~3','3~4','4~5'])+'\n')




#########################################################################################
    m_mid = mean([abs(item) for item in dsharpndcgat20])
    p_temp = list()
    m_list = list()

    subseq = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:list())))
    for i in range(0,len(preference),1):
        if abs(dsharpndcgat20[i]) >= m_mid:
            segment = abs(int(preference[i]/3.0))
            subseq['large'][segment]['p'].append(preference[i])
            subseq['large'][segment]['m'].append(dsharpndcgat20[i])
        else:
            segment = abs(int(preference[i]/3.0))
            subseq['small'][segment]['p'].append(preference[i])
            subseq['small'][segment]['m'].append(dsharpndcgat20[i])
    large.write('D#nDCG@20')
    for dice in range(0,5,1):
        large.write(','+str(taob(subseq['large'][dice]['p'],subseq['large'][dice]['m'])))
    large.write('\n')

    small.write('D#nDCG@20')
    for dice in range(0,5,1):
        small.write(','+str(taob(subseq['small'][dice]['p'],subseq['small'][dice]['m'])))
    small.write('\n')

#########################################################################################
    m_mid = mean([abs(item) for item in ndcgat20])
    p_temp = list()
    m_list = list()

    subseq = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:list())))
    for i in range(0,len(preference),1):
        if abs(ndcgat20[i]) >= m_mid:
            segment = abs(int(preference[i]/3.0))
            subseq['large'][segment]['p'].append(preference[i])
            subseq['large'][segment]['m'].append(ndcgat20[i])
        else:
            segment = abs(int(preference[i]/3.0))
            subseq['small'][segment]['p'].append(preference[i])
            subseq['small'][segment]['m'].append(ndcgat20[i])
    large.write('nDCG@20')
    for dice in range(0,5,1):
        large.write(','+str(taob(subseq['large'][dice]['p'],subseq['large'][dice]['m'])))
    large.write('\n')

    small.write('nDCG@20')
    for dice in range(0,5,1):
        small.write(','+str(taob(subseq['small'][dice]['p'],subseq['small'][dice]['m'])))
    small.write('\n')

#########################################################################################
    m_mid = mean([abs(item) for item in irecallat20])
    p_temp = list()
    m_list = list()

    subseq = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:list())))
    for i in range(0,len(preference),1):
        if abs(dsharpndcgat20[i]) >= m_mid:
            segment = abs(int(preference[i]/3.0))
            subseq['large'][segment]['p'].append(preference[i])
            subseq['large'][segment]['m'].append(irecallat20[i])
        else:
            segment = abs(int(preference[i]/3.0))
            subseq['small'][segment]['p'].append(preference[i])
            subseq['small'][segment]['m'].append(irecallat20[i])
    large.write('I-rec@20')
    for dice in range(0,5,1):
        large.write(','+str(taob(subseq['large'][dice]['p'],subseq['large'][dice]['m'])))
    large.write('\n')

    small.write('I-rec@20')
    for dice in range(0,5,1):
        small.write(','+str(taob(subseq['small'][dice]['p'],subseq['small'][dice]['m'])))
    small.write('\n')