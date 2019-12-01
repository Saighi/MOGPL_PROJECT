import numpy as np

import probability as pb


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


def humainStrat(D):
    i = int(input("pick between 1 and " + str(D) + " dices "))

    while i > D:
        print("not enough dices")
        i = int(input("pick between 1 and " + str(D) + " dices "))

    return i


def dice(d):
    r = np.random.randint(6, size=(d,))

    if 1 in r:
        return 1
    else:
        return np.sum(r)


def mainloopSeq(player1, player2, M, D, affichage=True):
    p1 = 0
    p2 = 0
    n = 0
    Eg_table_which_play_p1 = None
    Eg_table_which_play_p2 = None

    if player1 == chooseStrat:
        player1 = chooseStrat()

    if player2 == chooseStrat:
        player2 = chooseStrat()

    if player1 == choose_optimale:
        _, _, _, Eg_table_which_play_p1 = pb.eg(D, M, 0, 0, True)

    if player2 == choose_optimale:
        _, _, _, Eg_table_which_play_p2 = pb.eg(D, M, 0, 0, False)

    if affichage:
        while p1 < M and p2 < M:

            n += 1
            print("turn : " + str(n))
            p1 += dice(player1(D))
            print("p1 : " + str(p1))
            if p1 >= M:
                print("player 1 won")
                break
            p2 += dice(player2(D))
            print("p2 : " + str(p2))
            if p2 >= M:
                print("player 2 won")
                break
    else:
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
                p2 += dice(player2(Eg_table_which_play_p2, p2, p1))
            else:
                p2 += dice(player2(D))

            if p2 >= M:
                return -1


def start_game(M, D, simultane=False):
    print("0 - humain vs humain")
    print("1 - humain vs bot")
    print("2 - bot vs bot")
    t = int(input("what do you what to play ? : "))

    print(type(t))

    if t == 0:
        mainloopSeq(humainStrat, humainStrat, M, D)
    elif t == 1:
        mainloopSeq(humainStrat, chooseStrat(), M, D)
    elif t == 2:
        mainloopSeq(chooseStrat(), chooseStrat(), M, D)

# start_game(100, 10)
