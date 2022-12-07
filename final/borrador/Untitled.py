# import pandas as pd

# def matriz_inicial():
#     matriz = []
#     for y in range(10):     #Filas
#         matriz.append([])
#         for x in range(10): #Columnas
#             matriz[y].append(" ")
#     return pd.DataFrame(matriz, index = ["A","B","C","D","E","F","G","H","I","J"])


# matriz = matriz_inicial()

# codificacion = str.maketrans(
#         'ABCDEFGHIJ',
#         "0123456789",
#         )

# msg1 = "A9"

# fila = msg1[0].translate(codificacion)
# columna = msg1[1]

# # print(fila, columna)


# tablero = {"disparos_enemigos": matriz, "mis_barcos": matriz}

# matriz.iloc[int(fila), int(columna)]="aaaa"
# # print(matriz)
# print(matriz.iloc[int(fila), int(columna)])

# import random
# i = 0
# while True:
#     n = random.randint(0, 9)
#     if n == 0:
#         print(i, n)
#         break
#     i += 1


a = ["a", "b"]
b = ["c"]

print(["c"]+ a)