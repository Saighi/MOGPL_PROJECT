import numpy as np


def q(d, k):
    if k < 2 * d or k > 6 * d:
        return 0

    if d == 1:
        return 1 / 5

    sum_probability = 0

    for i in range(2, 6):
        sum_probability += q(d - 1, k - i) / 5

    return sum_probability


def p(d, k):
    if k == 1:
        return 1 - (5 / 6) ** d
    if (2 * d <= k <= 2 * d - 1) or k > 6 * d:
        return 0
    return ((5 / 6) ** d) * q(d, k)


def p_table(D):
    table = np.zeros((D+1, 6 * D+1))
    for d in range(1, D+1):
        for k in range(1, 6 * D):
            table[d, k] = p(d, k)
    np.savetxt('test.out', table, delimiter=',')
    return table


def max_esp(D):
    val_max_d = 0
    for d in range(1, D+1):
        if 4 * d * (5 / 6) ** d + 1 - (5 / 6) ** d > val_max_d:
            max_d = d
            val_max_d = 4 * d * (5 / 6) ** d + 1 - (5 / 6) ** d

    return max_d

def egLouis(M,D):
    d = max_esp(D)
    k = 4 * d * (5 / 6) ** d + 1 - (5 / 6) ** d
    pTable = p_table(D)[d-1]


    egTab = np.zeros((M+1,M+1))

    for i in range(M,0,-1):
        for j in range(M,0,-1):
            if i==M:
                egTab[i,j]=1
            elif j == M:
                egTab[i,j]=-1
            else :
                egTab[i,j] = egTab[i+1,j]-pTable[M-i]-egTab[i,j+1]+pTable[M-j]

    return egTab

def egPaul(M,D):
    d = max_esp(D)
    k = 4 * d * (5 / 6) ** d + 1 - (5 / 6) ** d
    p_Table = p_table(D)[d]

    # initialisation
    EG_table= np.zeros((M+1, M+1))
    EG_table[:,M]= np.full(M+1,1)
    EG_table[M, :] = np.full(M + 1, -1)
    EG_table[M, M]=0

    for i in range(M-1,-1,-1):
        for j in range(M - 1, -1, -1):
            if M-i<len(p_Table):
                proba_k=np.sum(p_Table[M-i:])
            else:
                proba_k=0

            EG_table[j, i] = proba_k-(proba_k*(1-proba_k))+EG_table[j, i+1]+EG_table[j+1, i]
            if EG_table[j, i]>1:
                EG_table[j, i]=1
            if EG_table[j, i] < -1:
                EG_table[j, i] = -1


    return EG_table



EG_table=egPaul(100,10)