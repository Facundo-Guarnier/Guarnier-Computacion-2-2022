#!/usr/bin/python3
"""
    Escribir un programa que genere dos hilos utilizando threading.

    Uno de los hilos deberá leer desde stdin texto introducido por 
    el usuario, y deberá escribirlo en un pipe (threading).

    El segundo hijo deberá leer desde el pipe el contenido de texto, 
    lo encriptará utilizando el algoritmo ROT13, y lo almacenará 
    en una cola de mensajes (queue).

    El primer hijo deberá leer desde dicha cola de mensajes y
    mostrar el contenido cifrado por pantalla.
"""

import sys, threading, queue, time

def animacion_carga(): 
    animation = "|/-\\"
    cont_animacion = 0
    cont_tiempo = 0        
    i = 0                     
  
    while (cont_tiempo != 20): 
        time.sleep(0.1)  
        sys.stdout.write("\r" + "Encriptando " + animation[cont_animacion]) 
        sys.stdout.flush() 
        cont_animacion = (cont_animacion + 1)% 4
        i += 1
        cont_tiempo += 1
    
    sys.stdout.write("\r")
    sys.stdout.flush() 


def leer(n):
    sys.stdin = open(0)
    for _ in range(n):  
        print("Ingrese un mensaje: ")
        q2.put(sys.stdin.readline())

        time.sleep(0.1)
        while q1.empty( ):
            animacion_carga()
            time.sleep(0.5)

        print("El mensaje encriptado es: ", q1.get())
        q1.task_done()


def encriptacion(n):
    rot13 = str.maketrans(
        'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
        'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm',
        )
    for i in range(n):
        texto = q2.get().translate(rot13)

        time.sleep(1)           #Solo para que aparezca la animacion de carga :)
        q1.put(texto)
        

if __name__ == "__main__":
    
    q1 = queue.LifoQueue()
    q2 = queue.LifoQueue()

    repeticion = 5      #No sabía cuantas lineas habia que leer jeje

    h1 = threading.Thread(target=leer, args=(repeticion,), name="h1")
    h2 = threading.Thread(target=encriptacion, args=(repeticion,), name="h2")
    h1.start()
    h2.start()
    h1.join()
    h2.join()
