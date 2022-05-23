#!/usr/bin/python3
"""
    Realizar un programa en python que reciba por argumentos:
        -p cantidad_procesos

        -f /ruta/al/archivo_matriz.txt

        -c funcion_calculo

    El programa deberá leer una matriz almacenada en el archivo de texto 
    pasado por argumento -f, y deberá calcular la funcion_calculo para 
    cada uno de sus elementos.

    Para aumentar la performance, el programa utilizará un Pool de 
    procesos, y cada proceso del pool realizará los cálculos sobre 
    una de las filas de la matriz.

    La funcion_calculo podrá ser una de las siguientes:
        raiz: calcula la raíz cuadrada del elemento.
        pot: calcula la potencia del elemento elevado a si mismo.
        log: calcula el logaritmo decimal de cada elemento.
    
    Ejemplo de uso:
        Suponiendo que el archivo /tmp/matriz.txt tenga este contenido:

            1, 2, 3
            4, 5, 6

        python3 calculo_matriz -f /tmp/matriz.txt -p 4 -c pot
            1, 4, 9
            16, 25, 36
"""
from multiprocessing import get_context
import argparse, math

def raiz(fila):
    matriz = []
    for x in fila:
        if x.isnumeric():
            a = math.sqrt(int(x))
            matriz.append(a) 

    matriz.append("\n")
    return matriz[0:len(matriz)-1]
    
def pot(fila):
    matriz = []
    for x in fila:
        if x.isnumeric():
            a = int(x) * int(x)      # No sabia si quería x^2 o x^x, en el ejemplo usa x^2.
            matriz.append(a) 

    matriz.append("\n")
    return matriz[0:len(matriz)-1]
    
def log(fila):
    matriz = []
    for x in fila:
        if x.isnumeric():
            a = math.log(int(x))
            matriz.append(a) 

    matriz.append("\n")
    return matriz[0:len(matriz)-1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, help="Cantidad de procesos.",  required=True)
    parser.add_argument("-f", type=str, help= "Ruta al archivo que contiene la matriz.", required=True)
    parser.add_argument("-c", type=str, help="Funcion de calculo.",  required=True)
    args = parser.parse_args()

    try:
        archivo = open(args.f, "r")
        filas = archivo.readlines()
        archivo.close()
    except FileNotFoundError:
        print("No se pudo abrir el archivo.")
        exit()

    pool = get_context("fork").Pool(args.p)

    if args.c == "raiz":
        matriz = pool.map(raiz, filas)
    elif args.c == "pot":
        matriz = pool.map(pot, filas)
    elif args.c == "log":
        matriz = pool.map(log, filas)
    else:
        matriz = "La funcion de calculo ingresada no es valida."

    for fila in matriz:
        for valor in fila:
            print("\t", str(valor)[0:5], end=" ")
        print()

if __name__=="__main__":
    main()