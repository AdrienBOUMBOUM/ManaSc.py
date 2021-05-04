#CarbuVert+FH

from pulp import *
import pandas as pd


### DATA ###

df = pd.read_excel("Data_Silo.xlsx", nrows=12)

silo = list(df['Silo'])

humidity = dict(zip(silo, df['humidity']))
density = dict(zip(silo, df['density']))
dommage = dict(zip(silo, df['dommage']))
non_organic = dict(zip(silo, df['non-organic']))
quantity = dict(zip(silo, df['quantity']))

print(silo, humidity, density, dommage, non_organic, quantity)

### DATA CLIENTS ###

df = pd.read_excel("Data_Clients1.xlsx", nrows=3)

clients = list(df['Client'])

c_humidity = dict(zip(clients, df['humidity']))
c_density = dict(zip(clients, df['density']))
c_dommage = dict(zip(clients, df['dommage']))
c_non_organic = dict(zip(clients, df['non-organic']))
c_quantitymin = dict(zip(clients, df['Qmin']))
c_quantitymax = dict(zip(clients, df['Qmax']))

print(clients, c_density, c_dommage, c_non_organic, c_quantitymax, c_quantitymin, c_humidity)

### MODEL ###

model = LpProblem(sense=LpMaximize)

X = [[LpVariable("Client " + str(i) + " Silo " + str(j),lowBound=0) for j in range(12)] for i in range(3)]

R = 67

#prix demandé a chaque client
for i in clients
    p[i] = (R * 1.15) - (0.5 * c_humidity[i]) - c_dommage[i] - c_non_organic[i] + (5 * c_density[i])



### CONSTRAINTS ###
### Contrainte de positivité du blé dans les silos ###
for j in silo:
    model += lpSum([X[i, j] for i in clients]) <= quantity[j]
##Carbu vert pas livré par FH a cause des dates
X[1, 12] = 0

#contrainte clients

# Contraintes quantités demandées
for i in clients:
    model += lpSum([X[i, j] for j in silo]) >= c_quantitymin[i]
    model += lpSum([X[i, j] for j in silo]) <= c_quantitymax[i]

tot_c = {} #total
for i in clients:
    tot_s = 0 #qté que les clients recoivent de chaque silo
    for j in silo:
        if j == len(silo):
            tot_s += X[i, j]
            tot_c[i] = tot_s
            break
        else:
            pass
        tot_s += X[i, j]

for i in clients:
    model += lpSum([X[i, j] * humidity[j] for j in silos]) <= c_humidity[i] * tot_c[i]#contrainte Humidi
    model += lpSum([X[i, j] * dommage[j] for j in silos]) <= c_dommage[i] * tot_c[i]#contrainte endommage
    model += lpSum([X[i, j] * non_organic[j] for j in silos]) <= c_non_organic[i] * tot_c[i]#contrainte non organique
    model += lpSum([X[i, j] * density[j] for j in silos]) >= c_density[i] * tot_c[i]#contrainte densite
    
model.resolve()
client = ""
for i in range(3):
        for j in range(12):
                X[i][j] = value(x[i][j])
                if i == 0 :
                        client = "CarbuVert"

                elif i == 1:
                        client = "TendreViande"

                else :
                        client = "HappyBle"

                print("Le silo {}, a vendu {} au client {}".format(j+1,x[i][j],client))

