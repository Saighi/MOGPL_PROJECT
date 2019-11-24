import numpy as np


def q(d, k):
    if k < 2 * d or k > 6 * d:
        return 0

    if d == 1:
        return 1 / 5

    sum_probability = 0

    for i in range(2, 6+1):
        sum_probability += q(d - 1, k - i) / 5

    return sum_probability


def p(d, k):
    if k == 1:
        return 1 - (5 / 6) ** d
    elif k < 2 * d or k > 6 * d:
        return 0
    else:
        return ((5 / 6) ** d) * q(d, k)


def p_table(D):
    table = np.zeros((D+1, 6 * D+1))
    for d in range(1, D+1):
        for k in range(1, 6 * D+1):
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

def egLouisinverse(M,D):
    d = max_esp(D)
    pTable = np.sum(p_table(D),axis=0)/D
    pTable = np.concatenate((pTable,np.zeros(M+1-pTable.shape[0])))
    print(pTable)

    egTab = np.zeros((M,M))

    for i in range(M-1,-1,-1):
        for j in range(M-1,-1,-1):
            if i == M-1:
                pi = 1
            else:
                pi = egTab[i+1,j]-pTable[M-i-1]
            egTab[i,j]=pi if pi >0.01 else 0

    for i in range(M-1,-1,-1):
        for j in range(M-1,-1,-1):
            if egTab[i,j] == 0:
                if j == M-1:
                    pj = -1
                else:
                    pj = egTab[i,j+1]+pTable[M-j-1]
                egTab[i,j]=pj if pj <-0.01 else 0

    return egTab

def egLouis(M,D):
    d = max_esp(D)
    pTable = np.sum(p_table(D),axis=0)/D
    pTable = np.concatenate((pTable,np.zeros(M+1-pTable.shape[0])))
    print(pTable)

    egTab = np.zeros((M,M))

    for i in range(M):
        for j in range(M):
            if i == 0:
                pi = pTable[M]
            else:
                pi = egTab[i-1,j]+pTable[M-i]
            egTab[i,j]=pi

    for i in range(M):
        for j in range(M):
            if egTab[i,j] == 0:
                if j == 0:
                    pj = -pTable[M]
                else:
                    pj = egTab[i,j-1]-pTable[M-j]
                egTab[i,j]=pj

    return egTab


"""
df = pd.DataFrame(egLouisinverse(20,2))
f= open("eg.html","w")
f.write(df.to_html())

df = pd.DataFrame(egLouis(20,2))
f= open("eg00.html","w")
f.write(df.to_html())
"""


def egPaul(M, D):
    d = max_esp(D)
    # initialisation
    EG_table = np.zeros((M + 1, M + 1))
    EG_table[:, M] = np.full(M + 1, 1)
    EG_table[:, M - 1] = np.full(M + 1, 1)
    EG_table[M, :] = np.full(M + 1, -1)
    EG_table[M, M] = 0

    for i in range(M - 2, -1, -1):
        for j in range(M - 1, -1, -1):
            EG_table[j, i] = EG_table[j, i + 1] - p(d, 1) + (p(d, 1) * EG_table[j + 1, i] + (p(d, 1) ** 2))

    return EG_table


EG_table = egPaul(10, 1)
