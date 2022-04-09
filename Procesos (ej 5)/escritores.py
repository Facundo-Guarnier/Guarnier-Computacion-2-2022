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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, required=True, help="Cantidad de procesos hijos.")
    parser.add_argument("-r", type=int, required=True, help="Repeticion.")
    parser.add_argument("-f", type=str, required=True, help="Ruta del archivo.")
    parser.add_argument("-v", equired=False, action='store_true', help="Activar modo verboso.")
    args = parser.parse_args()


    pid_padre = os.getpid()
    abcd = string.ascii_uppercase

    for i in range(args.n):

        os.fork()
        if pid_padre != os.getpid():    # Que el padre no haga la suma 
            
            escribir(args.v, args.f, abcd[i])

    for i in range(args.n):     #Espera a que termien n cantidad de hijos.
        os.wait()



def escribir(v,f):
    if v:
        pass
    else:
        p = subprocess.Popen(, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True)
        salida, error = p.communicate()
        a = "."
        

if __name__=='__main__':
    main()