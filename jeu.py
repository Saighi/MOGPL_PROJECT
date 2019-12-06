import os.path

import numpy as np

import probability as pb

import pandas as pd

"""Q7"""

def chooseStrat():
    strat = {"aveugle": pb.max_esp}
    n = 0

    for key, values in strat.items():
        print(str(n) + " - " + key)
        n += 1

    i = int(input("wich strat ? : "))

    return list(strat.items())[i][1]


def choose_optimale(Eg_table_which_play, i, j):
    return int(Eg_table_which_play[i, j])


def choose_aleatoire(D):
    return np.random.randint(1, D + 1)

def humainStrat(D):
    i = int(input("pick between 1 and " + str(D) + " dices "))

    while i > D:
        print("not enough dices")
        i = int(input("pick between 1 and " + str(D) + " dices "))

    return i


def dice(d):
    r = np.random.randint(1, 7, size=(d,))

    if 1 in r:
        return 1
    else:
        return np.sum(r)


# Permet de ne pas recalculer les tables quand on joue un grand nombre de parties avec les mêmes paramètres.
def metaloopSeq(nb_parties, player1, player2, M, D):
    Eg_table_which_play_p1, Eg_table_which_play_p2 = None, None

    if player1 == choose_optimale or player2 == choose_optimale:

        if os.path.isfile("tables_tpt/npy/which_play_p1_" + str(D) + "_" + str(M) + ".npy") and os.path.isfile(
                "tables_tpt/npy/which_play_p2_" + str(D) + "_" + str(M) + ".npy"):
            Eg_table_which_play_p1 = np.load("tables_tpt/npy/which_play_p1_" + str(D) + "_" + str(M) + ".npy")
            Eg_table_which_play_p2 = np.load("tables_tpt/npy/which_play_p2_" + str(D) + "_" + str(M) + ".npy")

        else:
            _, _, _, Eg_table_which_play_p1, Eg_table_which_play_p2 = pb.eg(D, M, 0, 0, True)
            np.save("tables_tpt/npy/which_play_p1_" + str(D) + "_" + str(M), Eg_table_which_play_p1)
            np.save("tables_tpt/npy/which_play_p2_" + str(D) + "_" + str(M), Eg_table_which_play_p2)
            df = pd.DataFrame(Eg_table_which_play_p1)
            f = open("tables_tpt/txt/which_play_p1_" + str(D) + "_" + str(M)+".html", "w")
            f.write(df.to_html())
            df = pd.DataFrame(Eg_table_which_play_p2)
            f = open("tables_tpt/txt/which_play_p2_" + str(D) + "_" + str(M)+".html", "w")
            f.write(df.to_html())


    wins = 0
    looses = 0
    for i in range(nb_parties):
        if main_for_meta_loopSeq(player1, player2, M, D, Eg_table_which_play_p1,
                                 Eg_table_which_play_p2) == 1:
            wins += 1
        else:
            looses += 1

    return wins, looses


def main_for_meta_loopSeq(player1, player2, M, D, Eg_table_which_play_p1,
                          Eg_table_which_play_p2):
    p1 = 0
    p2 = 0
    n = 0

    # Utile pour le calcul de l'espérence de gain du joueur 1
    while p1 < M and p2 < M:

        n += 1

        if player1 == choose_optimale:
            p1 += dice(player1(Eg_table_which_play_p1, p1, p2))
        else:
            p1 += dice(player1(D))

        if p1 >= M:
            return 1

        if player2 == choose_optimale:
            p2 += dice(player2(Eg_table_which_play_p2, p1, p2))
        else:
            p2 += dice(player2(D))

        if p2 >= M:
            return -1

# start_game(100, 10)

def simulation_simul(nb_parties, D, V1, V2):
    win = 0
    loose = 0
    null = 0
    dice_lance = np.zeros(D)
    dice_lance2 = np.zeros(D)
    for i in range(nb_parties):
        Vc1 = np.cumsum(V1)
        d1 = np.where(Vc1 > np.random.rand(1)[0])[0][0] + 1

        Vc2 = np.cumsum(V2)
        d2 = np.where(Vc2 > np.random.rand(1)[0])[0][0] + 1

        lance_d1 = dice(d1)
        lance_d2 = dice(d2)

        if lance_d1 > lance_d2:
            win += 1
        if lance_d1 == lance_d2:
            null += 1
        if lance_d1 < lance_d2:
            loose += 1
    return win, loose, null
