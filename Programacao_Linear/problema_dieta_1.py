from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMinimize, value

# Problem Data
feed = [0, 1, 2, 3, 4, 5]

costs = {0: 0.74,
         1: 0.70,
         2: 0.83,
         3: 0.81,
         4: 0.73,
         5: 0.75}


minimum = {0: 200,  # Carbohydrate
           1: 180,  # Protein
           2: 150}  # Vitamin


inf_nutri = [[50, 60, 30, 0, 20, 45],
             [27, 0, 40.5, 20, 30, 50],
             [50, 80, 60, 30, 20, 40]]

# Model and Decision Variables
model = LpProblem("Diet_problem", LpMinimize)
var = LpVariable.dict("R", feed, lowBound=0, cat='Integer')

# Goal function
model += lpSum(var[x] * costs[x] for x in var.keys())

# Constrains
list_rest = []
for i in minimum.keys():
    for j in feed:
        list_rest.append(var[j] * inf_nutri[i][j])
    model += lpSum(list_rest) >= minimum[i]
    list_rest = []
    
print(model)

# Solving problem
status = model.solve()
print(LpStatus[status])

print(" ")

# Printing results
print(" *** Best configuration *** ")
print('-------------------------------------')
for x in var.values():
    if value(x) != 0:
        print(f'{x.name} = {value(x)} ')
    else:
        continue
print('-------------------------------------')
print(f'The {LpStatus[status]} cost is: R$ {round(value(model.objective), 2)}')
