from pulp import *
import pandas as pd
import numpy as np


df = pd.read_excel("Classeur.xlsx", nrows=11)

silo = list(df['Silo'])

humidity = dict(zip(silo, df['humidity']))
density = dict(zip(silo, df['density']))
dommage = dict(zip(silo, df['dommage']))
non_organic = dict(zip(silo, df['non-organic']))
quantity = dict(zip(silo, df['quantity']))
cost = dict(zip(silo, df['cost']))
print(silo, humidity, density, dommage, non_organic, quantity)

# DATA CLIENTS #
df = pd.read_excel("Data_Clients.xlsx", nrows=3)

clients = np.arange(3)

c_humidity = dict(zip(clients, df['humidity']))
c_density = dict(zip(clients, df['density']))
c_dommage = dict(zip(clients, df['dommage']))
c_non_organic = dict(zip(clients, df['non-organic']))
c_quantitymin = dict(zip(clients, df['Qmin']))
c_quantitymax = dict(zip(clients, df['Qmax']))

print(clients, c_density, c_dommage, c_non_organic, c_quantitymax, c_quantitymin, c_humidity)

m = LpProblem(sense=LpMaximize)

###CREATION DES VARIABLES

x = [[LpVariable("Client " + str(i) + " Silo " + str(j),lowBound=0) for j in range(11)] for i in range(3)]
Y = [0] + [LpVariable("Client " + str(i) + " A LA FH",lowBound=0) for i in range(2)]

###CONTRAINTES


# Contrainte quantité

for i in range(3):
        m += lpSum(x[i]) + Y[i] <= c_quantitymax[i]
        m += lpSum(x[i]) + Y[i] >= c_quantitymin[i]

        m += lpSum(x[i]) + Y[i] <= c_quantitymax[i]*c_humidity[i]
        m += lpSum(x[i]) + Y[i] >= c_quantitymin[i]*c_humidity[i]

        m += lpDot(list(density.values()), x[i]) + 0.85*Y[i] <= c_quantitymax[i]*c_density[i]
        m += lpDot(list(density.values()), x[i]) + 0.85*Y[i] >= c_quantitymin[i]*c_density[i]

        m += lpDot(list(dommage.values()), x[i]) + 0.02*Y[i] <= c_quantitymax[i]*c_dommage[i]
        m += lpDot(list(dommage.values()), x[i]) + 0.02*Y[i] >= c_quantitymin[i]*c_dommage[i]

        m += lpDot(list(non_organic.values()), x[i]) + 0.02*Y[i] <= c_quantitymax[i]*c_non_organic[i]
        m += lpDot(list(non_organic.values()), x[i]) + 0.02*Y[i] >= c_quantitymin[i]*c_non_organic[i]

p = np.zeros(3)
for i in range(3):
        p[i] = 67*1.15-0.5*c_humidity[i]-c_dommage[i]-c_non_organic[i] + 5*c_density[i]

### FONCTION OBJECTIF 1

"""
m += lpDot([lpSum(x[0]),lpSum(x[1]),lpSum(x[2])],p) - lpSum([lpDot(x[0],cost),lpDot(x[1],cost),lpDot(x[2],cost)]) - 60.5 * lpSum(Y)
"""

### FONCTION OBJECTIF 2
"""
m += lpDot([lpSum(x[0]),lpSum(x[1]),lpSum(x[2])],p) - lpSum([lpDot(x[1],cost),lpDot(x[2],cost)]) - 60.5 * lpSum(Y)
"""

### FONCTION OBJECTIF 3
"""
m += lpDot([lpSum(x[0]),lpSum(x[1]),lpSum(x[2])],p) - lpSum([lpDot(x[0],cost),lpDot(x[1],cost),lpDot(x[2],cost)])

"""

### FONCTION OBJECTIF 4

m += lpDot([lpSum(x[0]),lpSum(x[1]),lpSum(x[2])],p) - lpSum([lpDot(x[1],cost),lpDot(x[2],cost)])


### RESOLUTION
m.resolve()
client = ""
for i in range(3):
        for j in range(11):
                x[i][j] = value(x[i][j])
                if i == 0 :
                        client = "CarbuVert"

                elif i == 1:
                        client = "TendreViande"

                else :
                        client = "HappyBle"

                print("Le silo {}, a vendu {} au client {}".format(j+1,x[i][j],client))

        print("La FH a vendu {} au client {}".format(value(Y[i]),client))