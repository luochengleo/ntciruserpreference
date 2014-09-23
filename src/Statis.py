__author__ = 'cheng'


from collections import defaultdict
def cate3kappa(annoA, annoB):
    length = -1.0
    if len(annoA)!= len(annoB):
        print 'different length error'
        return -1.0
    else:
        length = float(len(annoA))
    matrix = defaultdict(lambda:0)
    key1 = ''
    key2 = ''
    for i in range(0,int(length),1):
        if annoA[i]<0:
            key1 = 'NEG'
        if annoA[i]>0:
            key1 = 'POS'
        if annoA[i]==0:
            key1 = 'MID'
        if annoB[i]<0:
            key2 = 'NEG'
        if annoB[i]>0:
            key2 = 'POS'
        if annoB[i]==0:
            key2 = 'MID'

        matrix[(key1,key2)]+=1.0
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


