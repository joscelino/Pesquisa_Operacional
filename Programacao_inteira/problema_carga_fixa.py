from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMinimize, value

# Problem data
machines = [0, 1, 2]

fixed_cost = {0: 25,
              1: 45,
              2: 60}

variable_cost = {0: 4,
                 1: 7,
                 2: 12}

availability = {0: 30,
                1: 60,
                2: 78}

# Decision variables
var = LpVariable.dict("X", machines, cat='Integer', lowBound=0)
var2 = LpVariable.dict("Y", machines, cat='Binary')

# Model
model = LpProblem("fixed_load", LpMinimize)

# Goal function
model += lpSum(var[i] * variable_cost[i] + var2[i] * fixed_cost[i] for i in machines)

# Constrains
for i in machines:
    model += var[i] <= availability[i] * var2[i]
    
constrains_list = []
for x in var.values():
    constrains_list.append(x)
    
model += lpSum(constrains_list) == 75
    
# Model solution
status = model.solve()
print(LpStatus[status])
print(" ")
print(f'The cost is: {value(model.objective)}')
print(" ")

for i in machines:
    print(f'{var[i]} = {value(var[i])}')
    print(f'{var2[i]} = {value(var2[i])}')





















