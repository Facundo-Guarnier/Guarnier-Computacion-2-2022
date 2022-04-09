#!/usr/bin/python3
"""
    Escribir un programa en Python que reciba los siguientes 
    argumentos por línea de comandos:

    -n <N>
    -r <R>
    -h
    -f <ruta_archivo>
    -v
    El programa deberá abrir (crear si no existe) un archivo de 
    texto cuyo path ha sido pasado por argumento con -f.

    El programa debe generar <N> procesos hijos. Cada proceso estará 
    asociado a una letra del alfabeto (el primer proceso con la 
    "A", el segundo con la "B", etc). Cada proceso almacenará en 
    el archivo su letra <R> veces con un delay de un segundo entre 
    escritura y escritura (realizar flush() luego de cada escritura).

    El proceso padre debe esperar a que los hijos terminen, luego 
    de lo cual deberá leer el contenido del archivo y mostrarlo 
    por pantalla.

    La opción -h mostrará ayuda. La opción -v activará el modo 
    verboso, en el que se mostrará antes de escribir cada letra 
    en el archivo: Proceso <PID> escribiendo letra 'X'.

    Ejemplo 1:
    ./escritores.py -n 3 -r 4 -f /tmp/letras.txt

    ABCACBABCBAC

    Ejemplo 2:
    ./escritores.py -n 3 -r 5 -f /tmp/letras.txt -v
    Proceso 401707 escribiendo letra 'A'
    Proceso 401708 escribiendo letra 'B'
    Proceso 401709 escribiendo letra 'C'
    Proceso 401708 escribiendo letra 'B'
    Proceso 401707 escribiendo letra 'A'
    Proceso 401709 escribiendo letra 'C'
    Proceso 401707 escribiendo letra 'A'
    Proceso 401708 escribiendo letra 'B'
    Proceso 401709 escribiendo letra 'C'
    Proceso 401707 escribiendo letra 'A'
    Proceso 401708 escribiendo letra 'B'
    Proceso 401709 escribiendo letra 'C'
    Proceso 401707 escribiendo letra 'A'
    Proceso 401708 escribiendo letra 'B'
    Proceso 401709 escribiendo letra 'C'
    ABCBACABCABCABC

"""

import abc
import argparse, time, os, subprocess, string
from re import sub

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, required=True, help="Cantidad de procesos hijos.")
    parser.add_argument("-r", type=int, required=True, help="Repeticion.")
    parser.add_argument("-f", type=str, required=True, help="Ruta del archivo.") 
    parser.add_argument("-v", required=False, action='store_true', help="Activar modo verboso.", default=False)

    args = parser.parse_args()


    pid_padre = os.getpid()
    abcd = string.ascii_uppercase

    for i in range(args.n):

        os.fork()
        if pid_padre != os.getpid():    # Que el padre no escriba 
            for x in range(args.r):
                time.sleep(1)
                escribir(args.v, args.f, abcd[i])
            os._exit(0) 


    for i in range(args.n):     #Espera a que termien n cantidad de hijos.
        os.wait()




    with open(args.f, "a") as archivo:
        archivo.write("\n")
        archivo.flush()

    texto = subprocess.Popen("cat "+args.f, shell=True,  universal_newlines=True)




def escribir(v,f,letra):
    if v:
        print("Proceso {} escribiendo letra '{}'".format(os.getpid(), letra))

    with open(f, "a") as archivo:
        archivo.write(letra)
        archivo.flush()






if __name__=='__main__':
    main()