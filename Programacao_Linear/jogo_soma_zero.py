from pulp import *
#Dados do problema
#           b1  b2 b3
retorno = [[30,-10,-30], #Muito pesado A
           [0,-40,10],    # Médio A
           [-50,60,0]]  # Leve A

estrategiaA = [0,1,2]
estrategiaB = [0,1,2]

#Criação das variáveis de decisão
var = LpVariable.dict("A",(estrategiaA),lowBound=0)
v = LpVariable('v')
#Criação do modelo
model = LpProblem("Jogo_soma_zero",LpMaximize)
# Criação da função objetivo
model += v
#Criação das restrições
lista_rest = []

for j in estrategiaB:
    for i in estrategiaA:
        lista_rest.append(var[i]*retorno[i][j])
    model += v - lpSum(lista_rest) ==0
    lista_rest = []


for x in var.values():
    lista_rest.append(x)
    
model += lpSum(lista_rest) == 1
#Solução do modelo
print(model)

status = model.solve()
print(LpStatus[status])
print(f'O valor do jogo é {value(model.objective)}')

for x in var.values():
    print(f'{x} = {value(x)}')
















