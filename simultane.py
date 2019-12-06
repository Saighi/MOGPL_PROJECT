from probability import *
import pandas as pd

def EGsimu(d1, d2,ptable):
    p = 0

    if max(d1,d2) == 0:
        return 0

    h,w = ptable.shape

    for i in range(1,w):

        p += ptable[d1,i]*np.sum(ptable[d2,:i])

        p -= ptable[d1,i]*np.sum(ptable[d2,i+1:])

    return p if abs(p) > 0.01 else 0


def EGmat(D):
    mat = np.zeros((D + 1, D + 1))
    ptable = p_table(D)
    for d1 in range(D + 1):
        for d2 in range(D + 1):
            mat[d1, d2] = EGsimu(d1, d2,ptable)

    return mat[1:,1:]
