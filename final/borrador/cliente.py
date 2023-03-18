import socket, argparse, threading, os, time, pickle
import tkinter
import functools
from tkinter import ttk
import pandas as pd


def enviar_mensaje(s, m):
    s.send(pickle.dumps(m))


def recibir_mensaje(s):
    mensaje = s.recv(10000) 
    return pickle.loads(mensaje)


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=False, help="port", default= 5000)
    parser.add_argument("-d", required=False, help="direccion", default= "0.0.0.0")
    parser.add_argument("-i", type=str, required=True, help="Activar GUI", choices=["y", "n"], default="n")
    
    return parser.parse_args()


def abrir_socket(args):
    host = args.d
    port = args.p
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server:", host + ":" + str(port))
        s.connect((host, port))
        return s

    except:
        print("No se puede establecer conexion, finalizando...")
        os._exit(0)


def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")

    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def enviar(s):
    msg1 = input("[ Cliente ] ")
    enviar_mensaje(s, msg1)


def recibir(s):
# [msg1, tablero1, tablero2]
    mensaje = recibir_mensaje(s)
    print("[ Server ]", mensaje[0] )    #!Mensaje al jugador
    print("\n-----Mis barcos: \n", mensaje[1]["mis_barcos"])
    print("\n-----Disparos enemigos: \n", mensaje[1]["disparos_enemigos"])
    print("\n-----Mis disparos: \n", mensaje[2]["disparos_enemigos"])
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    return mensaje


def main():
    args = argumentos()

    s = abrir_socket(args)
    
    
    #! Sin interfaz grafica (GUI)
    if args.i == "n":
        mensaje = recibir(s)
        
        #! Sos el jugador 1
        if mensaje[0] == "1":
            while True:
                #* Enviar
                enviar(s)
                
                #* Recibir
                #! Estado de mi actaque al enemigo
                print("++ ESPERANDO RESPUESTA DEL SERVIDOR de mi ataque")
                recibir(s)
                
                #! Estado del actaque enemigo
                print("++ ESPERANDO RESPUESTA DEL SERVIDOR del ataque enemigo")
                recibir(s)
        
        #! Sos el jugador 2
        elif mensaje[0] == "2":
            while True:
                #* Recibir
                #! Estado del actaque enemigo
                print("++ ESPERANDO RESPUESTA DEL SERVIDOR del ataque enemigo")
                recibir(s)
        
                #* Enviar
                enviar(s)
        
                #* Recibir
                #! Estado de mi actaque al enemigo
                print("++ ESPERANDO RESPUESTA DEL SERVIDOR de mi ataque")
                recibir(s)

        else:
            print("ERROR AL IDENTIFICAR JUGADOR (error-c1)")
            
    #! Con interfaz grafica (GUI)
    elif args.i == "y":
        # s=""
        gui(s)   

#*-------------------------------------------------- GUI --------------------------------------------------


# "0":["A","B","C","D","E","F","G","H","I","J"],
# "1":[" "," "," "," "," "," "," "," "," "," "],
# "2":[" "," "," "," "," "," "," "," "," "," "],
# "3":[" "," "," "," "," "," "," "," "," "," "],
# "4":[" "," "," "," "," "," "," "," "," "," "],
# "5":[" "," "," "," "," "," "," "," "," "," "],
# "6":[" "," "," "," "," "," "," "," "," "," "],
# "7":[" "," "," "," "," "," "," "," "," "," "],
# "8":[" "," "," "," "," "," "," "," "," "," "],
# "9":[" "," "," "," "," "," "," "," "," "," "],


def salir(r):
    r.destroy()
    r.quit()
    #TODO y cerrar la conexion
    pass


def crear_cuadricula(tablero):
    y_tablero = -1  # Para el tag
    x_tablero = -1
    
    for x in range(0,352,32):   # Cada 32 pixeles se hace un rectangulo (352 / 11 = 32)
        for y in range(0,352,32):
            #! Los rectangulos tienen el mismo tag que los textos, para poder hacer click.
            tablero.create_rectangle(x,y,x+32, y+32, fill='gray15', tags="REC -> Fila: {}, Columna: {}".format(y_tablero,x_tablero))
            y_tablero += 1
        y_tablero = -1
        x_tablero += 1


def on_board_click(event):
    #! Esto deberia esperar a que lleguen los barcos del lado del server
    #! Luego de seleccionar un casillero, no se deberia poder seleccionar otro hasta que llegue de nuevo la respuesta del server (punto de encuentro?: no funciona porque congela el main)

    if event.widget.find_withtag(tkinter.CURRENT):
        # print("TAG del casillero", event.widget.itemcget(tkinter.CURRENT, "tag")[1:4])       #! Obtener el tag        
        print("TAG del casillero", event.widget.itemcget(tkinter.CURRENT, "tag"))       #! Obtener el tag        
        # event.widget.itemconfig(tkinter.CURRENT, fill="blue")


def encabezado_tablero(tablero):
    x = 0
    for x_gui in range(32,352,32):
        tablero.create_text(16+x_gui, 16, text=x, fill='white', font = ('Arial', 18), tag="Columna {}".format(x))        
        x += 1
        
    abc = "ABCDEFGHIJ"
    y = 0
    for y_gui in range(32,352,32):
        tablero.create_text(16, 16+y_gui, text=abc[y], fill='white', font = ('Arial', 18), tag="Fila {}".format(abc[y]))        
        y += 1


def barcos_tableros(tablero1, tablero2, s):
    mensaje = recibir_mensaje(s)

    #T* Tablero 1
    mis_barcos = mensaje[1]["mis_barcos"]
    x_tabla = 0
    y_tabla = 0
    for y_gui in range(32,352,32):
        for x_gui in range(32,352,32):
            #! Los textos tienen el mismo tag que los rectangulos, para poder hacer click.
            tablero1.create_text(16+x_gui,16+y_gui, text=mis_barcos.iloc[y_tabla, x_tabla][0], fill='red2', font = ('Arial', 18), tag="TEXT -> Fila {}, Columna {}.".format(y_tabla+1, x_tabla+1))        
            x_tabla += 1
        x_tabla = 0    
        y_tabla += 1
    
    
    #T* Tablero 2
    mis_disparos = mensaje[2]["disparos_enemigos"]
    x_tabla = 0
    y_tabla = 0
    for y_gui in range(32,352,32):
        for x_gui in range(32,352,32):
            #! Los textos tienen el mismo tag que los rectangulos, para poder hacer click.
            tablero2.create_text(16+x_gui,16+y_gui, text=mis_disparos.iloc[y_tabla, x_tabla][0], fill='red2', font = ('Arial', 18), tag="TEXT -> Fila {}, Columna {}.".format(y_tabla+1, x_tabla+1))        
            x_tabla += 1
        x_tabla = 0    
        y_tabla += 1


    jugador = str(mensaje[0])
    if "1" == jugador:
        #! Si es jugador 1 no deberia esperar, sino directamente enviar el disparo.
        pass
        
    elif "2" == jugador:
        #! Si es jugador 2, tiene que esperar al disparo del jugador 1.
        pass


def gui(s):
    print("PID gui: ", os.getpid())
    #T* Pantalla
    raiz = tkinter.Tk()
    raiz.title("Batalla Naval")
    # raiz.iconbitmap("ruta_foto.ico")

    frame_principal = tkinter.Frame(raiz, width=800, height=600)
    frame_principal.pack()


    #T* Titulo
    frame_titulo = tkinter.Frame(frame_principal, width=800, height=50, bg="black")
    frame_titulo.grid(row=0, column=0)
    # frame_titulo.grid_propagate(False)   #! No ajusta el tamaño del freame al contenido

    b_salir = tkinter.Button(frame_titulo, text="Salir", bg='orange', command=functools.partial(salir, raiz))
    b_salir.grid(row=0, column=0)
    

    #T* Frame para cada tableros
    frame_tableros = tkinter.Frame(frame_principal, width=800, height=550, bg="green")
    frame_tableros.grid(row=1, column=0)
    frame_tableros.grid_propagate(False)   #! No ajusta el tamaño del freame al contenido

    titulo1 = tkinter.Label(frame_tableros, text="Tablero 1:", font=("Arial", 18), padx=5, pady=5)
    titulo1.grid(row=0, column=0, padx=5, pady=5)

    titulo1 = tkinter.Label(frame_tableros, text="Tablero 2:", font=("Arial", 18), padx=5, pady=5)
    titulo1.grid(row=0, column=1, padx=5, pady=5)

    #! Tablero 1
    tablero1 = tkinter.Canvas(frame_tableros, bg='black', width=352, height=352)
    tablero1.grid(row=1, column=0, padx=5, pady=5)    
    crear_cuadricula(tablero1)
    
    #! Tablero 2
    tablero2 = tkinter.Canvas(frame_tableros, bg='black', width=352, height=352)
    tablero2.grid(row=1, column=1, padx=5, pady=5)
    crear_cuadricula(tablero2)
    
    
    #T* Funcion de click en el tablero para disparar/atacar
    tablero2.bind("<Button-1>", on_board_click)     #TODO Revisar como funciona biente esto, <Button-1> es clic izquierdo    

    
    #T* Contenido tablero
    encabezado_tablero(tablero1)
    encabezado_tablero(tablero2)
    threading.Thread(target=barcos_tableros, args=(tablero1, tablero2, s)).start()
    
    raiz.mainloop()     #! Siempre al final


if __name__ == '__main__':
    main()

#* Info
# print(tablero.itemcget("#99", "fill"))      #! Devuelve el valor de la configuracion
# tablero.itemconfig("#99", fill="blue")      #! Cambia la configuracion del elemento

# TODO
# Como comunicar la funcion "on_board_click" con la de "barcos_tableros" para saber cuando 
# puedo hacer click y cuando no, por cuestion de turnos.

#// El problema de los tag al hacer click seguramente se debe a que el espacio en blaco 
#// del Dataframe tiene otro tag que el del rectangulo donde este se encuentra.

