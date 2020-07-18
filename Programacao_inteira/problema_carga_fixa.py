from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMinimize, value
from typing import List, Dict

# Problem data
machines: List = [0, 1, 2]

fixed_cost: Dict = {0: 25,
                    1: 45,
                    2: 60}

variable_cost: Dict = {0: 4,
                       1: 7,
                       2: 12}

availability: Dict = {0: 30,
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
status: int = model.solve()
print(LpStatus[status])
print(" ")
print(f'The cost is: {round(value(model.objective), 2)}')
print(" ")

for i in machines:
    print(f'{var[i]} = {value(var[i])}')
    print(f'{var2[i]} = {value(var2[i])}')





















