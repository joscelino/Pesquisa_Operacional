from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMaximize, value

# Problem data
#           b1  b2 b3
reward = [[30, -10, -30],   # Very Hard A
          [0, -40, 10],     # Average A
          [-50, 60, 0]]     # Light strategy A

strategy_A = [0, 1, 2]
strategy_B = [0, 1, 2]

# Decision variables
var = LpVariable.dict("A", strategy_A, lowBound=0)
v = LpVariable('v')

# Model
model = LpProblem("zero_sum_game", LpMaximize)

# Goal function
model += v

# Constrains
constrains_list = []

for j in strategy_B:
    for i in strategy_A:
        constrains_list.append(var[i] * reward[i][j])
    model += v - lpSum(constrains_list) == 0
    constrains_list = []


for x in var.values():
    constrains_list.append(x)
    
model += lpSum(constrains_list) == 1

# Model solution
print(model)

status = model.solve()
print(LpStatus[status])
print(f'Game value: {value(model.objective)}')

for x in var.values():
    print(f'{x} = {value(x)}')















