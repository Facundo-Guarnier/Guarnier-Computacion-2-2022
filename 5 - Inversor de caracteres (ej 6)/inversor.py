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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="Ruta del archivo.") 

    args = parser.parse_args()

    with open(args.f, 'r') as file:
        texto = file.readlines()
        cant_filas = len(texto)

    for i in range(cant_filas):
        r,w = os.pipe()
        
        id_hijo = os.fork()

        if id_hijo == 0:
            os.close(r)
            w = os.fdopen(w, 'w')
            
            fila = texto[i] 
            invertida = ""
            for a in range(len(fila)):
                invertida += fila[-1-a]

            w.write(invertida)
            w.close()
            sys.exit(0)             #Muere el hijo

        else:
            os.close(w)
            r = os.fdopen(r)
            print(r.read(), end="")
    r.close()
    print("")

    for i in range(cant_filas):
        os.wait()    



if __name__=='__main__':
    main()