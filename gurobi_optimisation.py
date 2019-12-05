#!/usr/bin/python

from gurobipy import *

# Copyright 2013, Gurobi Optimization, Inc.
from simultane import *


def strat_opt_simu(D):
    matrice_de_gain = EGmatP(D)
    nbcont = D + 1
    nbvar = D

    # Range of plants and warehouses
    lignes = range(nbcont - 1)
    colonnes = range(nbvar)

    # Matrice des contraintes
    a = matrice_de_gain

    # Coefficients de la fonction objectif

    m = Model("mogplex")
    m.setParam('OutputFlag', False)

    # declaration variables de decision
    x = []
    for i in colonnes:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i + 1)))

    val_max = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="val_min")

    # maj du modele pour integrer les nouvelles variables
    m.update()

    obj = val_max

    # definition de l'objectif
    m.setObjective(obj, GRB.MAXIMIZE)

    # Definition des contraintes
    for i in colonnes:
        m.addConstr(val_max - quicksum(a[j][i] * x[j] for j in lignes) <= 0, "Contrainte%d" % i)

    left_member = 0
    for i in range(D):
        left_member += x[i]

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
        strat_vec[j] = x[j].x
    return strat_vec


def strat_opt_simu_mat(matrice_de_gain):
    D = len(matrice_de_gain)

    nbcont = D + 1
    nbvar = D

    # Range of plants and warehouses
    lignes = range(nbcont - 1)
    colonnes = range(nbvar)

    # Matrice des contraintes
    a = matrice_de_gain

    # Coefficients de la fonction objectif

    m = Model("mogplex")
    m.setParam('OutputFlag', False)

    # declaration variables de decision
    x = []
    for i in colonnes:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i + 1)))

    val_max = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="val_min")

    # maj du modele pour integrer les nouvelles variables
    m.update()

    obj = val_max

    # definition de l'objectif
    m.setObjective(obj, GRB.MAXIMIZE)

    # Definition des contraintes
    for i in colonnes:
        m.addConstr(val_max - quicksum(a[j][i] * x[j] for j in lignes) <= 0, "Contrainte%d" % i)

    left_member = 0
    for i in range(D):
        left_member += x[i]

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
        strat_vec[j] = x[j].x

    return strat_vec

# opt = EGmatP(2)
# strat_vec=strat_opt_simu(10)
