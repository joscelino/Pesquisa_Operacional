from pulp import *

# Dados do problema
capital = 1000000
investimentos = [0,1,2,3,4]


juros = {0:0.020,
         1:0.030,
         2:0.025,
         3:0.032,
         4:0.005}

risco = {0:0.03,
         1:0.08,
         2:0.10,
         3:0.13,
         4:0.01}

# Criar as var_decisão
var = LpVariable.dict("E",(investimentos),lowBound = 70000,upBound = 599999.99)

# Criar o modelo
model = LpProblem("Problema_investimento",LpMaximize)
#criar a função objetivo
lista_fo = []

for x in var.keys():
    lista_fo.append(juros[x]*(1-risco[x])*var[x])

model += lpSum(lista_fo)


#criar as restrições
lista_rest = []

for x in var.values():
    lista_rest.append(x)
    
model += lpSum(lista_rest) <= capital
print(model)
#Solução do modelo
status = model.solve()
print(LpStatus[status])
print (f'O lucro foi de R${value(model.objective)}')
print(" ")

for x in var.values():
    print(f'{x} = {value(x)}')

























