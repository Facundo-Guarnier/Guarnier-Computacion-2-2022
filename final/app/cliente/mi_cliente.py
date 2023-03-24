import socket, argparse, threading, os, datetime, pickle, re
import tkinter
import functools
from tkinter import ttk
import pandas as pd
import queue

def hora_actual():
    return datetime.datetime.now().strftime("%H:%M:%S")

#! Solo la casilla (Ej: B1, J9)
def enviar_mensaje(s, m):
    s.send(pickle.dumps(m))


def recibir_mensaje(s):
    mensaje = s.recv(10000) 
    return pickle.loads(mensaje)


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=False, help="Puerto", default= 5000)
    parser.add_argument("-d", required=False, help="Direccion IPv4", default= "0.0.0.0")
    parser.add_argument("-i", type=str, required=False, help="Activar GUI", choices=["y", "n"], default="n")
    
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
    er = r'[A-J][0-9]$'   #! Expresion regular para las coordenadas.

    while True:
        msg1 = input("[ Cliente {} ] Input: ".format(hora_actual())).upper()
        
        #TODO Hacer mejor esto, no siempre deberia pueder escribir continuar o salir.  
        if msg1.lower() == "continuar":     #! Jugar proxima partida
            break
        
        elif msg1.lower() == "salir":       #! Desconectar
            break
        
        elif re.match(er, msg1):        #! Coordenada correcta
            break
        
        else:
            print("[ Cliente {} ] Coordenada inválida.".format(hora_actual()))
    

    enviar_mensaje(s, msg1)


def print_mensaje(mensaje):
#! [msg1, tablero1, tablero2, estado]
    print("\n++++++++++++++++++++++++++++++++++++++++++++ PRINT ++++++++++++++++++++++++++++++++++++++++++++\n")
    print("[ Server {} ]\n   Mensaje: {}\n   Estado: {}".format(hora_actual() , mensaje[0], mensaje[3]))    #!Mensaje al jugador
    print("\n-----Mis barcos: \n", mensaje[1]["mis_barcos"])
    print("\n-----Disparos enemigos: \n", mensaje[1]["disparos_enemigos"])
    print("\n-----Mis disparos: \n", mensaje[2]["disparos_enemigos"])
    print("\n++++++++++++++++++++++++++++++++++++++++++++ PRINT ++++++++++++++++++++++++++++++++++++++++++++\n")


def main():
    args = argumentos()

    s = abrir_socket(args)
    
    if args.i == "n":       #! Sin interfaz grafica (GUI)
        print("Sin GUI")
        mensaje = recibir_mensaje(s)        
        print_mensaje(mensaje)
        
        if mensaje[3][0] == False:  #! Error en el server.
            print("++++ ERROR EN EL SERVER ANTES DE SABER QUE JUGADOR SOS {}".format(mensaje[3][1]))
        
        elif mensaje[3][1] == "1":    
            
            while True:     #! Bucle del Jugador 1
                
                while True:     #! Bucle si es que existe un error del server (ej: error-s1)
                    enviar(s)   #! Envia las coordenadas ingresadas por el usuario.
                    
                    print("++ ESPERANDO RESPUESTA DEL SERVIDOR de mi ataque")
                    respuesta = recibir_mensaje(s)  #! Estado de mi actaque al enemigo
                    
                    if respuesta[3][0]:    #! No existe error
                        print("+++++++++++++++++++++ No hay error +++++++++++++++++++++")
                        print_mensaje(respuesta)
                        
                        if respuesta[3][1] == "FIN":
                            print("FIN DE LA PARTIDA, CONTINUAR O SALIR")
                        
                        else:
                            break
                    
                    else:       #! Existe error.
                        print("+++++++++++++++++++++ Si hay error +++++++++++++++++++++")
                        print_mensaje(respuesta)
                    
                    
                #! Estado del actaque enemigo
                while True:     #! Bucle si es que existe un error del server (ej: error-s1)
                    print("++ ESPERANDO RESPUESTA DEL SERVIDOR del ataque enemigo")
                    respuesta = recibir_mensaje(s)
                    
                    if respuesta[3][0]:    #! No existe error
                        print("+++++++++++++++++++++ No hay error +++++++++++++++++++++")
                        print_mensaje(respuesta)
                        if respuesta[3][1] == "FIN":
                            print("FIN DE LA PARTIDA, CONTINUAR O SALIR")
                        
                        else:
                            break
                    
                    else:       #! Existe error.
                        print("+++++++++++++++++++++ Si hay error +++++++++++++++++++++")
                        print_mensaje(respuesta)
                        
        

        elif mensaje[3][1] == "2":  
            while True:     #! Bucle del Jugador 2
                
                #! Estado del actaque enemigo
                while True:     #! Bucle si es que existe un error del server (ej: error-s1)
                    print("++ ESPERANDO RESPUESTA DEL SERVIDOR del ataque enemigo")
                    respuesta = recibir_mensaje(s)
                    
                    if respuesta[3][0]:    #! No existe error
                        print("+++++++++++++++++++++ No hay error +++++++++++++++++++++")
                        print_mensaje(respuesta)
                        if respuesta[3][1] == "FIN":
                            print("FIN DE LA PARTIDA, CONTINUAR O SALIR")
                        
                        else:
                            break
                    
                    else:       #! Existe error.
                        print("+++++++++++++++++++++ Si hay error +++++++++++++++++++++")
                        print_mensaje(respuesta)
                        
                        
                while True:     #! Bucle si es que existe un error del server (ej: error-s1)
                    enviar(s)   #! Envia las coordenadas ingresadas por el usuario.
                    
                    print("++ ESPERANDO RESPUESTA DEL SERVIDOR de mi ataque")
                    respuesta = recibir_mensaje(s)  #! Estado de mi actaque al enemigo
                    
                    if respuesta[3][0]:    #! No existe error
                        print("+++++++++++++++++++++ No hay error +++++++++++++++++++++")
                        print_mensaje(respuesta)
                        
                        if respuesta[3][1] == "FIN":
                            print("FIN DE LA PARTIDA, CONTINUAR O SALIR")
                        
                        else:
                            break
                    
                    else:       #! Existe error.
                        print("+++++++++++++++++++++ Si hay error +++++++++++++++++++++")
                        print_mensaje(respuesta)
                    

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
            tablero.create_rectangle(x,y,x+32, y+32, fill='gray15', tags="{}{}".format(y_tablero,x_tablero))
            y_tablero += 1
        y_tablero = -1
        x_tablero += 1


#! Esto es para que el bind quede en un hilo
#TODO Hay que ver si esto es necesario 
def on_board_click_wrapper(event,q1,e1):
    threading.Thread(target=on_board_click, args=(event,q1,e1)).start()


#! Luego de seleccionar un casillero, no se deberia poder seleccionar otro hasta que llegue de nuevo la respuesta del server (punto de encuentro?: no funciona porque congela el main)
def on_board_click(event,q1,e1):
    print("AFUERA DEL IF")
    e1.wait()   #! Espera a que lo habiliten a hacer click.
                #TODO no se si el wait va dentro o fuera del if.
    
    if event.widget.find_withtag(tkinter.CURRENT):
        print("DENTRO DEL IF")
        print("TAG del casillero: ", event.widget.itemcget(tkinter.CURRENT, "tag"))   #! Obtener el tag      
        q1.put(event.widget.itemcget(tkinter.CURRENT, "tag"))   #! Envia el tag al hilo de enviar/recibir.  


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


def barcos_tableros(tablero1, tablero2, s, q1, e1):
    mensaje = recibir_mensaje(s)

    #T* Tablero 1
    mis_barcos = mensaje[1]["mis_barcos"]
    x_tabla = 0
    y_tabla = 0
    for y_gui in range(32,352,32):
        for x_gui in range(32,352,32):
            #! Los textos tienen el mismo tag que los rectangulos, para poder hacer click.
            tablero1.create_text(16+x_gui,16+y_gui, text=mis_barcos.iloc[y_tabla, x_tabla][0], fill='red2', font = ('Arial', 18), tag="{}{}".format(y_tabla, x_tabla))        
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
            tablero2.create_text(16+x_gui,16+y_gui, text=mis_disparos.iloc[y_tabla, x_tabla][0], fill='red2', font = ('Arial', 18), tag="{}{}".format(y_tabla, x_tabla))        
            x_tabla += 1
        x_tabla = 0    
        y_tabla += 1


    jugador = str(mensaje[0])
    if "1" == jugador:
        
        #? COMO SE CUANDO TENGO QUE ATACAR O CUANDO TENGO QUE ESPERAR A SER ATACADO?? EL SERVER DEBERIA MANDAR UN TIPO DE SEÑAL, YA QUE 
        #? NO NECEASRIAMENTE SIEMPRE VA A SEGUIR UN ORDEN EN ESPECIDICO: 
        #?   1°: ATACO -> RECIBO ESTADO DE MI ACATQUE -> RECIBO ESTADO DEL ATAQUE HACIA MI
        #?   2°: ATACO -> RECIBO QUE INGRESÉ MAL LAS COORDENADAS -> VUELVO A INGRESAR MAL LAS COORDENADAS -> ETC.
        
        #* Si es jugador 1 no deberia esperar, sino directamente enviar el disparo.
        print("+++++++++++++++++++++++++++++++++++++++++++++ Jugador 1 +++++++++++++++++++++++++++++++++++++++++++++")
        while True:
            e1.set()    #! Habilitar la posibilidad de hacer click.
            #* Se deberia quedar esperando a que se haga click
            msg = q1.get()    #! Leer el click.
            enviar_mensaje(s, msg)
            
    
    elif "2" == jugador:
        print("+++++++++++++++++++++++++++++++++++++++++++++ Jugador 2 +++++++++++++++++++++++++++++++++++++++++++++")
        #* Si es jugador 2, tiene que esperar al disparo del jugador 1.
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
    q1 = queue.Queue()      #! Para enviar el click con el evniar/recibir.
    e1 = threading.Event()  #! Para no estar haciendo click cuando no se debe.
    
    #TODO Revisar como funciona biente esto, <Button-1> es clic izquierdo.
    # tablero2.bind("<Button-1>", on_board_click_wrapper)
    tablero2.bind("<Button-1>", lambda event: on_board_click_wrapper(event, q1, e1))
    """
        En esta línea de código, se está asignando una función anónima (lambda) como controlador de eventos para el 
        evento "Button-1" del widget "tablero2". Esta función anónima llama a la función "on_board_click" pasando 
        como argumentos el objeto evento "event" y la variable "cola".

        La función lambda es una forma de crear una función pequeña y anónima que puede ser útil en situaciones donde 
        se necesita una función temporal. En este caso, se utiliza para encapsular la llamada a la función 
        "on_board_click" junto con la variable "cola", para poder pasar ambos argumentos al controlador de eventos 
        sin tener que declarar una función separada.
    """
    
    

    
    #T* Contenido tablero
    encabezado_tablero(tablero1)
    encabezado_tablero(tablero2)
    threading.Thread(target=barcos_tableros, args=(tablero1, tablero2, s, q1, e1)).start()
    
    raiz.mainloop()     #! Siempre al final


if __name__ == '__main__':
    main()



#* Info
# print(tablero.itemcget("#99", "fill"))      #! Devuelve el valor de la configuracion
# tablero.itemconfig("#99", fill="blue")      #! Cambia la configuracion del elemento

# TODO
# Ver lo que está en rojo en la funcion "barcos_tableros".

# Hacer bien lo de continuar o salir al fin de una partida. Revisar funcion "enviar".

# Como comunicar la funcion "on_board_click" con la de "barcos_tableros" para saber cuando 
# puedo hacer click y cuando no, por cuestion de turnos.

#// El problema de los tag al hacer click seguramente se debe a que el espacio en blaco 
#// del Dataframe tiene otro tag que el del rectangulo donde este se encuentra.
