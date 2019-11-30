import numpy as np


def q(d, k):
    if k < 2 * d or k > 6 * d:
        return 0

    if d == 1:
        return 1 / 5

    sum_probability = 0

    for i in range(2, 6 + 1):
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
    table = np.zeros((D + 1, 6 * D + 1))
    for d in range(1, D + 1):
        for k in range(1, 6 * D + 1):
            table[d, k] = p(d, k)
    np.savetxt('test.out', table, delimiter=',')
    return table


def max_esp(D):
    val_max_d = 0
    for d in range(1, D + 1):
        if 4 * d * (5 / 6) ** d + 1 - (5 / 6) ** d > val_max_d:
            max_d = d
            val_max_d = 4 * d * (5 / 6) ** d + 1 - (5 / 6) ** d

    return max_d


"""
df = pd.DataFrame(p_table(3))
f= open("eg.html","w")
f.write(df.to_html())
"""


def esp(a):
    return 4 * a * (5 / 6) ** a + 1 - (5 / 6) ** a


D = 10
proba_table = p_table(D)[1:, :]
M = 100
Eg_table = np.full((M, M), 1000.)
Eg_table_which_play = np.full((M, M), 1000.)
Eg_table_which_play_j2 = np.full((M, M), 1000.)


def egPaul(i, j, j1):
    global D
    global M
    global Eg_table

    if i >= M:
        return 1
    if j >= M:
        return -1

    Eij_potentiels = np.zeros(len(proba_table))

    if j1:

        for k in range(len(proba_table)):

            for x in range(1, len(proba_table[k])):

                if proba_table[k][x] != 0.:

                    if (i + x < M) and Eg_table[i + x, j] != 1000.:
                        Eij_potentiels[k] += proba_table[k][x] * Eg_table[i + x, j]
                    else:
                        Eij_potentiels[k] += proba_table[k][x] * egPaul(i + x, j, False)

        Egij = np.amax(Eij_potentiels)
        des = np.argmax(Eij_potentiels) + 1
    else:

        for k in range(len(proba_table)):

            for x in range(1, len(proba_table[k])):

                if proba_table[k][x] != 0.:

                    if (j + x < M) and Eg_table[i, j + x] != 1000.:
                        Eij_potentiels[k] += proba_table[k][x] * Eg_table[i, j + x]
                    else:
                        Eij_potentiels[k] += proba_table[k][x] * egPaul(i, j + x, True)

        Egij = np.amin(Eij_potentiels)
        des = np.argmin(Eij_potentiels) + 1

    if Eg_table_which_play[i, j] == 1000.:
        if j1:
            Eg_table_which_play[i, j] = des
        else:
            Eg_table_which_play_j2[i, j] = des

    if Eg_table[i, j] == 1000.:
        Eg_table[i, j] = Egij

    return Egij


EG = egPaul(96, 96, True)


# Partie simultanée

def EGsimu(d1, d2):
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


def EGmat(D):
    mat = np.zeros((D + 1, D + 1))

    for d1 in range(D + 1):
        for d2 in range(D + 1):
            mat[d1, d2] = EGsimu(d1, d2)

    return mat

# print(EGmat(3))
