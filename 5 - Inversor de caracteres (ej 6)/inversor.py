#!/usr/bin/python3
"""
    Escriba un programa que abra un archvo de texto 
    pasado por argumento utilizando el modificador -f.

    El programa deberá generar tantos procesos hijos 
    como líneas tenga el archivo de texto.
    El programa deberá enviarle, vía pipes (os.pipe()), 
    cada línea del archivo a un hijo.
    Cada hijo deberá invertir el orden de las letras 
    de la línea recibida, y se lo enviará al proceso 
    padre nuevamente, también usando os.pipe().
    El proceso padre deberá esperar a que terminen todos 
    los hijos, y mostrará por pantalla las líneas 
    invertidas que recibió por pipe.

    Ejemplo:
        Contenido del archivo /tmp/texto.txt

        Hola Mundo
        que tal
        este es un archivo
        de ejemplo.

    Ejecución:
        python3 inversor.py -f /tmp/texto.txt
        ovihcra nu se etse
        .olpmeje ed
        lat euq
        odfilas aloH
"""

import argparse, os, sys


def hijo(i, texto, pw):
    fila = texto[i] 
    invertida = ""
    for a in range(len(fila)):
        invertida += fila[-1-a]

    with os.fdopen(pw, 'w') as w:
        w.write(invertida)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="Ruta del archivo.") 

    args = parser.parse_args()

    with open(args.f, 'r') as archivo:  #Se listan las filas del archivo
        texto = archivo.readlines()
        cant_filas = len(texto)

    pr,pw = os.pipe()                   #Creacion de la tuberia. 

    for i in range(cant_filas):         #Tantos hijo como filas en el archivo.
        id_hijo = os.fork()

        if id_hijo == 0:
            os.close(pr)                #Se cierra la lectura para el hijo
            hijo(i, texto, pw)
            sys.exit(0)                 #Muere el hijo

    os.close(pw)

    for i in range(cant_filas):
        os.wait()
    
    with os.fdopen(pr) as r:
        print(r.read())

    sys.exit(0)

if __name__=='__main__':
    main()