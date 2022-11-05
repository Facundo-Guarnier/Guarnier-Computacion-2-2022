"""
    Realizar un programa en python que reciba por argumentos:
        -f /ruta/al/archivo_matriz.txt
        -c funcion_calculo
        
    El programa deberá leer una matriz almacenada en el archivo de texto pasado por argumento -f, y deberá 
    calcular la funcion_calculo para cada uno de sus elementos.

    Para aumentar la performance, el programa utilizará un Celery, que recibirá mediante una cola de 
    mensajes Redis, cada una de las tareas a ejecutar.

    La funcion_calculo, modelada como tareas de Celery, podrá ser una de las siguientes:
        raiz: calcula la raíz cuadrada del elemento.
        pot: calcula la potencia del elemento elevado a si mismo.
        log: calcula el logaritmo decimal de cada elemento.
"""

# docker run --rm -p 6379:6379 redis       ->  Redis, cola de mensaje, BD
# celery -A celery_task worker --loglevel=INFO -c4       -> Celery, toma las tarea en cola y las trabaja, se puede sincronizar con otros celerys para mayor disponibilidad ($ sync with celery@mr-arch)
# pip install redis
# Con .delay() me permite seguir ejecutando el codigo, a pesar que el resultado no esté. No hay que esperar.
# Con el .get() obtengo el resultado. Si éste aun no está disponible, me quedo esperandolo (no sigue la ejecucion)

import argparse, time
from celery_task import funcion_calculo

def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", required=True, help="direccion del archivo")
    parser.add_argument("-c", required=True, help="funcion de calculo", choices=["pot", "raiz", "log"])
    return parser.parse_args()

def archivo(f):
    try:
        archivo = open(f, "r")
        filas = archivo.readlines()
        archivo.close()
        return filas
    except FileNotFoundError:
        print("No se pudo abrir el archivo.")
        exit()

def imprimir_matriz(matriz):
    for fila in matriz:
        for valor in fila:
            print("\t", str(valor)[0:5], end=" ")
        print()

def main():
    args = argumentos()
    
    filas = archivo(args.f)
        
    matriz = []
    for x in filas:
        x = x[:-1]
        lista_fila = x.split(",")
        matriz.append(lista_fila)

    try:        
        imprimir_matriz(matriz)
        resultado = funcion_calculo(args.c, matriz)
        imprimir_matriz(resultado.get())
    except:
        print("Matriz invalida")
    
if __name__ == '__main__':
    main()
    
    # docker run --rm -p 6379:6379 redis
    # celery -A celery_confg worker --loglevel=INFO -c4
    # python3 app.py -f /tmp/matriz.txt -c raiz