from typing import Dict, List

from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value

# Problem data
machines: List = [0, 1, 2]

fixed_cost: Dict = {0: 25, 1: 45, 2: 60}

variable_cost: Dict = {0: 4, 1: 7, 2: 12}

availability: Dict = {0: 30, 1: 60, 2: 78}

# Decision variables
var_1 = LpVariable.dict("X", machines, cat="Integer", lowBound=0)
var_2 = LpVariable.dict("Y", machines, cat="Binary")

# Model
model = LpProblem("fixed_load", LpMinimize)

# Goal function
model += lpSum(var_1[i] * variable_cost[i] + var_2[i] * fixed_cost[i] for i in machines)

# Constrains
for i in machines:
    model += var_1[i] <= availability[i] * var_2[i]

model += lpSum(x for x in var_1.values()) == 75

print(model)
# Model solution
status: int = model.solve()

print(f" *** Best configuration - {LpStatus[status]} *** ")
print("-------------------------------------")
print(f"The cost is: {round(value(model.objective), 2)}")
print(" ")

for i in machines:
    print(f"{var_1[i]} = {value(var_1[i])}")
    print(f"{var_2[i]} = {value(var_2[i])}")
