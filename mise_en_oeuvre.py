from jeu import *

D = 2
M = 10

strat = {"aveugle": pb.max_esp, "optimale": choose_optimale}
player1 = strat["optimale"]
player2 = strat["optimale"]

echantillon = 10000
resultats = 0

for i in range(echantillon):
    resultats += mainloopSeq(player1, player2, M, D, affichage=False)

esperence_ = resultats / echantillon
print(esperence_)
