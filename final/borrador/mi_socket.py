import socket, threading, os, pickle, multiprocessing, argparse, queue, time

# https://stackoverflow.com/questions/3991104/very-large-input-and-piping-using-subprocess-popen


# pickle.loads(msg)  bits -> Normal
# pickle.dumps(msg)  Normal -> bits
def conexion(sock, q1):   
    print("  Hilo 'Conexion' ID:", threading.get_native_id())
    while True:
        msg1 = sock.recv(10000)      #Recibe bits
        msg1 = pickle.loads(msg1)   #De bits a normal
        # q1.put(msg1)
        
        # print("q1:", q1)
        # print("get 1:", q1.get())
        # print("get 2:", q1.get())
        

        msg2 = "{}, tu mama".format(msg1)
        msg2 = pickle.dumps(msg2)   #De normal a bits 
        sock.send(msg2)


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=False, help="port", default=5000)
    # parser.add_argument("-c", type=str, required=True, help="concurrencia", choices=["p", "t"])
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



#! Hilo de partida     
#! Acá tiene que leer el diccionario y cada 2 en estado de espera crear una partida 
def partida():
    pass




#! Conexion con la BD
def base_datos():
    pass


def aceptar_cliente(server):
    while True:
        s2,addr = server.accept()
        print("-------------------------------------")
        print("  Nuevo cliente {}". format(addr))
        print("  Proceso padre ID:", os.getpid())
        
        q1 = queue.Queue(maxsize=1)
        # nickname = s2.recv(10000)
        # nickname = pickle.loads(nickname)
        nickname = "Jugador" + str(addr[1])
        
        global clientes
        clientes[nickname] = {
            "s2": s2,
            "q1": q1,
            "jugando": False ,
        }

        threading.Thread(target=conexion, args=(s2, q1)).start()


#! Acá tiene que agregar al diccionario las conexiones
def online(server):
    print("  Proceso 'Online' ID:", os.getpid())
    candado = threading.Lock()  # Seccion critica
    barrera = threading.Barrier(3)  #Es un punto de encuentro de 3 personas
    q_dict = queue.Queue(maxsize=1)

    global clientes
    clientes = {}
    
    threading.Thread(target=aceptar_cliente, args=(server,)).start()

    while len(clientes.keys()) < 2: 
        print("++++++++++++++++++++ Esperando cliente nuevo ++++++++++++++++++++")
        print("Clientes actuales:", len(clientes.keys()))
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        time.sleep(5)
    
    
    for clave in clientes.keys():
        print("Clave:", clave)
    
    print("Clientes:", clientes)
    
    print("muriendo proceso...")
    time.sleep(120)

    # threading.Thread(target=partida, args=()).start()



def main():
    args = argumentos()
    server = abrir_socket(args)
    
    pid_padre = os.getpid()
    print("  Proceso main ID:", pid_padre)

    #! Proceso de todas las partidas y clienets
    p_partidas = multiprocessing.Process(target=online, args=(server,)).start()

    
    #! Proceso BD
    # p_bd = multiprocessing.Process(target=base_datos, args=())
    
    # ...
    #! Proceso main del servidor 
    # ...
    
    
if __name__ == '__main__':
    main()



#TODO Cambiar el diccionario cliente por una clase Cliente.
#TODO ¿Como borrar un cliente que se desconectó con "ctrl + c"?