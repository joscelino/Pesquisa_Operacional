from typing import Dict, List

from pulp import LpMaximize, LpProblem, LpStatus, LpVariable, lpSum, value

# Problem data
items: List = ["MS1", "MS2", "MS3", "MS4", "MS5", "MS6"]

availability: int = 20000
weight: Dict = {
    "MS1": 7000,
    "MS2": 4500,
    "MS3": 8700,
    "MS4": 8000,
    "MS5": 4900,
    "MS6": 7500,
}

item_value: Dict = {"MS1": 36, "MS2": 64, "MS3": 40, "MS4": 45, "MS5": 60, "MS6": 40}

# Decision variables
var = LpVariable.dict("", items, cat="Binary")

# Model
model = LpProblem("Backpack_problem", LpMaximize)

# Goal function
model += lpSum(var[item] * item_value[item] for item in items)

# Constrains
model += lpSum(var[item] * weight[item] for item in items) <= availability

# Model solution
print(model)
status: int = model.solve()
print(LpStatus[status])
print(f"Objective value: {value(model.objective)}")
print(" ")

for x in var.values():
    print(f"{x} = {round(value(x), 2)}")
