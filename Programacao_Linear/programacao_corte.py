from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMinimize, value
from typing import List, Dict

# Problem data
cutting_possibilities: Dict = {0: 'plate_1', 1: 'plate_2'}
plate_length: List = [0.8, 1.5]
orders: List = [1, 2, 3]
width_dimensions: Dict = {1: 0.4, 2: 0.6, 3: 0.7}

plate_1: List = [[2, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]]

plate_2: List = [[3, 2, 2, 1, 0, 0],
                 [0, 1, 0, 1, 1, 0],
                 [0, 0, 1, 0, 1, 2]]

loss_plate_1: Dict = {1: 0, 2: 0.4, 3: 0.3}
loss_plate_2: Dict = {1: 0.3, 2: 0.1, 3: 0, 4: 0.5, 5: 0.2, 6: 0.1}

width_plate_1: List = [1, 2, 3]
width_plate_2: List = [1, 2, 3, 4, 5, 6]

required_length: List = [10, 30, 20]
scraps_k: List = [1, 2, 3]

# Model and Decision Variables
model = LpProblem('Cutting_problem', LpMinimize)
var_1 = LpVariable.dict("Cut_1", width_plate_1, lowBound=0, cat='Integer')
var_2 = LpVariable.dict("Cut_2", width_plate_2, lowBound=0, cat='Integer')
var_3 = LpVariable.dict('y', scraps_k, lowBound=0, cat='Integer')

# Goal function
model += lpSum(var_1[x] * loss_plate_1[x] for x in var_1.keys()) + \
         lpSum(var_2[x] * loss_plate_2[x] for x in var_2.keys()) + \
         lpSum(var_3[x] * width_dimensions[x] for x in var_3.keys())

# Constrains
model += lpSum(var_1[x+1] * plate_1[0][x] for x in range(0, len(width_plate_1), 1)) + \
         lpSum(var_2[x+1] * plate_2[0][x] for x in range(0, len(width_plate_2), 1)) - \
         var_3[1] == required_length[0]

model += lpSum(var_1[x+1] * plate_1[1][x] for x in range(0, len(width_plate_1), 1)) + \
         lpSum(var_2[x+1] * plate_2[1][x] for x in range(0, len(width_plate_2), 1)) - \
         var_3[2] == required_length[1]

model += lpSum(var_1[x+1] * plate_1[2][x] for x in range(0, len(width_plate_1), 1)) + \
         lpSum(var_2[x+1] * plate_2[2][x] for x in range(0, len(width_plate_2), 1)) - \
         var_3[3] == required_length[2]

print(model)

# Solving problem
status: int = model.solve()

# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')

for x in var_1.values():
    if value(x) != 0:
        print(f'{x.name} = {value(x)} ')
    else:
        continue
print('-------------------------------------\n')

for x in var_2.values():
    if value(x) != 0:
        print(f'{x.name} = {value(x)} ')
    else:
        continue

print('-------------------------------------\n')
for x in var_3.values():
    if value(x) != 0:
        print(f'{x.name} = {value(x)} ')
    else:
        print(f'{x.name} = {value(x)} ')

print('-------------------------------------')
print(f'The {LpStatus[status]} loss is: {round(value(model.objective), 2)}')
