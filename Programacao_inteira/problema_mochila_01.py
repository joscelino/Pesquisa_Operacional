# importar o pulp
from pulp import *

# Criar dados do problema

itens = ['MS1','MS2','MS3','MS4','MS5','MS6']

capacidade = 20000
peso = {'MS1':7000,
        'MS2':4500,
        'MS3':8700,
        'MS4':8000,
        'MS5':4900,
        'MS6':7500}

valor ={'MS1':36,
        'MS2':64,
        'MS3':40,
        'MS4':45,
        'MS5':60,
        'MS6':40}

# Criar as variáveis de decisão
var = LpVariable.dict("",(itens),cat = 'Binary')

# Criar o Problema
model = LpProblem("Problema_mochila_01",LpMaximize)
# Criar fo
lista_fo =[]

for item in itens:
    lista_fo.append(var[item] * valor[item])

model += lpSum(lista_fo)


# Criar restrições
lista_rest = []

for item in itens:
    lista_rest.append(var[item]*peso[item])
    
model += lpSum(lista_rest) <= capacidade

# Solução do modelo
print(model)
status = model.solve()
print(LpStatus[status])
print(f'O valor total da fo é {value(model.objective)}')
print(" ")

for x in var.values():
    print(f'{x} = {value(x)}')
