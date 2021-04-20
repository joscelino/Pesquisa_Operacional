from typing import Dict, List

from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value

""" Problema retirado do livro: Otimizacao combinatoria e meta-heuristica pag: 20-22"""

# Problem data
cutting_possibilities: List = [0, 1, 2]
cutting_list: Dict = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9}
scrap: List = [1910, 1910, 2440, 1630, 1090, 1171, 1171, 2594, 1171]
cutting_patterns: List = [[4, 0, 0],
                          [0, 9, 0],
                          [0, 3, 15],
                          [2, 3, 5],
                          [2, 0, 15],
                          [0, 1, 21],
                          [1, 3, 11],
                          [0, 5, 9],
                          [0, 7, 6]]
orders = [20, 17, 22]

# Model and Decision Variables
model = LpProblem('Cutting_problem', LpMinimize)
var = LpVariable.dict('Plate', (cutting_possibilities, cutting_list), lowBound=0, cat='Integer')

# Goal Function
model += lpSum(var[(i, x)] * scrap[x] for i, x in var.keys())

# Constrains
for i in cutting_possibilities:
    model += lpSum(var[(i, x)] * cutting_patterns[x][i] for x in cutting_list.keys()) >= orders[i]

# Solving problem
status: int = model.solve()

# Printing results
print(model)
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')

for x in var.values():
    if value(x) != 0:
        print(f'{x.name} = {value(x)} ')
    else:
        continue
print('-------------------------------------\n')