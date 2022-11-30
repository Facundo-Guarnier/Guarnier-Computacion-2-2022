"""
    Escribir un programa que reciba por argumento la opción -f acompañada de un path_file.

    El programa deberá crear una memoria compartida (variable global, queue, etc.), y generar dos hilos: H1 y H2

    El hilo H1 leerá desde el stdin línea por línea lo que ingrese el usuario.

    Cada vez que el usuario ingrese una línea, H1 la almacenará en la memoria compartida, y notificará, mediante 
    event/condition, al hilo H2.

    El hilo H2 al recibir la notificación leerá la línea desde la memoria compartida la línea, y la almacenará 
    en mayúsculas en el archivo pasado por argumento (path_file).

"""
import argparse, threading, sys, queue, time 

def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="path_file")
    return parser.parse_args()


def hilo1(queue2, event):
    sys.stdin = open(0)
    while True:                                       
        print("Texto: ")
        queue2.put(sys.stdin.readline())
        # print(event.is_set())
        event.wait()
        event.clear()
    

def hilo2(queue2, args, event):
    while True:
        archivo = open(args.f, "a")
        archivo.write(queue2.get().upper())
        # time.sleep(5)
        event.set()   


def main():
    args = argumentos()
    event = threading.Event()
    queue2 = queue.Queue()

    h1 = threading.Thread(target=hilo1, args=(queue2, event)).start()
    h2 = threading.Thread(target=hilo2, args=(queue2, args, event)).start()


if __name__ == "__main__":
    main()

