from typing import Dict

import numpy as np
from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value

# Problem Data
cities: Dict = {0: 'Niteroi', 1: 'Angra', 2: 'Campos', }
terminals: Dict = {0: 'Terminal_1', 1: 'Terminal_1', 2: 'Terminal_1', 3: 'Terminal_1', }
availabilities: object = np.array([1500, 2600, 3400, ])
weekly_manufacture: object = np.array([800, 1200, 650, 1450, ])
fixed_costs = np.array([300000, 400000, 490000, ])
variable_costs: object = ([40, 15, 20],
                          [10, 12, 25],
                          [30, 17, 27],
                          [10, 12, 20],)
annual_weeks: int = 52

# Model and variables
model = LpProblem('Terminal_location', LpMinimize)
var_1 = LpVariable.dict("Cities", cities, lowBound=0, cat='Binary')
var_2 = LpVariable.dict("Location", (terminals, cities), lowBound=0, cat='Integer')

# Goal function
model += lpSum(variable_costs[x][i] * var_2[(x, i)] for x, i in var_2) * annual_weeks \
         + lpSum(var_1[y] * fixed_costs[y] for y in cities)

# Constrains
for i in terminals:
    model += lpSum(var_2[(i, x)] for x in cities) == weekly_manufacture[i]

for x in cities:
    model += lpSum(var_2[(i, x)] for i in terminals) <= availabilities[x]

print(model)

# Solving problem
status: int = model.solve()
print(LpStatus[status])

# Printing results
print(" *** Best configuration *** ")
print('-------------------------------------')

for x in var_2.values():
    if value(x) != 0:
        print(f'{x.name} = {value(x)}')

print('-------------------------------------')
print(f'Cost {LpStatus[status]} = R$ {round(value(model.objective), 2)}')
