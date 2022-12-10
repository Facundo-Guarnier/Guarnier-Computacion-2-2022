import socket, argparse, threading, os, time, pickle
import tkinter
import functools
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
    while True:
        msg1 = input("[ Cliente ]: ")
        enviar_mensaje(s, msg1)


def salir(r):
    r.destroy()
    r.quit()
    # y cerrar la conexion
    pass


def barco(tablero):
    print(tablero.itemcget("#99", "fill"))      # Devuelve el valor de la configuracion
    tablero.itemconfig("#99", fill="blue")      # Cambia la configuracion del elemento


def main():
    args = argumentos()

    global pe
    pe = threading.Barrier(2)

    # s = abrir_socket(args)
    s=""
    gui(s)   


def recibir(s):
    while True:
        mensaje = recibir_mensaje(s)
        print("[ Server ]", mensaje[0] )
        
        # print("Mis barcos: \n", mensaje[1]["mis_barcos"])
        # print("Disparos enemigos: \n", mensaje[2]["disparos_enemigos"])
        # print("Mis disparos: \n", mensaje[2]["disparos_enemigos"])
        return mensaje

    
    # threading.Thread(target=enviar, args=(s,)).start()

    # while True:
    #     msg2 = recibir_mensaje(s)
    #     borrarPantalla()
    #     print("[ Server ]", msg2)
    pass


def crear_cuadricula(tablero):
    
    y_tablero = -1  # Para el tag
    x_tablero = -1
    
    for x in range(0,352,32):   # Cada 32 pixeles se hace un rectangulo (352 / 11 = 32)
        for y in range(0,352,32):
            tablero.create_rectangle(x,y,x+32, y+32, fill='gray15', tags="#{}{}".format(y_tablero,x_tablero), )
            print("#{}{}".format(y_tablero,x_tablero))
            
            y_tablero += 1
        y_tablero = -1
        x_tablero += 1


def on_board_click(event):
    #! Esto deberia esperar a que lleguen los barcos del lado del server
    #! Luego de seleccionar un casillero, no se deberia poder seleccionar otro hasta que llegue de nuevo la respuesta del server (punto de encuentro?)

    # global pe
    
    # pe.wait()

    if event.widget.find_withtag(tkinter.CURRENT):
        print(event.widget.itemcget(tkinter.CURRENT, "tag")[1:4])       # Obtener el tag
        event.widget.itemconfig(tkinter.CURRENT, fill="blue")


def indices_tablero(tablero):
    x = 0
    for x_gui in range(32,352,32):
        tablero.create_text(16+x_gui, 16, text=x, fill='white', font = ('Arial', 18), tag="AAA")        
        x += 1
        
    abc = "ABCDEFGHIJ"
    y = 0
    for y_gui in range(32,352,32):
        tablero.create_text(16, 16+y_gui, text=abc[y], fill='white', font = ('Arial', 18), tag="AAA")        
        y += 1



def leer_click(tablero):
    print(threading.get_native_id())
    tablero.bind("<Button-1>", on_board_click)     #TODO Revisar como funciona biente esto
    

def barcos_tableros(tablero1, tablero2, s):
    mensaje = recibir(s)
    
    jugador = str(mensaje[0])
    mis_barcos = mensaje[1]["mis_barcos"]

    x_tabla = 0
    y_tabla = 0
    for y_gui in range(32,352,32):
        for x_gui in range(32,352,32):
            tablero1.create_text(16+x_gui,16+y_gui, text=mis_barcos.iloc[y_tabla, x_tabla][0], fill='red2', font = ('Arial', 18), tag="##{}{}".format(y_tabla+1, x_tabla+1))        
            x_tabla += 1
        x_tabla = 0    
        y_tabla += 1
    
    
    if "1" == jugador:
        #! Si es jugador 1 no deberia esperar, sino directamente enviar el disparo.
        pass
        
    elif "2" == jugador:
        #! Si es jugador 2, tiene que esperar al disparo del jugador 1.
        global pe
        pe.wait()


def gui(s):
    
    #T* Pantalla
    raiz = tkinter.Tk()
    raiz.title("Batalla Naval")
    # raiz.iconbitmap("ruta_foto.ico")

    frame_principal = tkinter.Frame(raiz, width=800, height=600)
    frame_principal.pack()
    
    #T* Variables
    disparo = tkinter.StringVar()

    
    #T* Titulo
    frame_titulo = tkinter.Frame(frame_principal, width=800, height=50, bg="black")
    frame_titulo.grid(row=0, column=0)
    frame_titulo.grid_propagate(False)   #No ajusta el tamaño del freame al contenido

    b_salir = tkinter.Button(frame_titulo, text="Salir", bg='orange', command=functools.partial(salir, raiz))
    b_salir.grid(row=0, column=0)
    

    #T* Tableros
    frame_tableros = tkinter.Frame(frame_principal, width=800, height=550, bg="green")
    frame_tableros.grid(row=1, column=0)
    frame_tableros.grid_propagate(False)   #No ajusta el tamaño del freame al contenido

    titulo1 = tkinter.Label(frame_tableros, text="Tablero 1:", font=("Arial", 18), padx=5, pady=5)
    titulo1.grid(row=0, column=0, padx=5, pady=5)

    titulo1 = tkinter.Label(frame_tableros, text="Tablero 2:", font=("Arial", 18), padx=5, pady=5)
    titulo1.grid(row=0, column=1, padx=5, pady=5)


    tablero1 = tkinter.Canvas(frame_tableros, bg='black', width=352, height=352)
    tablero1.grid(row=1, column=0, padx=5, pady=5)    
    crear_cuadricula(tablero1)
    
    tablero2 = tkinter.Canvas(frame_tableros, bg='black', width=352, height=352)
    tablero2.grid(row=1, column=1, padx=5, pady=5)
    crear_cuadricula(tablero2)
    
    threading.Thread(target=leer_click, args=(tablero2,)).start()
    
    
    boton = tkinter.Button(frame_titulo, text="Barco", bg='orange', command=functools.partial(barco, tablero1))
    boton.grid(row=0, column=1)
    

    #T* Cuadro disparo
    cuadro_disparo = tkinter.Entry(frame_titulo, textvariable=disparo, fg="red", justify="right")
    cuadro_disparo.grid(row=0, column=2, )

    
    #T* Contenido tablero
    indices_tablero(tablero1)
    indices_tablero(tablero2)
    # threading.Thread(target=barcos_tableros, args=(tablero1, tablero2, s)).start()
    
    raiz.mainloop()     # Siempre al final



if __name__ == '__main__':
    main()
    
#TODO
# ya obtuve el tag de cada casillero (linea 107), ahora se lo tengo que enviar al server como disparo