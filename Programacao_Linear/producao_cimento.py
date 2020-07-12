from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMaximize, value
import numpy as np

# Problem data
product_manufactured = {0: 'CP320', 1: 'AF250'}
product_sales = {0: 'CP320', 1: 'AF250', 2: 'clinker'}
components = {0: 'clinker', 1: 'slag', 2: 'plaster', 3: 'additive'}
composition = [[0.85, 0.50],
               [0.07, 0.45],
               [0.03, 0.03],
               [0.05, 0.02]]
limit_manufacture = 1100000
clinker_sales = 200000
slag_orders = 180000
plaster_orders = 50000
margin = np.array([41.00, 37.80, 34.40])
slag_price = 22.10
plaster_price = 34.20
additive_price = 1.90

# Model and variables
model = LpProblem('Cement_production', LpMaximize)
var = LpVariable.dict("Product_sale", product_sales, lowBound=0, cat='Integer')

# Goal function
model += lpSum(var[x] * margin[x] for x in product_sales) - slag_price * \
         lpSum((var[x] * composition[1][x] for x in product_manufactured)) - margin[2] * \
         lpSum((var[x] * composition[2][x] for x in product_manufactured)) - additive_price * \
         lpSum((var[x] * composition[3][x] for x in product_manufactured))

# Constrains
model += var[0] + var[1] <= limit_manufacture
print(model)