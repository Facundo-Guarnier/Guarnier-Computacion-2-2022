#!/usr/bin/python3
"""
    Basándose en estos ejemplos, escribir un programa que reciba por 
    argumentos de línea de comandos los siguientes modificadores:

    -c command

    -f output_file

    -l log_file

    El código deberá crear los archivos pasados por los argumentos -f y -l en 
    el caso de que no existan.

    El código deberá ejecutar el comando haciendo uso de subprocess. Popen, 
    y almacenar su salida en el archivo pasado en el parámetro -f. En el 
    archivo pasado por el modificador -l deberá almacenar el mensaje 
    “fechayhora: Comando XXXX ejecutado correctamente” o en su defecto el 
    mensaje de error generado por el comando si este falla.

    Por ejemplo:
    python ejecutor.py -c “ip a” -o /tmp/salida -l /tmp/log
    El archivo /tmp/salida deberá contener la salida del comando, y /tmp/log 
    deberá contener:fechayhora: Comando “ip a” ejecutado correctamente.
    
    Otro ejemplo:
    python ejecutor.py -c “ls /cualquiera” -o /tmp/salida -l /tmp/log
    El archivo /tmp/salida no contendrá nada nuevo, ya que el comando fallará. 
    El archivo /tmp/log contendrá:
    fechayhora: ls: cannot access '/cualquiera': No such file or directory
"""

import argparse
from datetime import datetime
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", type=str, required=True, help="command")
    parser.add_argument("-o", type=str, required=True, help="output_file")
    parser.add_argument("-l", type=str, required=True, help="log")
    args = parser.parse_args()

    with open(args.o, 'a') as archivo_salida, open(args.l, 'a') as archivo_log:
        p = subprocess.Popen(args.c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True)
        salida, error = p.communicate()
        a = "."

        if a != (a+error):      #Se deberia pode hacer "if error is None:" pero no funciona.
            print("dentro de Error"+error+".")
            archivo_log.write(str(datetime.now()) + " " + str(error))

        else:
            print("fuera de Error"+error+".")
            texto= str(datetime.now()) + ": Comando '" + str(args.c) + "' ejecutado correctamente.\n"
            archivo_log.write(str(texto))
            archivo_salida.write(str(salida) + "\n")


if __name__=='__main__':
    main()