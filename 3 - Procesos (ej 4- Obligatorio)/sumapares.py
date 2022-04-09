#!/usr/bin/python3
"""
    Escribir un programa en Python que reciba los siguientes argumentos por línea de comandos:

        -n <numero>
        -h
        -v

    El programa debe generar <numero> procesos hijos, y cada proceso calculará la suma de todos 
    los números enteros pares entre 0 y su número de PID.

    El programa deberá mostrar por pantalla:

        PID – PPID : <suma_pares>
    El proceso padre debe esperar a que todos sus hijos terminen.

    La opción -h mostrará ayuda de uso, y la opción -v habilitará el modo verboso de la aplicación. 
    El modo verboso debe mostrar, además de la suma, un mensaje al inicio y al final de la 
    ejecución de cada proceso hijo, que indique su inicio y fin.

    Ejemplos 1:

        ./sumapares.py -n 2
        32803 – 4658: 269009202
        32800 – 4658: 268943600

    Ejemplos 2:

        ./sumapares.py -n 2 -v
        Starting process 32800
        Starting process 32803
        Ending process 32803
        32803 – 4658: 269009202
        Ending process 32800
        32800 – 4658: 268943600

"""
import argparse, os, time, random

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-n", type=int, required=True, help="Numero de procesos hijos.", )
        parser.add_argument("-v", required=False, action='store_true', help="Activar el modo verboso.")
        args = parser.parse_args()
        # action='store_true': Por defecto es False, pero si se menciona, pasaria a ser True.
    except:
        print("Error en los argumentos")
        os._exit(0)

    pid_padre = os.getpid()

    for i in range(args.n):
        os.fork()
        if pid_padre != os.getpid():    # Que el padre no haga la suma 
            f_hijo(args.v, i)
            
        # os.wait()   #Espera a que el hijo termine para seguir con otro.

    # os.wait()   #Todos los hijos se ejecutarian a la vez y espera a que terminen todos pero de forma rara.

    for i in range(args.n): #Espera a que termien n cantidad de hijos.
        os.wait()


def f_hijo(v, i):
    suma = 0
    for x in range(os.getpid()):
            if x % 2 == 0:
                suma += x
    
    if v:
        print("Starting process ", os.getpid())
        print("Ending process ", os.getpid())
        print("%d - %d: %d\n" % (os.getpid(),os.getppid(), suma))

    else:
        print("%d - %d: %d" % (os.getpid(),os.getppid(), suma))
    print("Estoy esperando", i)
    
    a = (1,2,3,4,5,6,7,8,9)
    time.sleep(5 + random.choice(a))
    os._exit(0)      #Finaliza el hijo


if __name__ == "__main__":
    main()
