from typing import Dict, List

from pulp import LpMaximize, LpProblem, LpStatus, LpVariable, lpSum, value

# Problem data
product_manufactured: Dict = {0: "CP320", 1: "AF250"}
product_sales: Dict = {0: "CP320", 1: "AF250", 2: "clinker"}
components: Dict = {0: "clinker", 1: "slag", 2: "plaster", 3: "additive"}
composition: List = [[0.85, 0.50], [0.07, 0.45], [0.03, 0.03], [0.05, 0.02]]
limit_manufacture: int = 1100000
clinker_sales: int = 200000
slag_orders: int = 180000
plaster_orders: int = 50000
margin: List = [41.00, 37.80, 34.40]
slag_price: float = 22.10
plaster_price: float = 34.20
additive_price: float = 1.90

# Model and variables
model = LpProblem("Cement_production", LpMaximize)
var = LpVariable.dict("Product_sale", product_sales, lowBound=0, cat="Integer")

# Goal function
model += (
    lpSum(var[x] * margin[x] for x in product_sales)
    - slag_price * lpSum((var[x] * composition[1][x] for x in product_manufactured))
    - margin[2] * lpSum((var[x] * composition[2][x] for x in product_manufactured))
    - additive_price * lpSum((var[x] * composition[3][x] for x in product_manufactured))
)

# Constrains
model += var[2] <= clinker_sales
model += lpSum(var[x] for x in product_manufactured) <= limit_manufacture
model += (
    lpSum(composition[0][x] * var[x] for x in product_manufactured) + var[2]
    <= limit_manufacture
)
model += lpSum(composition[1][x] * var[x] for x in product_manufactured) <= slag_orders
model += (
    lpSum(composition[2][x] * var[x] for x in product_manufactured) <= plaster_orders
)
model += (
    lpSum(composition[3][x] * var[x] for x in product_manufactured) <= plaster_orders
)

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
