from jeu import *

D = 10
M = 100
strat = {"aveugle": pb.max_esp, "optimale": choose_optimale}
player1 = strat["optimale"]
player2 = strat["aveugle"]
nb_parties = 1000

resultats = metaloopSeq(nb_parties, player1, player2, M, D)
print(resultats)
print((resultats[0] / nb_parties) - (resultats[1] / nb_parties))
