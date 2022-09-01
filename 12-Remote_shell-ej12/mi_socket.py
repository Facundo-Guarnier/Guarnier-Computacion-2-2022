import socket, threading, os, pickle, subprocess, argparse

# https://stackoverflow.com/questions/3991104/very-large-input-and-piping-using-subprocess-popen

def hilo(sock):
    print("  Hijo ID:", threading.get_native_id())
    while True:
        msg1 = sock.recv(10000)      #Recibe bits
        msg1 = pickle.loads(msg1)   #De bits a normal

        if msg1 == "exit":
            print("Cliente saliendo...")
            sock.send(pickle.dumps("Saliendo..."))
            sock.close()
            break

        else:
            msg2_diccionario = ejecutor(msg1)
            msg2_diccionario = pickle.dumps(msg2_diccionario)   #De normal a bits 
            sock.send(msg2_diccionario)


def proceso(sock):
    print("  Hijo ID:", os.getpid())
    while True:
        msg1 = sock.recv(10000)      #Recibe bits
        msg1 = pickle.loads(msg1)   #De bits a normal

        if msg1 == "exit":
            print("  Cliente saliendo...")
            sock.send(pickle.dumps("Saliendo..."))
            sock.close()
            break

        else:
            msg2_diccionario = ejecutor(msg1)
            msg2_diccionario = pickle.dumps(msg2_diccionario)   #De normal a bits 
            sock.send(msg2_diccionario)
    os._exit(0) 


def ejecutor(msg1):
    p = subprocess.Popen(msg1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True, bufsize=10000)
    salida, error = p.communicate()
    return {"salida":salida, "error":error}


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="port")
    parser.add_argument("-c", type=str, required=True, help="concurrencia", choices=["p", "t"])
    return parser.parse_args()


def abrir_socket(args):
    host = "0.0.0.0"
    port = args.p

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    print("Padre ID:", os.getpid())
    print("Server 'ON' <" + host + ": " + str(port) + ">")
    s.listen()
    return s


def main():
    args = argumentos()
    s = abrir_socket(args)

    if args.c == "p": 
        print("+++++++++++++ Procesos ++++++++++++++")
        pid_padre = os.getpid()
        while True:
            s2,addr = s.accept()
            print("-------------------------------------")
            print("  Nuevo cliente {}". format(addr))
            os.fork()
            if pid_padre != os.getpid():    
                proceso(s2)

    elif args.c == "t":
        print("+++++++++++++++ Hilos +++++++++++++++")
        while True:
            s2,addr = s.accept()
            print("-------------------------------------")
            print("  Nuevo cliente {}". format(addr))
            threading.Thread(target=hilo, args=(s2,)).start()
        
        
if __name__ == '__main__':
    main()
    
