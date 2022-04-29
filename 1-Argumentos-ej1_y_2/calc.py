"""
> Opcion (-a)
> Argemuneto (-a lalala)
  El argumento en lalala de la opcion -a


Ejercicio 1 - Getopt
    Crear una calculadora, donde se pase como argumentos luego de la opción -o el operador que se va a ejecutar (+,-,*,/), luego 
    de -n el primer número de la operación, y de -m el segundo número.

    Ejemplo:
    python3 calc.py -o + -n 5 -m 6
    5 + 6 = 11
    Considerar que el usuario puede ingresar los argumentos en cualquier orden. El programa deberá verificar que los argumentos 
    sean válidos (no repetidos, números enteros, y operaciones válidas.

"""
import sys
import getopt

numero1=""
numero2=""
operador=""
try:
    opcion, argumento = getopt.getopt(sys.argv[1:], "-o:-n:-m:")
    for opc, arg in opcion:
        if opc == "-o" :
            if arg in "- + / *" and operador == "":
                operador = arg
            else:
                print("Error: Operador no valido o repetido.")
                exit()
        elif opc == "-n":
            if numero1 == "": 
                numero1 = int(arg)
            else:
                print("Error: Operador repetido.")
                exit()
        elif opc == "-m":
            if  numero2 == "":
                numero2 = int(arg)
            else:
                print("Error: Operador repetido.")
                exit()

    if operador == "+":
        print(numero1, "+", numero2, "=", numero1 + numero2)
    elif  operador == "-":
        print(numero1, "-", numero2, "=", numero1 - numero2)
    elif  operador == "/":
        print(numero1, "/", numero2, "=", numero1 / numero2)
    elif  operador == "*":
        print(numero1, "*", numero2, "=", numero1 * numero2)


except getopt.GetoptError as e:
    print("Error:", e)
    exit()

except ValueError as e:
    print("Error:", e)
    exit()