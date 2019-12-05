from probability import *

def eg_d(i,j,table_d1,table_d2,Eg_table_j1_k_l):
    sum_1=0
    for k in range(len(table_d1)):
        sum_2=0
        for l in range(len(table_d2)):
            sum_2 += table_d2[j]* Eg_table_j1_k_l[i+k,j+l]
        sum_1+= table_d1[i] * sum_2
    return sum_1

def eg_d_table(i,j,table_D,Eg_table_j1_k_l):
    D = len(table_D)
    table_eg_d = np.zeros((D,D))

    for x in range(D):
        for y in range(D):
            table_eg_d[x,y] = eg_d(i, j, table_D[x+1], table_D[y+1], Eg_table_j1_k_l)
            pass

    return table_eg_d
