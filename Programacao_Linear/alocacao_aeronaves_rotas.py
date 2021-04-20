from typing import Dict, List

from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value

# Problem data
aircraft_type: List = [0, 1, 2]
routes: List = [0, 1, 2, 3]

passenger_capacity: Dict = {0: 50, 1: 30, 2: 20}
aircraft_availability: Dict = {0: 5, 1: 8, 2: 10}
route_demand: Dict = {0: 100, 1: 200, 2: 90, 3: 120}
total_travels: List = [[3, 2, 2, 1],
                       [4, 3, 3, 2],
                       [5, 5, 4, 2]]

operational_costs = [[1000, 1100, 1200, 1100],
                     [800, 900, 1000, 1000],
                     [600, 800, 800, 1000]]

# Model and Decision Variables
model = LpProblem('Routing_problem', LpMinimize)
var = LpVariable.dict("aircraft", (aircraft_type, routes), lowBound=0, cat='Integer')

# Goal Function
model += lpSum(var[(x, y)] * operational_costs[x][y] for x, y in var.keys())

# Constrains
for y in route_demand.keys():
    """ Soma as capacidades das aeronaves nas rotas e limita em relacao a demanda """
    model += lpSum(passenger_capacity[x] * var[(x, y)] for x in passenger_capacity) >= route_demand[y]

for i in aircraft_type:
    """ Soma o numero de viagens/rota e restringe em relacao a disponibilidade de aeronaves """
    model += lpSum(var[(i, y)] * (1/total_travels[i][y]) for y in routes) <= aircraft_availability[i]


print(model)

# Solving problem
status: int = model.solve()

# Printing results
print(f" *** Best configuration - {LpStatus[status]} *** ")
print('-------------------------------------')
print(f'Cost: ${value(model.objective)}')

for x in var.values():
    print(f'{x} = {value(x)}')