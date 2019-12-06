from gurobi_optimisation import strat_opt_simu
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

def gameResN_simu(V1,V2,Dmin,Dmax,nb_parties):

    resultats = {}
    resultats["D"] = []
    resultats["1"] = []
    resultats["2"] = []

    print("start")

    for D in range(Dmin, Dmax, 1):
        print(D)
        result1 = simulation_simul(nb_parties, D, V1, V2)
        result2 = simulation_simul(nb_parties, D, V2, V1)
        resultats["D"].append(D)
        resultats["1"].append((result1[0] / nb_parties) - (result1[1] / nb_parties))
        resultats["2"].append((result2[0] / nb_parties) - (result2[1] / nb_parties))

    r=pd.DataFrame()
    r['D']=resultats['D']
    r["1"]=resultats["1"]
    r["2"]=resultats["2"]

    r = pd.melt(r, id_vars=['D'], value_vars=['1','2'],
          var_name='groupe', value_name='Esperance')

    a = sns.lineplot(x=r["D"],y=r["Esperance"],
                 palette=sns.color_palette("pastel", 2))

    plt.show()

    a.get_figure().savefig("img/aveugle_optimale_simu.png")

"""
V1 = strat_opt_simu(D)
V2 = np.zeros(D)
V2[6]=1
"""
#gameResN_simu(V1,V2, 1, 15, 100000)