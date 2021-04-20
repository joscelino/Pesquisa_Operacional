from typing import Dict, List

from pulp import LpMaximize, LpProblem, LpStatus, LpVariable, lpSum, value

# Problem data
cycle_time: List = [[2, 5, 5, 0, 0],
                    [5, 5, 0, 2, 2],
                    [6, 7, 0, 10, 2],
                    [0, 0, 4, 2, 0],
                    [0, 1, 7, 0, 0],
                    [0, 0, 3, 0, 4],
                    [0, 5, 2, 0, 4],
                    [0, 0, 10, 0, 1],
                    [0, 4, 3, 8, 0],
                    [3, 0, 0, 0, 3]]

product: List = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

max_limit: Dict = {0: 300.5,
                   1: 200.5,
                   2: 150,
                   3: 180,
                   4: 220,
                   5: 200.5,
                   6: 160,
                   7: 300,
                   8: 150,
                   9: 200}

profit: Dict = {0: 1.2,
                1: 2.3,
                2: 3.4,
                3: 2,
                4: 3,
                5: 1.9,
                6: 0.6,
                7: 1,
                8: 2,
                9: 3}

availabilities: Dict = {0: 4000,
                        1: 5000,
                        2: 3000,
                        3: 7000,
                        4: 2500}

total_volume: int = 1000


# Decision variable
var = LpVariable.dict("P", product, lowBound=0)

# Model
model = LpProblem("Manufacturing_problem_mix", LpMaximize)

# Goal function
model += lpSum(var[x] * profit[x] for x in product)

# Constrains
constrains_list: List = []

for i in availabilities.keys():
    for j in product:
        if cycle_time[j][i] != 0:
            constrains_list.append(var[j] * cycle_time[j][i])
        else:
            None
    model += lpSum(constrains_list) <= availabilities[i]
    constrains_list = []

for x in var.keys():
    model += var[x] <= max_limit[x]

for x in var.values():
    constrains_list.append(x)

model += lpSum(constrains_list) <= total_volume

print(model)

# Model solution
status: int = model.solve()
print(LpStatus[status])
print(f'Profit = R${value(model.objective)}')

# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')
for x in var.values():
    if value(x) != 0:
        print(f'{x} = {value(x)}')
