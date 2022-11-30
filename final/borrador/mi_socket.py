import socket, threading, os, pickle, multiprocessing, argparse, queue, time

# https://stackoverflow.com/questions/3991104/very-large-input-and-piping-using-subprocess-popen

def conexion(sock, q1, q_dict):
    # pickle.loads(msg)  bits -> Normal
    # pickle.dumps(msg)  Normal -> bits
    
    print("  Hilo ID:", threading.get_native_id())
    

    dic = q_dict.get()
    dic["nickname"] = "guarnold"
    q_dict.put(dic)
    
    while True:
        msg1 = sock.recv(10000)      #Recibe bits
        msg1 = pickle.loads(msg1)   #De bits a normal
        q1.put(msg1)
        
        # print("q1:", q1)
        # print("get 1:", q1.get())
        # print("get 2:", q1.get())
        

        # msg2 = "{}, tu mama".format(msg1)
        # msg2 = pickle.dumps(msg2)   #De normal a bits 
        # sock.send(msg2)
        pass


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="port")
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



def partida(s):
    #! Hilo de partida     
    while True:
        threading.Thread(target=aceptar_cliente, args=(s,)).start()



def aceptar_cliente(s, q_dict):
    while True:
        s2,addr = s.accept()
        q1 = queue.Queue(maxsize=1)
        
        dic = {
            "s2": s2,
            "q1": q1,
        }
        q_dict.put(dic)
        
        print("-------------------------------------")
        print("  Nuevo cliente {}". format(addr))
        print("  Proceso padre ID:", os.getpid())
        threading.Thread(target=conexion, args=(s2, q1, q_dict)).start()



#! Acá tiene que agregar al diccionario las conexiones
def partidas(s):
    
    q_dict = queue.Queue(maxsize=1)
    threading.Thread(target=aceptar_cliente, args=(s, q_dict)).start()
    
    #! Acá tiene que leer el diccionario y cada 2 en estado de espera crear una partida 
    threading.Thread(target=partida, args=(s)).start()



#! Conexion con la BD
def base_datos():
    pass




def main():
    global clientes = {}

    args = argumentos()
    s = abrir_socket(args)
    
    pid_padre = os.getpid()
    print("  Proceso main ID:", pid_padre)

    #! Proceso de todas las partidas y jugadores
    p_partidas = multiprocessing.Process(target=partidas, args=(s,))

    
    #! Proceso BD
    p_bd = multiprocessing.Process(target=base_datos, args=())
    
    # ...
    #! Proceso main del servidor 
    # ...
    
    
if __name__ == '__main__':
    main()
