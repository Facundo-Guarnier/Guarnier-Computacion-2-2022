import socket, threading, os, pickle, multiprocessing, argparse, queue, time

# https://stackoverflow.com/questions/3991104/very-large-input-and-piping-using-subprocess-popen


# pickle.loads(msg)  bits -> Normal
# pickle.dumps(msg)  Normal -> bits
def conexion(sock, q1):   
    print("  Hilo 'Conexion' ID:", threading.get_native_id())
    while True:
        msg1 = sock.recv(10000)      #Recibe bits
        msg1 = pickle.loads(msg1)   #De bits a normal
        q1.put(msg1+", del j1")
        
        # print("q1:", q1)
        # print("get 1:", q1.get())
        # print("get 2:", q1.get())
        
        #TODO Problema: Ahora tengo que leer el q1 pero cuando el otro jugador me cambió el valor, si pongo ahora un .get voy a leer lo que puse mas recien.
        # msg2 = q1.get()
        
        msg2 = "[RESPUESTA] {}".format(msg1)
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
        #TODO Poner una seccion critica 
        clientes[nickname] = {
            "s2": s2,
            "q1": q1,
            "espera": True,
        }

        threading.Thread(target=conexion, args=(s2, q1)).start()


#! Hilo de partida     
#! Acá tiene que leer el diccionario y cada 2 en estado de espera crear una partida 
def partida(jugadores):
    print("  Hilo 'Partida' ID:", threading.get_native_id())

    global clientes
    q_jugador1 = jugadores[list(jugadores.keys())[0]]["q1"]
    q_jugador2 = jugadores[list(jugadores.keys())[1]]["q1"]
    
    #TODO Estas en el problema de sincronizacion de turnos entre los 2 jugadores, ya que el queue de cada jugador no se vé con el del otro, 
    #TODO por lo tanto abria que utilizar el mismo queue (q1) pero hay que avisar cuando puede leer  y cuando puede escribir. Para esto estas 
    #TODO viendo la clase de EVENT. VER LA CLASE 2 de EVENT

# { "Jugador5923":
#     {
#         "s2": s2,
#         "q1": q1,
#         "espera": True,
#     }
# }


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

        time.sleep(5)

    while True:
        jugadores_espera = {}
        
        for clave in clientes.keys():
            if clientes[clave]["espera"]:
                jugadores_espera[clave] = clientes[clave]
        
        if len(jugadores_espera) >= 2:
            threading.Thread(target=partida, args=(jugadores_espera,)).start()
        
        else:
            print("++++++++++++++++++++ Esperando jugador nuevo ++++++++++++++++++++")
            time.sleep(3)



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
#TODO Poner una seccion critica a las variables globales