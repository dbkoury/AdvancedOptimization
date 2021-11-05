# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 23:19:41 2021

@author: dylan
"""
import random
from pulp import LpVariable, LpProblem, LpMaximize, LpStatus, value, LpMinimize

status = 0
LpStatus[status] = "Infeasible"
while LpStatus[status] == "Infeasible":
    #indexed ranges
    P = 10 #number of facilities (i)
    Q = 3 #number of hybrid corns (j)
    T = 3 #number of regions (k)
    
    #data 
        #Processing Capacity
    U = []
    for i in range(P): #loop through facilities
        U.append(int(random.random()*1000))
        
         #Number of Bushels per bag  
    b = []
    for j in range(Q): #loop through hybrids
        b.append(int(random.random()*10))
        
        #Cost of Bag of Hybrid j at Facility i
    c = []
    for i in range(P):
        facilityrow = []
        for j in range(Q):
            facilityrow.append(round(random.random()*10,2))
        c.append(facilityrow)
            
        #Demand of Hybrid j in region k
    d = []
    for j in range(Q):
        hybridrow = []
        for k in range(T):
            hybridrow.append(round(random.random()*1000))
        d.append(hybridrow)
        
        #Shipping cost of hybrid j from facility i to region k
    S = []
    for i in range(P):
        facilityrow = []
        for j in range(Q):
            hybridrow = []
            for k in range(T):
                hybridrow.append(round(random.random()*10,2))
            facilityrow.append(hybridrow)
        S.append(facilityrow)
        
    #Decision Variables
        #Production Amount of hybrid j at facility i
    X = []
    for i in range(P):
        facilityrow = []
        for j in range(Q):
            facilityrow.append(LpVariable(f"X{i}{j}",0,None))
        X.append(facilityrow)
        
        #Amount of Hybrid j Shipped from Facility i to Region k
    Y = []
    for i in range(P):
        facilityrow = []
        for j in range(Q):
            hybridrow = []
            for k in range(T):
                hybridrow.append(LpVariable(f"Y{i}{j}{k}",0,None))
            facilityrow.append(hybridrow)
        Y.append(facilityrow)
    
    #define problem
    prob = LpProblem("problem", LpMinimize)
    
    #constraints
        #Capacity Constraints
    for i in range(P):
        globals()[f'production{i}'] = 0
        for j in range(Q):
            globals()[f'production{i}'] += b[j]*X[i][j]
        prob += globals()[f'production{i}'] <= U[i]
        
        #Demand Constraints
    for j in range(Q):
        for k in range(T):
            globals()[f'ship{j}{k}'] = 0
            for i in range(P):
                globals()[f'ship{j}{k}'] += Y[i][j][k]
            prob += globals()[f'ship{j}{k}'] == d[j][k]
            
        #Flow Constraints
    for i in range(P):
        for j in range(Q):
            globals()[f'flow{i}{j}'] = 0
            for k in range(T):
                globals()[f'flow{i}{j}'] += Y[i][j][k]
            prob += globals()[f'flow{i}{j}'] == X[i][j]
    
    #objective: Min Cost
        #Production Costs
    prodcost = 0
    for i in range(P):
        for j in range(Q):
            prodcost += c[i][j]*X[i][j]
        #Shipping Costs
    shipcost = 0
    for i in range(P):
        for j in range(Q):
            for k in range(T):
                shipcost += S[i][j][k]*Y[i][j][k]
                
        #Min Cost
    prob += prodcost + shipcost
    
    # solve the problem
    status = prob.solve()
print(f"Problem")
print(f"status={LpStatus[status]}")
print(f"")
if LpStatus[status] == "Optimal":
    print(f"Min Cost = ${round(value(prob.objective),2)}\n")
    print("\t\tProduction and Shipping of Hybrids to Regions By Facility")
    for i in range(P):
        print(f"Facility {i + 1}")
        for j in range(Q):
            print(f'\tHybrid {j + 1}\t\t',X[i][j].varValue)
            for k in range(T):
                print(f"\t\tRegion {k + 1}\t\t",Y[i][j][k].varValue)
                print(f"")
    
            