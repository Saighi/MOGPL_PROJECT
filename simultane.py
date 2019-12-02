from probability import *

def EGsimuL(d1, d2):
    p = 0
    truc = 0

    ptable = p_table(max(d1, d2))

    for i1 in range(1, ptable.shape[1]):
        for i2 in range(1, ptable.shape[1]):
            truc += (ptable[d2, i2] / (max(d1, d2) * 6))
            if i2 < i1 and d1 != 0:
                p += (ptable[d1, i1] / (max(d1, d2) * 6))
            elif i2 > i1 and d2 != 0:
                p -= (ptable[d2, i2] / (max(d1, d2) * 6))

    print(truc)

    return p if abs(p) > 0.01 else 0


def EGmatL(D):
    mat = np.zeros((D + 1, D + 1))

    for d1 in range(D + 1):
        for d2 in range(D + 1):
            mat[d1, d2] = EGsimuL(d1, d2)

    return mat

#Matrice_Louis= EGmatL(3)

def EGsimuP(d1, d2 , D):
    p_table_j1 = p_table(D)[d1]
    p_table_j2 = p_table(D)[d2]
    eg_j1=0
    for i in range(1, len(p_table_j1)):
        eg2=0
        for j in range(1, len(p_table_j2)):
            if i>j:
                eg2 += p_table_j2[j]
            if j>i:
                eg2 -= p_table_j2[j]

        eg_j1 += p_table_j1[i]*eg2

    return eg_j1


def EGmatP(D):
    mat = np.zeros((D + 1, D + 1))

    for d1 in range(D + 1):
        for d2 in range(D + 1):
            mat[d1, d2] = EGsimuP(d1, d2, D)

    return mat

matrice_Paul = EGmatP(3)