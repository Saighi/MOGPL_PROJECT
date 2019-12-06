from probability import *
from gurobi_optimisation import *

""" Q17 """
def eg_d(i, j, table_d1, table_d2, Eg_table_j1_k_l):
    sum_1 = 0
    for k in range(1, len(table_d1)):
        sum_2 = 0
        for l in range(1, len(table_d2)):
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

""" Q18 """
def eg_simu_meta(i, j, D, N):
    table_D = p_table(D)
    Eg_table_j1 = np.full((N, N), 1000.)
    Eg_table_which_play_j1 = [[0]*N]*N

    def eg_simu(i, j):

        if i >= N and j >= N:
            if i == j:
                return 0
            if i > j:
                return 1
            if j > i:
                return -1

        if i >= N:
            return 1
        if j >= N:
            return -1

        if i == j and i != 0:
            Eg_table_j1[i, j] = 0
            return 0

        Eg_table_j1_k_l = np.zeros((N+(6*D), N+(6*D)))

        for x in range(i+1, N+(6*D)):
            for y in range(j+1, N+(6*D)):
                if x < N and y < N and Eg_table_j1[x, y] != 1000.:
                    Eg_table_j1_k_l[x, y] = Eg_table_j1[x, y]
                else:
                    Eg_table_j1_k_l[x, y] = eg_simu(x, y)

        eg_d_t_1 = eg_d_table(i, j, table_D, Eg_table_j1_k_l)
        strat_opti_1, val_max = strat_opt_simu_mat(eg_d_t_1)

        Eg_table_j1[i, j] = val_max
        Eg_table_which_play_j1[i][j] = strat_opti_1
        return val_max

    return eg_simu(i, j), Eg_table_j1,Eg_table_which_play_j1


eg_fac, Eg_table_j1, Eg_table_which_play_j1 = eg_simu_meta(0, 0, 10, 20)
np.save("tables_simu/vec_D10_M20",Eg_table_j1)