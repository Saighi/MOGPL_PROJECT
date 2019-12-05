from probability import *
import pandas as pd

def EGsimuL(d1, d2,ptable):
    p = 0

    if max(d1,d2) == 0:
        return 0

    p += np.sum(ptable[d1, d2*6:])

    p -= np.sum(ptable[d2, d1*6:])

    return p if abs(p) > 0.01 else 0


def EGmatL(D):
    mat = np.zeros((D + 1, D + 1))
    ptable = p_table(D)
    for d1 in range(D + 1):
        for d2 in range(D + 1):
            mat[d1, d2] = EGsimuL(d1, d2,ptable)

    return mat[1:,1:]

#Matrice_Louis= EGmatL(10)

def EGsimuP(d1, d2 , pt):
    p_table_j1 = pt[d1]
    p_table_j2 = pt[d2]
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
    pt = p_table(D)

    for d1 in range(D + 1):
        for d2 in range(D + 1):
            mat[d1, d2] = EGsimuP(d1, d2, pt)

    return mat[1:, 1:]

#matrice_Paul = EGmatP(3)



"""def matrice_des_gains(D):
    mat_gain=np.zeros(((6*D)+1,(6*D)+1))
    for i in range(1,(6*D)+1):
        for j in range(1, (6 * D)+1):
            if i>j:
                mat_gain[i, j]=1
            if i==j:
                mat_gain[i, j]=0
            if i<j:
                mat_gain[i, j]=-1
    return mat_gain[1:,1:]

mat_gain = matrice_des_gains(3)"""
