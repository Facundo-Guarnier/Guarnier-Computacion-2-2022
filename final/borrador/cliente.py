import socket, pickle, argparse, threading, os
import tkinter

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


def recibir(s):
    print("[ Server ]", pickle.loads(s.recv(10000)))
    threading.Thread(target=enviar, args=(s,)).start()

    while True:
        msg2 = s.recv(10000)
        msg2 = pickle.loads(msg2)   #De bits a normal
        borrarPantalla()
        print("[ Server ]", msg2)


def enviar(s):
    while True:
        msg1 = input("[ Cliente ]: ")
        msg1 = pickle.dumps(msg1)     #De normal a bits
        s.send(msg1)


def main():
    args = argumentos()

    s = abrir_socket(args)

    threading.Thread(target=recibir, args=(s,)).start()



def gui():
    # https://www.youtube.com/watch?v=hTUJC8HsC2I 
    raiz = tkinter.Tk()
    raiz.title("Batalla Naval")
    # raiz.iconbitmap("ruta_foto.ico")
    
    raiz.config(bg="blue")
    
    
    #++++++++++++++++++++++++++++
    
    mi_frame = tkinter.Frame(raiz, width=800, height=600,bg="red")
    
    mi_frame.pack()
    
    
    #+++++++++++++++++++++++++++++
    
    mi_label = tkinter.Label(mi_frame, text="Hola bb", font=("Arial", 18), padx=5, pady=5)
    
    mi_label.grid(row=0,column=0)
    
    
    #+++++++++++++++++++++++++++++
    
    cuadro_texto = tkinter.Entry(mi_frame, padx=5, pady=5)
    cuadro_texto.grid(row=0,column=1)
    
    
    #+++++++++++++++++++++++++++++
    
    raiz.mainloop()     # Siempre al final



if __name__ == '__main__':
    main()
    # gui()