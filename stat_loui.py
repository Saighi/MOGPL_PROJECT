from jeu import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

D = 10
M = 100
strat = {"aveugle": pb.max_esp, "optimale": choose_optimale, "aleatoire": choose_aleatoire}

def gameResM(strat1,strat2,Mmin,Mmax,D):

    resultats = {}
    resultats["M"] = []
    resultats["1"] = []
    resultats["2"] = []
    nb_parties = 1000

    print("start")

    for M in range(Mmin,Mmax,5):

        print(M)
        result1 = metaloopSeq(nb_parties, strat1, strat2, M, D)
        result2 = metaloopSeq(nb_parties, strat1, strat2, M, D)
        resultats["M"].append(M)
        resultats["1"].append((result1[0] / nb_parties) - (result1[1] / nb_parties))
        resultats["2"].append((result2[0] / nb_parties) - (result2[1] / nb_parties))

    r=pd.DataFrame()
    r['M']=resultats['M']
    r["1"]=resultats["1"]
    r["2"]=resultats["2"]

    r = pd.melt(r, id_vars=['M'], value_vars=['1','2'],
          var_name='groupe', value_name='Esperance')

    a = sns.lineplot(x=r["M"],y=r["Esperance"],
                 palette=sns.color_palette("pastel", 2))

    plt.show()

    a.get_figure().savefig("img/aveugle_aleatoire.png")

gameResM(strat["optimale"],strat["aleatoire"],10,100,10)
