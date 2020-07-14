from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMinimize, value

# Problem data
manufacturers = [0, 1]
markets = [0, 1, 2, 3, 4, 5]

costs = [[3.69, 3, 3.06, 4.35, 2.59, 2.44],
         [0.3, 2.33, 0.85, 0.46, 4.37, 3.77]]

availabilities = {0: 5000,
                  1: 3000}

demands = {0: 1000,
           1: 1300,
           2: 900,
           3: 880,
           4: 780,
           5: 2000}

# Decision variables
var = LpVariable.dict("x", (manufacturers, markets), lowBound=0, cat='Integer')

# Model
model = LpProblem("Transportation_problem", LpMinimize)

# Goal function
model += lpSum(var[x] * costs[x[0]][x[1]] for x in var.keys())

# Constrains
constrains_list = []

for f in manufacturers:
    for m in markets:
        constrains_list.append(var[(f, m)])
    model += lpSum(constrains_list) <= availabilities[f]
    constrains_list = []

for m in markets:
    for f in manufacturers:
        constrains_list.append(var[(f, m)])
    model += lpSum(constrains_list) >= demands[m]
    constrains_list = []
    
print(model)

# Model solution

status = model.solve()
print(LpStatus[status])

# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')
print(f'The transportation cost is $: {value(model.objective)}')
print(" ")

for x in var.values():
    if value(x) != 0:
        print(f'{x} = {value(x)}')
    else:
        continue



