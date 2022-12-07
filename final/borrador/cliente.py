import socket, pickle, argparse, threading, os, time
import tkinter
import functools
import pandas as pd

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
        msg1 = pickle.dumps(msg1)     #De normal a bits
        s.send(msg1)


def salir(r):
    r.destroy()
    r.quit()
    # y cerrar la conexion


def barco(t):
    print(t.find_withtag("AAA"))
    t.coords(t.find_withtag("AAA"), (50, 50))


def main():
    args = argumentos()

    s = abrir_socket(args)
        
    gui(s)
    
    
    
def recibir(s):
    while True:
        mensaje = pickle.loads(s.recv(10000))        
        print("[ Server ]", mensaje[0] )
        
        # print("Mis barcos: \n", mensaje[1]["mis_barcos"])
        # print("Disparos enemigos: \n", mensaje[2]["disparos_enemigos"])
        # print("Mis disparos: \n", mensaje[2]["disparos_enemigos"])
        return mensaje

    
    # threading.Thread(target=enviar, args=(s,)).start()

    # while True:
    #     msg2 = s.recv(10000)
    #     msg2 = pickle.loads(msg2)   #De bits a normal
    #     borrarPantalla()
    #     print("[ Server ]", msg2)
    pass


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
    


def barcos_tableros(tablero1, tablero2, s):
    mensaje = recibir(s)
    
    mis_barcos = mensaje[1]["mis_barcos"]
    
    print(mis_barcos)
    
    x_tabla = 0
    y_tabla = 0
    for y_gui in range(32,352,32):
        for x_gui in range(32,352,32):
            tablero1.create_text(16+x_gui,16+y_gui, text=mis_barcos.iloc[y_tabla, x_tabla][0], fill='red2', font = ('Arial', 18), tag="AAA")        
            x_tabla += 1
        x_tabla = 0    
        y_tabla += 1
        


def gui(s):
    #T* Pantalla
    raiz = tkinter.Tk()
    raiz.title("Batalla Naval")
    # raiz.iconbitmap("ruta_foto.ico")

    frame_principal = tkinter.Frame(raiz, width=800, height=600)
    frame_principal.pack()

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

    tablero1 = tkinter.Canvas(frame_tableros, bg='black', width=350, height=350)
    tablero1.grid(row=1, column=0, padx=5, pady=5)

    for x in range(0,460,32):
        for y in range(0,460,32):
            tablero1.create_rectangle(x,y,x+32, y+32, fill='gray15')


    tablero2 = tkinter.Canvas(frame_tableros, bg='black', width=352, height=352)
    tablero2.grid(row=1, column=1, padx=5, pady=5)

    for x in range(0,460,32):
        for y in range(0,460,32):
            tablero2.create_rectangle(x,y,x+32, y+32, fill='gray15')

    boton = tkinter.Button(frame_titulo, text="Barco", bg='orange', command=functools.partial(barco, tablero1))
    boton.grid(row=0, column=1)

    #T* Contenido
    indices_tablero(tablero1)
    indices_tablero(tablero2)
    barcos_tableros(tablero1, tablero2, s)
    


    # mi_label = tkinter.Label(mi_frame, text="❤", font=("Arial", 18), padx=5, pady=5)

    # mi_label.grid(row=0, column=0, padx=5, pady=5)

    # cuadro_texto = tkinter.Entry(mi_frame)
    # cuadro_texto.grid(row=0, column=1, padx=5, pady=5)

    raiz.mainloop()     # Siempre al final



if __name__ == '__main__':
    main()
    
#TODO
# El enviar no deberia ser un hilo nuevo, sino una ejecucion despues del mostrar el contenido en los tableros,
# pero el recibir si deberia ser un hilo para evitar que la app se quede esperando.