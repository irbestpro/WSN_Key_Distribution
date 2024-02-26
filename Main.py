'''

This Code is Written By: Mehdi Touyserkani - Feb 2024.
BESTPRO SOFTWARE ENGINEERING GROUP

Base Paper: https://arxiv.org/pdf/1901.07314.pdf

'''

from gekko import GEKKO

import numpy as np
import math

import warnings
warnings.filterwarnings("ignore")

#________________Import Local Functions____________________________________

from Create_Graphs import create_erods_renyi_graph
from Parameters import Params
from Nodes import Nodes

indexer = 0 # accessing to Expected Vertexes,Nodes,Memory limitation and etc

#_______________________Geaph Creation_______________________________________

G1 = create_erods_renyi_graph(Params.V[indexer])# Create A Graph with specified Nodes Count
nodes = np.array(G1.nodes) # Access to WSN Nodes
Edges = np.array(G1.edges) # Access To WSN Edges
Adj_Matrix = np.zeros((len(nodes) , len(nodes))) #adjacency matrix

for x in Edges:
    Adj_Matrix[x[0],x[1]],Adj_Matrix[x[1],x[0]] = 1,1 # create ADJ Matrix

Nodes_List = nodes # Defining Nodes_List in Variables-Vector

#____________Define the limit on assigning Keys to Nodes_List________________

Max_Key_Length = Params.K[indexer]
Assigned_Key_Length = Params.tk[indexer]

#_____________Defining WSN-Key Distribution Problem(KMP)_____________________

model = GEKKO(remote=False)

#______Define Decision variable for assigning k-keys to each Nodes___________

Keys = model.Array(model.Var,(len(Nodes_List),Max_Key_Length), integer=True , lb=0 , ub = 1)

#_____Objective Function According to Key Distribution (Base Paper: 1a)______

z = sum(1 for i in Nodes_List for j in Nodes_List if(Adj_Matrix[i][j]==1) for h in range(0,Max_Key_Length) for k in range(0,Max_Key_Length) if(Keys[i,h].value == Keys[j,k].value))
model.Maximize(z)

# ______________________Constraints Definition_______________________________

for k in range(0,Max_Key_Length):
    model.Equation(model.sum(Keys[:,k]) >= Params.tk[indexer]) # Constraint 1e
    model.Equation(model.sum(Params.mk * Keys[:,k]) <= Params.ci[indexer]) # Constraint 1b
    for i in Nodes_List:
        Neighbors = np.where(Adj_Matrix[i]==1) # Extract Neighbors
        for j in Neighbors:
            yijk = model.sum([Keys[i,k],Keys[j,k]]) # node i , j have shared common key k
            model.Equation(yijk <= (Params.p * len(Neighbors)) + Params.alpha ) # Constraint 3c
            for l in j:
                zij = sum(1 for x in range(0,Max_Key_Length) if(Keys[i,x].value == Keys[l,x].value)) == Params.q
                model.Equation( yijk >= Params.q * zij) # Constraint 3b
                model.Equation([yijk <= Keys[i,k]]) # Constraint 3d
                model.Equation([yijk <= Keys[l,k]]) # Constraint 3d
                model.Equation([yijk >= Keys[i,k] + Keys[l,k] - 1]) # Constraint 3e

#_____________Slove The problem by Integer Programming Optimizer_____________

model.options.SOLVER = 1
model.solve(disp = True , debug=True)

print(Keys)

#_________________Create Node Structures_________________________________

WSN_Nodes = np.empty((len(Nodes_List),), dtype=object)

for i in Nodes_List:
    temp = Nodes(i)
    WSN_Nodes[i] = temp
    for j in range(0,Max_Key_Length):
        WSN_Nodes[i].Add_Key(Keys[i,j].value)
        WSN_Nodes[i].Add_Name("Key" + str(i) + str(j))

#___________Show final Result and Optimization Process___________________

print('\n-------------------\n' , 'Adjacency Matrix: \n\n' ,Adj_Matrix , '\n-------------------\n')

for i in Nodes_List:
    for j in range(0,len(WSN_Nodes[i].keys)):
        print('Node #' , WSN_Nodes[i].id , ':' , ' , Key #', j  , ':' , WSN_Nodes[i].keys[j])
    print('\n-------------------\n')
print('Objective: ', -model.options.OBJFCNVAL)
