#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.
from simultane import *

from gurobipy import *

matrice_de_gain = EGmatP(10)

nbcont = 11
nbvar = 10

# Range of plants and warehouses
lignes = range(nbcont-1)
colonnes = range(nbvar)

# Matrice des contraintes
a = matrice_de_gain


# Coefficients de la fonction objectif
c = [0]*10

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
m.addConstr(x[0]+x[1] + x[2]+ x[3]+x[4] + x[5]+ x[6]+x[7] + x[8]+x[9] == 1, "Contrainte%d" % 4)

# Resolution
m.optimize()

print("")
print('Solution optimale:')
for j in colonnes:
    print('x%d' % (j + 1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)


