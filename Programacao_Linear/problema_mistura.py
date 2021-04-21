from typing import Dict, List

import numpy as np
from pulp import LpMaximize, LpProblem, LpStatus, LpVariable, lpSum, value

# Problem Data
components: Dict = {0: "pure_gas", 1: "octane", 2: "additive"}
availabilities = np.array([9600000, 4800000, 2200000])
gas_types: Dict = {0: "green_gas", 1: "blue_gas", 2: "common_gas"}
composition: List = [[0.22, 0.50, 0.28], [0.52, 0.34, 0.14], [0.74, 0.20, 0.06]]
contribution_margin = np.array([0.30, 0.25, 0.20])
limit_blue_gas: int = 600000
min_common_gas: int = 16  # times more than green gas

# Model and variables
model = LpProblem("Mix_gas", LpMaximize)
var = LpVariable.dict("GAS", gas_types, lowBound=0, cat="Integer")

model += lpSum(var[x] * contribution_margin[x] for x in gas_types)

# Constrains
model += (
    lpSum(
        var[0] * composition[0][0]
        + var[1] * composition[1][0]
        + var[2] * composition[2][0]
    )
    <= availabilities[0]
)
model += (
    lpSum(
        var[0] * composition[0][1]
        + var[1] * composition[1][1]
        + var[2] * composition[2][1]
    )
    <= availabilities[1]
)
model += (
    lpSum(
        var[0] * composition[0][2]
        + var[1] * composition[1][2]
        + var[2] * composition[2][2]
    )
    <= availabilities[2]
)

model += lpSum(min_common_gas * (var[0])) - lpSum(var[2]) <= 0
model += lpSum(var[1]) <= limit_blue_gas

print(model)

# Solving problem
status: int = model.solve()

# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print("-------------------------------------")
for x in var.values():
    if value(x) != 0:
        print(f"{x.name} = {value(x)} ")
    else:
        continue
print("-------------------------------------")
print(f"The {LpStatus[status]} profit is: R$ {round(value(model.objective), 2)}")
