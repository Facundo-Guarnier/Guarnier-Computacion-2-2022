#!/usr/bin/python3
"""
    Escribir un programa que reciba por argumento la 
    opción -f acompañada de un path_file.

    >Etapa 1:
    El programa deberá crear un segmento de memoria
    compartida anónima, y generar dos hijos: H1 y H2

    El H1 leerá desde el stdin línea por línea lo que 
    ingrese el usuario.

    Cada vez que el usuario ingrese una línea, H1 la 
    almacenará en el segmento de memoria compartida, 
    y enviará la señal USR1 al proceso padre.

    El proceso padre, en el momento en que reciba la 
    señal USR1 deberá mostrar por pantalla el contenido 
    de la línea ingresada por el H1 en la memoria 
    compartida, y deberá notificar al H2 usando la 
    señal USR1.

    El H2 al recibir la señal USR1 leerá la línea 
    desde la memoria compartida la línea, y la 
    almacenará en mayúsculas en el archivo pasado 
    por argumento (path_file).

    >Etapa 2:
    Cuando el usuario introduzca "bye" por terminal, 
    el hijo H1 enviará la señal USR2 al padre indicando 
    que va a terminar, y terminará.
    El padre, al recibir la señal USR2 la enviará al 
    H2, que al recibirla terminará también.
    El padre esperará a que ambos hijos hayan 
    terminado, y terminará también.
"""
import sys, os, mmap, argparse, signal

def h1(pid, memoria):
    for linea in sys.stdin:
        if linea == "bye\n":
            print("Terminando hijo 1.... :'(")
            os.kill(os.getppid(), signal.SIGUSR2)
            sys.exit(0)

        memoria.write(linea.encode())
        os.kill(os.getppid(), signal.SIGUSR1)


def h2(pid):
    while True:
        signal.signal(signal.SIGUSR1, handler_h2_1)
        signal.signal(signal.SIGUSR2, handler_h2_2)
        signal.pause()

def handler_h2_1(nro, frame):
    leido = memoria.read(1024)
    memoria.seek(0)
    with open(args.f, 'w+') as archivo:
        archivo.write(leido.decode().upper())

def handler_h2_2(nro, frame):
    print("Terminando hijo 2.... :'(")
    sys.exit(0)


def padre():
    while True:
        signal.signal(signal.SIGUSR1, handler_padre_1)
        signal.signal(signal.SIGUSR2, handler_padre_2)
        signal.pause()

def handler_padre_1(nro, frame):
    print(memoria.read(1024).decode())
    memoria.seek(0)
    os.kill(pid_h2, signal.SIGUSR1)


def handler_padre_2(nro, frame):
    os.kill(pid_h2, signal.SIGUSR2)
    print("Terminando Padre.... :'(")
    for _ in range(2):
        os.wait()
    sys.exit(0)



parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, required=True, help="Ruta del archivo.") 
args = parser.parse_args()

memoria = mmap.mmap(-1, 1024)

for i in range(2):
    pid_hijo = os.fork()

    if i == 0:
        pid_h1 = pid_hijo
        if pid_h1 == 0:
            h1(pid_h1, memoria)

    elif i == 1:
        pid_h2 = pid_hijo
        if pid_h2 == 0:
            h2(pid_h2)

padre()

#./ej_7.py -f /home/texto.txt