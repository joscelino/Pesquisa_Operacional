from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMinimize, value


# Problem data
teams = [0, 1, 2, 3, 4]
jobs = [0, 1, 2, 3, 4]

costs = [[33, 22, 40, 21, 43],
         [27, 40, 55, 32, 26],
         [33, 38, 42, 49, 29],
         [36, 30, 52, 36, 34],
         [28, 45, 31, 42, 19]]

# Decision variables
var = LpVariable.dict("x", (teams, jobs), cat='Binary')

# Model
model = LpProblem('Designation_problem', LpMinimize)

# Goal function
model += lpSum(var[x] * costs[x[0]][x[1]] for x in var.keys())


# Constrains
constrains_list = []

for time in teams:
    for job in jobs:
        constrains_list.append(var[(time, job)])
    model += lpSum(constrains_list) == 1
    constrains_list = []

for job in jobs:
    for time in teams:
        constrains_list.append(var[(time, job)])
    model += lpSum(constrains_list) == 1
    constrains_list = []
    
print(model)

# Model solution
status = model.solve ()
print(LpStatus[status])

# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')
print(f'The goal function value is $: {value(model.objective)}')

for x in var.values():
    if value(x) == 1:
        print(f'{x} = {value(x)}')
    else:
        continue





