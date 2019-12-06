from jeu import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

D = 10
N = 100
strat = {"aveugle": pb.max_esp, "optimale": choose_optimale, "aleatoire": choose_aleatoire}

def gameResN(strat1,strat2,Nmin,Nmax,D):

    resultats = {}
    resultats["N"] = []
    resultats["1"] = []
    resultats["2"] = []
    nb_parties = 1000

    print("start")

    for N in range(Nmin,Nmax,5):

        print(N)
        result1 = metaloopSeq(nb_parties, strat1, strat2, N, D)
        result2 = metaloopSeq(nb_parties, strat1, strat2, N, D)
        resultats["N"].append(N)
        resultats["1"].append((result1[0] / nb_parties) - (result1[1] / nb_parties))
        resultats["2"].append((result2[0] / nb_parties) - (result2[1] / nb_parties))

    r=pd.DataFrame()
    r['N']=resultats['N']
    r["1"]=resultats["1"]
    r["2"]=resultats["2"]

    r = pd.melt(r, id_vars=['N'], value_vars=['1','2'],
          var_name='groupe', value_name='Esperance')

    a = sns.lineplot(x=r["N"],y=r["Esperance"],
                 palette=sns.color_palette("pastel", 2))

    plt.show()

    a.get_figure().savefig("img/aveugle_optimale.png")

gameResN(strat["aveugle"],strat["optimale"],10,100,10)
