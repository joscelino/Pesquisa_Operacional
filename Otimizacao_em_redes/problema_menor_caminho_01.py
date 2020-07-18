from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMinimize, value
from typing import List, Dict


# Problem data
nodes: List = [0, 1, 2, 3, 4]
source: int = 0
destination: int = 1
fork: List = [[0, 1, 1, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 1, 1],
              [0, 1, 0, 0, 1],
              [0, 0, 0, 0, 0]]

costs: List = [[0, 300, 90, 0, 0],
               [0, 0, 60, 0, 0],
               [0, 0, 0, 30, 180],
               [0, 45, 0, 0, 150],
               [0, 0, 0, 0, 0]]

# Decision variables
var: Dict = {}
for i in nodes:
    for j in nodes:
        if fork[i][j] == 1:
            var[(i, j)] = LpVariable(name=f'x{i}{j}', cat='Binary')
        else:
            continue
    var.update(var)

# Model
model = LpProblem('Shortest_path_problem', LpMinimize)

# Goal function
model += lpSum(var[x] * costs[x[0]][x[1]] for x in var.keys())
    
# Constrains
constrains_o: List = []
constrains_f: List = []

for node in nodes:
    for edge in var.keys():
        
        if edge[0] == node:
            constrains_o.append(var[edge])
            
        if edge[1] == node:
            constrains_f.append(var[edge])
            
    if node == source:
        model += lpSum(constrains_o) == 1
    elif node == destination:
        model += lpSum(constrains_f) == 1
    else:
        model += lpSum(constrains_o) - lpSum(constrains_f) == 0
    
    constrains_o: List = []
    constrains_f: List = []

print(model)

# Model solution
status: int = model.solve()


# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')
print(f'The cost is $: {round(value(model.objective), 2)}')
print(" ")

for x in var.values():
    if value(x) == 1:
        print(f'{x} = {value(x)}')
    else:
        continue
