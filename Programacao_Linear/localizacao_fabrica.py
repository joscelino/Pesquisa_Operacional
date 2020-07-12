from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMinimize, value
import numpy as np

# Problem Data
cities = {0: 'Niteroi', 1: 'Angra', 2: 'Campos'}
terminals = {0: 'Terminal_1', 1: 'Terminal_1', 2: 'Terminal_1', 3: 'Terminal_1'}
availabilities = np.array([1500, 2600, 3400])
weekly_manufacture = np.array([800, 1200, 650, 1450])
fixed_costs = np.array([300000, 400000, 490000])
variable_costs = ([40, 15, 20],
                  [10, 12, 25],
                  [30, 17, 27],
                  [10, 12, 20])
annual_weeks = 52

# Model and variables
model = LpProblem('Mix_cakes', LpMinimize)
var_1 = LpVariable.dict("Cities", cities, lowBound=0, cat='Binary')
var_2 = LpVariable.dict("Location", (terminals, cities), lowBound=0, cat='Integer')

# Goal function
model += lpSum(variable_costs[x][i] * var_2[(x, i)] for x, i in var_2) * annual_weeks \
         + lpSum(var_1[y] * fixed_costs[y] for y in cities)

# Constrains
model += lpSum(var_2[(0, 0)] + var_2[(0, 1)] + var_2[(0, 2)]) == weekly_manufacture[0]
model += lpSum(var_2[(1, 0)] + var_2[(1, 1)] + var_2[(1, 2)]) == weekly_manufacture[1]
model += lpSum(var_2[(2, 0)] + var_2[(2, 1)] + var_2[(2, 2)]) == weekly_manufacture[2]
model += lpSum(var_2[(3, 0)] + var_2[(3, 1)] + var_2[(3, 2)]) == weekly_manufacture[3]

model += lpSum(var_2[(0, 0)] + var_2[(1, 0)] + var_2[(2, 0)] + var_2[(3, 0)]) <= availabilities[0]
model += lpSum(var_2[(0, 1)] + var_2[(1, 1)] + var_2[(2, 1)] + var_2[(3, 1)]) <= availabilities[1]
model += lpSum(var_2[(0, 2)] + var_2[(1, 2)] + var_2[(2, 2)] + var_2[(3, 2)]) <= availabilities[2]

print(model)

# Solving problem
status = model.solve()
print(LpStatus[status])

# Printing results
print(" *** Best configuration *** ")
print('-------------------------------------')

for x in var_2.values():
    if value(x) != 0:
        print(f'{x.name} = {value(x)}')

print('-------------------------------------')
print(f'Cost {LpStatus[status]} = R$ {round(value(model.objective), 2)}')
