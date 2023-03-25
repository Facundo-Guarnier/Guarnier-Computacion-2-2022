import threading, os, pickle
import tkinter
import functools
from tkinter import ttk
import queue


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


#! Solo la casilla (Ej: B1, J9)
def enviar_mensaje(s, m):
    s.send(pickle.dumps(m))


def recibir_mensaje(s):
    mensaje = s.recv(10000) 
    return pickle.loads(mensaje)



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

