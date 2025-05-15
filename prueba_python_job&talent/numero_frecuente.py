
def numero_mas_frecuente(lista):
    
    contar = {}
    
    for num in lista:
        contar[num] = contar.get(num,0)+1
    mas = max(contar.values())
    opcionados= [num for num in contar if contar[num] == mas]
    
    return min(opcionados)
print(numero_mas_frecuente([1,1,1,3,3,3,4,5,6,7,8,9]))

        
