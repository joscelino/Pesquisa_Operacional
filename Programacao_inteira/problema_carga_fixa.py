from pulp import *

#Dados do problema
maquinas = [0,1,2]

fixo = {0:25,
        1:45,
        2:60}

variavel = {0:4,
            1:7,
            2:12}

capacidade ={ 0: 30,
             1:60,
             2:78}

#Criação das variáveis de decisão
var = LpVariable.dict("X",(maquinas),cat = 'Integer',lowBound = 0)
var2 = LpVariable.dict("Y",(maquinas),cat = 'Binary')

#Criação do model

model = LpProblem("Carga_Fixa",LpMinimize)
#Criação da função objetivo
lista_fo = []

for i in maquinas:
    lista_fo.append(var[i]*variavel[i] + var2[i]*fixo[i])

model+= lpSum(lista_fo)

#Criação das restrições

for i in maquinas:
    model += var[i] <= capacidade[i]*var2[i]
    
lista_rest = []
for x in var.values():
    lista_rest.append(x)
    
model += lpSum(lista_rest) == 75
    
#Solução do modelo

status = model.solve()
print(LpStatus[status])
print(" ")
print(f'O custo é de {value(model.objective)}')
print(" ")

for i in maquinas:
    print(f'{var[i]} = {value(var[i])}')
    print(f'{var2[i]} = {value(var2[i])}')





















