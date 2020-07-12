from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMaximize, value
import numpy as np

# Problem Data
product = {0: 'Cream_cake', 1: 'Chocolate_cake'}
profits = {0: 1, 1: 3}
demand = np.array([40, 60])
cycle_time = np.array([3, 2])
deal_chocolate = 10
min_lot = 20
machine_hour = 180

# Model and variables
model = LpProblem('Mix_cakes', LpMaximize)
var = LpVariable.dict("Cake", product, lowBound=0, cat='Integer')

# Objective function
model += lpSum([profits[i] * var[i] for i in product])

# Constrains
# Time
model += lpSum(cycle_time[i] * var[i] for i in product) <= machine_hour

# Quantities
model += lpSum(var[0]) <= demand[0]
model += lpSum(var[1]) <= demand[1]

# Deals and manufacture
model += lpSum(var[0] + var[1]) >= min_lot
model += lpSum(var[1]) >= deal_chocolate

# Final model
print(model)

# Solving problem
status = model.solve()
print(LpStatus[status])

# Printing results
for x in var.values():
    if value(x) != 0:
        print(f'{x.name} = {value(x)}')

print('-------------------------------------')
print(f'Profit = R${round(value(model.objective), 2)}')
