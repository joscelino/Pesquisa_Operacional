from pulp import LpVariable, LpProblem, lpSum, LpStatus, LpMaximize, value

# Dados do Problema
tempos =[[2,5,5,0,0],
         [5,5,0,2,2],
         [6,7,0,10,2],
         [0,0,4,2,0],
         [0,1,7,0,0],
         [0,0,3,0,4],
         [0,5,2,0,4],
         [0,0,10,0,1],
         [0,4,3,8,0],
         [3,0,0,0,3]]

produto = [0,1,2,3,4,5,6,7,8,9]

maximo = {0:300.5,
            1:200.5,
            2:150,
            3:180,
            4:220,
            5:200.5,
            6:160,
            7:300,
            8:150,
            9:200}

lucro =  {0:1.2,
            1:2.3,
            2:3.4,
            3:2,
            4:3,
            5:1.9,
            6:0.6,
            7:1,
            8:2,
            9:3}

capacidades = {0:4000,
               1:5000,
               2:3000,
               3:7000,
               4:2500}

volume_total = 1000


#Criação das variáveis de decisão
var = LpVariable.dict("C", produto,lowBound = 0)

#Criação do modelo
model = LpProblem("Problema_mix_produção",LpMaximize)
#Criação da função objetivo
lista_fo = []

for x in produto:
    lista_fo.append(var[x]*lucro[x])

model += lpSum(lista_fo)

# Criação das restrições
lista_rest = []
for i in capacidades.keys():
    for j in produto:
        if tempos[j][i]!=0:
            lista_rest.append(var[j]*tempos[j][i])
        else:
            None
    model+= lpSum(lista_rest)<= capacidades[i]
    lista_rest = []

for x in var.keys():
    model += var[x] <= maximo[x]
    

for x in var.values():
    lista_rest.append(x)

model+= lpSum(lista_rest) <= volume_total

print(model)
#Solução do modelo

status = model.solve()
print(LpStatus[status])
print(f'Lucro = R${value(model.objective)}')


for x in var.values():
    if value(x) != 0:
        print(f'{x} = {value(x)}')

























