from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMaximize, value

# Problem data
capital = 1000000
investments = [0, 1, 2, 3, 4]


interest = {0: 0.020,
            1: 0.030,
            2: 0.025,
            3: 0.032,
            4: 0.005}

risk = {0: 0.03,
        1: 0.08,
        2: 0.10,
        3: 0.13,
        4: 0.01}

# Decision variables
var = LpVariable.dict("E", investments, lowBound=75000, upBound=500000.00)

# Model
model = LpProblem("Investment_problem", LpMaximize)

# Goal function
model += lpSum(interest[x] * (1 - risk[x]) * var[x] for x in var.keys())

# Constrains
constrains_list = []

for x in var.values():
    constrains_list.append(x)
    
model += lpSum(constrains_list) <= capital
print(model)

# Model solution
status: int = model.solve()
print(LpStatus[status])

# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')
print(f'Profit: ${value(model.objective)}')

for x in var.values():
    print(f'{x} = {value(x)}')

























