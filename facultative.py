from probability import *
from gurobi_optimisation import *


def eg_d(i, j, table_d1, table_d2, Eg_table_j1_k_l):
    sum_1 = 0
    for k in range(len(table_d1)):
        sum_2 = 0
        for l in range(len(table_d2)):
            sum_2 += table_d2[l] * Eg_table_j1_k_l[i + k, j + l]
        sum_1 += table_d1[k] * sum_2
    return sum_1


def eg_d_table(i, j, table_D, Eg_table_j1_k_l):
    D = len(table_D)-1
    table_eg_d = np.zeros((D, D))
    for x in range(D):
        for y in range(D):
            table_eg_d[x, y] = eg_d(i, j, table_D[x + 1], table_D[y + 1], Eg_table_j1_k_l)

    return table_eg_d


def eg_simu_meta(i, j, D, N):
    table_D = p_table(D)
    Eg_table_j1 = np.full((N, N), 1000.)

    # Eg_table_which_play_j1 = np.full((N, N), 1000.)
    def eg_simu(i, j):

        if i == j and i!= 0:
            return 0

        if i >= N and j >= N:
            return 0
        if i >= N:
            return 1
        if j >= N:
            return -1

        Eg_table_j1_k_l = np.zeros((N+(6*D), N+(6*D)))

        for x in range(i+1, D+(6*D)):
            for y in range(j+1, D+(6*D)):
                if x < N and y < N and Eg_table_j1[x, y] != 1000.:
                    Eg_table_j1_k_l[x, y] = Eg_table_j1[x, y]
                else:
                    Eg_table_j1_k_l[x, y] = eg_simu(x, y)

        eg_d_t = eg_d_table(i, j, table_D, Eg_table_j1_k_l)
        print(eg_d_t)
        strat_opti = strat_opt_simu_mat(eg_d_t)

        eg = 0
        for x in range(len(strat_opti)):
            sum = 0
            for y in range(len(strat_opti)):
                sum += strat_opti[y] * eg_d_t[x, y]
            eg += strat_opti[x] * sum
        if Eg_table_j1[i, j] == 1000.:
            Eg_table_j1[i, j] = eg
        return eg

    return eg_simu(i, j), Eg_table_j1


eg_fac = eg_simu_meta(0, 0, 2, 10)
