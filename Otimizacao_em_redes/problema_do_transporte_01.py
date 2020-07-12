# Importando o Pulp
from pulp import *

# Dados do Problema
fabricas = [0,1]
mercados = [0,1,2,3,4,5]

custos = [[3.69,3,3.06,4.35,2.59,2.44],
          [0.3,2.33,0.85,0.46,4.37,3.77]]

capacidade = {0:5000,
              1:3000}

demandas = {0:1000,
            1:1300,
            2:900,
            3:880,
            4:780,
            5:2000}


# Criação das variáveis de decisão
var = LpVariable.dict("x",(fabricas,mercados),lowBound =0,cat = 'Integer')
# Criação do modelo
model = LpProblem("Problema_do_Transporte",LpMinimize)
# Criação da fo
lista_fo = []

for x in var.keys():
    lista_fo.append(var[x]*custos[x[0]][x[1]])

model += lpSum(lista_fo)

# Criação das restrições
lista_rest = []

for f in fabricas:
    for m in mercados:
        lista_rest.append(var[(f,m)])
    model += lpSum(lista_rest) <= capacidade[f]
    lista_rest = []

for m in mercados:
    for f in fabricas:
        lista_rest.append(var[(f,m)])
    model += lpSum(lista_rest) >= demandas[m]
    lista_rest = []
    
print(model)

# Solução do modelo

status = model.solve()
print(LpStatus[status])
print(f'O custo de transporte foi de R${value(model.objective)}')
print(" ")

for x in var.values():
    if value(x) != 0:
        print(f'{x} = {value(x)}')
    else:
        continue



