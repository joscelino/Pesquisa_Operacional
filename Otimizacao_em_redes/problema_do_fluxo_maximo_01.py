from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMaximize, value

# Problem data
nodes = [0, 1, 2, 3, 4]
source = 0
destination = 4

fork = [[0, 1, 1, 1, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0]]

availabilities = [[0, 200, 300, 100, 0],
                  [0, 0, 400, 0, 300],
                  [0, 0, 0, 100, 200],
                  [0, 0, 50, 0, 200],
                  [0, 0, 0, 0, 0]]

# Decision variables
var = {}
for i in nodes:
    for j in nodes:
        if fork[i][j]==1:
            var[(i,j)]= LpVariable(name=f'x{i}{j}', lowBound=0, cat='Integer')
        else:
            continue
    var.update(var)

# Model
model = LpProblem("Maximum_flow_problem", LpMaximize)

# Goal function
goal_function = []
for x in var.keys(): 
    if x[0] == source:
        goal_function.append(var[x])

model += lpSum(goal_function)

# Constrains
constrains_o = []
constrains_d = []

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
    
    constrains_o = []
    constrains_d = []

for x in var.keys():
    model += var[x] <= availabilities[x[0]][x[1]]

print(model)
    
# Model solution
status = model.solve()

# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')
print(f'A quantidade total é de {value(model.objective)}')
print(" ")
for x in var.values():
    print(f'{x} = {value(x)}')













