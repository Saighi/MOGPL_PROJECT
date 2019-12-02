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


def eg(D, M, i, j, j1):
    proba_table = p_table(D)[1:, :]
    Eg_table_j1 = np.full((M, M), 1000.)
    Eg_table_j2 = np.full((M, M), 1000.)
    Eg_table_which_play_j1 = np.full((M, M), 1000.)
    Eg_table_which_play_j2 = np.full((M, M), 1000.)

    def egPaul(i, j, j1):

        if i >= M:
            return 1
        if j >= M:
            return -1

        Eij_potentiels = np.zeros(len(proba_table))

        if j1:

            for k in range(len(proba_table)):

                for x in range(1, len(proba_table[k])):
                    if proba_table[k][x] != 0.:

                        if (i + x < M) and Eg_table_j2[i + x, j] != 1000.:
                            Eij_potentiels[k] += proba_table[k][x] * Eg_table_j2[i + x, j]
                        else:
                            Eij_potentiels[k] += proba_table[k][x] * egPaul(i + x, j, False)

            Egij = np.amax(Eij_potentiels)
            des = np.argmax(Eij_potentiels) + 1
        else:

            for k in range(len(proba_table)):

                for x in range(1, len(proba_table[k])):

                    if proba_table[k][x] != 0.:

                        if (j + x < M) and Eg_table_j1[i, j + x] != 1000.:
                            Eij_potentiels[k] += proba_table[k][x] * Eg_table_j1[i, j + x]
                        else:
                            Eij_potentiels[k] += proba_table[k][x] * egPaul(i, j + x, True)
            Egij = np.amin(Eij_potentiels)
            des = np.argmin(Eij_potentiels) + 1

        if Eg_table_which_play_j1[i, j] == 1000. and j1:
            Eg_table_which_play_j1[i, j] = des

        if Eg_table_which_play_j2[i, j] == 1000. and not j1:
            Eg_table_which_play_j2[i, j] = des

        if Eg_table_j1[i, j] == 1000. and j1:
            Eg_table_j1[i, j] = Egij
        elif Eg_table_j2[i, j] == 1000. and not j1:
            Eg_table_j2[i, j] = Egij

        return Egij

    return egPaul(i, j, j1), Eg_table_j1, Eg_table_j2, Eg_table_which_play_j1, Eg_table_which_play_j2


Eij, Eg_table_j1, Eg_table_j2, Eg_table_which_play_j1, Eg_table_which_play_j2 = eg(2, 10, 0, 0, True)



