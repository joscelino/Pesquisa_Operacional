from typing import Dict, List

from pulp import LpMaximize, LpProblem, LpStatus, LpVariable, lpSum, value

# Problem data
nodes: List = [0, 1, 2, 3, 4]
source: int = 0
destination: int = 4

fork: List = [[0, 1, 1, 1, 0],
              [0, 0, 1, 0, 1],
              [0, 0, 0, 1, 1],
              [0, 0, 1, 0, 1],
              [0, 1, 0, 1, 0]]

availabilities: List = [[0, 200, 300, 100, 0],
                        [0, 0, 400, 0, 300],
                        [0, 0, 0, 100, 200],
                        [0, 100, 50, 0, 200],
                        [0, 100, 0, 100, 0]]

# Decision variables
var: Dict = {}
for i in nodes:
    for j in nodes:
        if fork[i][j] == 1:
            var[(i, j)] = LpVariable(name=f'x{i}{j}', lowBound=0, cat='Integer')
        else:
            continue
    var.update(var)

# Model
model = LpProblem("Maximum_flow_problem", LpMaximize)

# Goal function
goal_function: List = []
for x in var.keys(): 
    if x[0] == source:
        goal_function.append(var[x])

model += lpSum(goal_function)

# Constrains
constrains_o: List = []
constrains_d: List = []

for node in nodes:
    for x in var.keys():
        
        if node == x[0]:
            constrains_o.append(var[x])
        elif node == x[1]:
            constrains_d.append(var[x])
        else:
            continue

    if node == destination or node == source:
        None
    else:
        model += lpSum(constrains_o) - lpSum(constrains_d) == 0
    
    constrains_o: List = []
    constrains_d: List = []

for x in var.keys():
    model += var[x] <= availabilities[x[0]][x[1]]

print(model)
    
# Model solution
status: int = model.solve()

# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')
print(f'A quantidade total é de {round(value(model.objective), 2)}')
print(" ")
for x in var.values():
    print(f'{x} = {value(x)}')













