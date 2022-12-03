import socket, threading, os, pickle, multiprocessing, argparse, queue, time

# https://stackoverflow.com/questions/3991104/very-large-input-and-piping-using-subprocess-popen


# pickle.loads(msg)  bits -> Normal
# pickle.dumps(msg)  Normal -> bits
def cliente(sock, q1, e1, pe):   
    print("  Hilo 'Conexion' ID:", threading.get_native_id())

    msg1 = sock.recv(10000)      #Recibe bits
    msg1 = pickle.loads(msg1)   #De bits a normal

    if "1" == msg1: 
        msg2 = pickle.dumps("Sos el jugador 1")   #De normal a bits 
        sock.send(msg2)
        jugador1(sock, q1, e1, pe)
        
    elif "2" == msg1:
        msg2 = pickle.dumps("Sos el jugador 2")   #De normal a bits 
        sock.send(msg2)
        jugador2(sock, q1, e1, pe)

    else:
        msg2 = pickle.dumps("No se que jugador sos, msg1: {} {}".format(msg1, type(msg1)))   #De normal a bits 
        sock.send(msg2)
        



def jugador1(sock, q1, e1, pe):
    while True:
        #! Desde acá deberia empezar el jugador1
        msg1 = sock.recv(10000)      #Recibe bits
        msg1 = pickle.loads(msg1)   #De bits a normal
        
        q1.put(msg1+", del j1")
        
        pe.wait()
        
        
        #! Desde acá deberia empezar el jugador2
        e1.wait()
        
        msg2 = q1.get() #Mensaje desde el hilo 'Partida'
        
        e1.clear()
        
        msg2 = pickle.dumps(msg2)   #De normal a bits 
        sock.send(msg2)
        
        pass


def jugador2(sock, q1, e1, pe):
    while True:
        #! Desde acá deberia empezar el jugador2
        e1.wait()
        
        msg2 = q1.get() #Mensaje desde el hilo 'Partida'
        
        e1.clear()
        
        msg2 = pickle.dumps(msg2)   #De normal a bits 
        sock.send(msg2)
        
        #! Desde acá deberia empezar el jugador1
        msg1 = sock.recv(10000)      #Recibe bits
        msg1 = pickle.loads(msg1)   #De bits a normal
        
        q1.put(msg1+", del j2")
        
        pe.wait()
        
        pass



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
    print("  Hilo 'Aceptar_cliente' ID:", threading.get_native_id())
    while True:
        s2,addr = server.accept()
        print("-------------------------------------")
        print("  Nuevo cliente {}". format(addr))
        print("  Proceso padre ID:", os.getpid())
        
        q1 = queue.Queue(maxsize=1)
        e1 = threading.Event()      # Predeterminado es falso
        pe = threading.Barrier(2)
        # nickname = s2.recv(10000)
        # nickname = pickle.loads(nickname)
        nickname = "Jugador" + str(addr[1])
        
        
        global clientes
        #TODO Poner una seccion critica 
        clientes[nickname] = {
            "s2": s2,
            "q1": q1,
            "e1": e1,
            "espera": True,
            "pe": pe,
        }

        threading.Thread(target=cliente, args=(s2, q1, e1, pe)).start()


#! Hilo de partida     
def partida(jugadores):
    print("  Hilo 'Partida' ID:", threading.get_native_id())

    global clientes
    q_jugador1 = jugadores[list(jugadores.keys())[0]]["q1"]
    q_jugador2 = jugadores[list(jugadores.keys())[1]]["q1"]
    
    e_jugador1 = jugadores[list(jugadores.keys())[0]]["e1"]
    e_jugador2 = jugadores[list(jugadores.keys())[1]]["e1"]
    
    pe_jugador1 = jugadores[list(jugadores.keys())[0]]["pe"]
    pe_jugador2 = jugadores[list(jugadores.keys())[1]]["pe"]
    
    
    #! Siempre empieza el jugador 1. 
    while True:
        #T* ACÁ me quedé 
        #* PROBLEMATICA: Productor consumidor pero es bidireccional o que cambiar de roll 
        #* Se puede utilizar puntos de encuentro ya que son bidireccionales (los 2 amigos 
        #* tienen que llegar a la plaza, no importa si A llega primero y luego B o viceversa)

        #! Desde acá deberia empezar el jugador1
        pe_jugador1.wait()
        msg1 = q_jugador1.get()
        
        # ...
        # Procesar el mensaje del primer jugador.
        # ...
        msg1 = msg1 + ", este mensaje fue procesado por el hilo 'Partida' :)"
        q_jugador2.put(msg1)
        e_jugador1.set()
        
        
        #! Desde acá deberia empezar el jugador2
        e_jugador2.set()
        pe_jugador2.wait()
        
        msg1 = q_jugador2.get()
        
        # ...
        # Procesar el mensaje del primer jugador.
        # ...
        msg1 = msg1 + ", este mensaje fue procesado por el hilo 'Partida' :)"
        q_jugador1.put(msg1)
        
        pass
        
        
        
        
        
        # #! Codigo viejo
        # msg1 = q_jugador1.get()
        # # ...
        # # Procesar el mensaje del primer jugador.
        # # ...
        # msg1 = msg1 + ", este mensaje fue procesado por el hilo 'Partida' :)"
        
        
        # q_jugador2.put(msg1)


        
        # #! Fin del la jugada del jugador 1
        # #! Comienzo de la jugada del jugador 2
        # msg1 = q_jugador2.get()
        # # ...
        # # Procesar el mensaje del primer jugador.
        # # ...
        # msg1 = msg1 + ", este mensaje fue procesado por el hilo partida :)"
        # e_jugador1.set()    #Avisa al jugador 1 que ya está listo para leer de su queue1.
        
        
        # q_jugador2.put(msg1)
        # q_jugador1.set() 
        # #T* Hasta acá
        
    
    
    
    


# { "Jugador5923":
#     {
#         "s2": s2,
#         "q1": q1,
#         "e1": e1,
#         "espera": True,
#         "pe": pe
#     }
# }


#! Acá tiene que agregar al diccionario las conexiones
def online(server):
    print("  Proceso 'Online' ID:", os.getpid())
    
    semaforo = threading.Semaphore(3)   #Soporta 3 productos del productor (como si fuece un buffer de 3 o que mi recurso soporta 3 instancias)
    candado = threading.Lock()  # Seccion critica, inicia en abierto (creo que es como un semanforo pero inicializado en 1), se suele trabajar con "with candado: ...".
    barrera = threading.Barrier(3)  #Es un punto de encuentro de 3 personas
    q_dict = queue.Queue(maxsize=1)

    global clientes
    clientes = {}
    
    threading.Thread(target=aceptar_cliente, args=(server,)).start()

    #! Acá tiene que leer el diccionario y cada 2 en estado de espera crear una partida 
    while True:
        jugadores_espera = {}
        
        for clave in clientes.keys():
            if clientes[clave]["espera"]:
                jugadores_espera[clave] = clientes[clave]
                
                if len(jugadores_espera) >= 2:
                    break
                
        
        if len(jugadores_espera) >= 2:
            print("++++++++++++++++++++ Se pudo establecer una partida ++++++++++++++++++++")
            threading.Thread(target=partida, args=(jugadores_espera,)).start()
            print("Jugadores en espera:", jugadores_espera)

            for clave in jugadores_espera.keys():
                clientes[clave]["espera"] = False
        
            time.sleep(5)

        else:
            print("++++++++++++++++++++ Esperando jugador nuevo ++++++++++++++++++++")
            print("  Total de jugadores:", len(clientes.keys()))
            print("  Jugadores en espera:", len(jugadores_espera))
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
#TODO Ver como matar al proceso "online" cuando muere el main. Señal de ctrl + c para que tambien se la envíe al hijo. 
#TODO Seccion critica??? En todo los lugares en que esté un q1 y e1.
#TODO Ver si se puede con IPv4 y v6
#TODO Estudiar las diferencias entre threading.Lock(), threading.RLock(), threading.Barrier(3), threading.Semaphore(), threading.BoundedSemaphore(), threading.Condition(), event y otros