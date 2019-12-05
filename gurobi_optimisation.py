#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.
from simultane import *

from gurobipy import *

def strat_opt_simu(D):

    matrice_de_gain = EGmatP(D)

    nbcont = D+1
    nbvar = D

    # Range of plants and warehouses
    lignes = range(nbcont-1)
    colonnes = range(nbvar)

    # Matrice des contraintes
    a = matrice_de_gain


    # Coefficients de la fonction objectif
    c = [0]*D

    m = Model("mogplex")

    # declaration variables de decision
    x = []
    for i in colonnes:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i + 1)))

    # maj du modele pour integrer les nouvelles variables
    m.update()

    obj = LinExpr();
    obj = 0
    for j in colonnes:
        obj += c[j] * x[j]

    # definition de l'objectif
    m.setObjective(obj, GRB.MAXIMIZE)

    # Definition des contraintes
    for i in lignes:
        m.addConstr(quicksum(a[i][j] * x[j] for j in colonnes) <= 0, "Contrainte%d" % i)
    left_member=0
    for i in range(D):
        left_member+=x[i]

    m.addConstr(left_member == 1, "Contrainte%d" % 4)

    # Resolution
    m.optimize()

    """print("")
    print('Solution optimale:')
    for j in colonnes:
        print('x%d' % (j + 1), '=', x[j].x)
    print("")
    print('Valeur de la fonction objectif :', m.objVal)"""

    strat_vec = np.zeros(D)
    for j in colonnes:
        strat_vec[j]=x[j].x

    return strat_vec


strat_vec=strat_opt_simu(10)