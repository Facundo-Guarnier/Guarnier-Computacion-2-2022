#!/usr/bin/python3
"""
    Escribir un programa que genere dos hijos utilizando multiprocessing.

    Uno de los hijos deberá leer desde stdin texto introducido por el 
    usuario, y deberá escribirlo en un pipe (multiprocessing).

    El segundo hijo deberá leer desde el pipe el contenido de texto, lo 
    encriptará utilizando el algoritmo ROT13, y lo almacenará en una cola 
    de mensajes (multiprocessing).

    El primer hijo deberá leer desde dicha cola de mensajes y mostrar el 
    contenido cifrado por pantalla.
"""
import sys, multiprocessing

def leer(e,n):
    sys.stdin = open(0)
    for i in range(n):                  
        e.send(sys.stdin.readline())
    e.close()


def encriptacion(l,n):
    rot13 = str.maketrans(
        'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
        'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm',
        )
    for i in range(n):
        texto = l.recv().translate(rot13)
        print(texto)

if __name__ == "__main__":
    p_lectura, p_escritura = multiprocessing.Pipe()

    repeticion = 5      #No sabía cuantas lineas habia que leer jeje

    h1 = multiprocessing.Process(target=leer, args=(p_escritura,repeticion))
    h2 = multiprocessing.Process(target=encriptacion, args=(p_lectura,repeticion))
    h1.start()
    h2.start()
    h1.join()
    h2.join()
