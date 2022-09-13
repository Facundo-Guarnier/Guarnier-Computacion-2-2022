import pickle, subprocess, argparse, concurrent.futures, socket

def handle(s2, addr):
    print("+-------------------------------------+")
    print("| Nuevo cliente {}  |".format(addr))
    print("+-------------------------------------+")

    while True:
        msg1 = s2.recv(1024)
        msg1 = pickle.loads(msg1)
        if msg1 == "exit":
            print("  Cliente {} saliendo...".format(addr))
            s2.send(pickle.dumps("Saliendo..."))
            break

        else:
            msg2_diccionario = ejecutor(msg1)
            msg2_diccionario = pickle.dumps(msg2_diccionario)   #De normal a bits 
            s2.send(msg2_diccionario)


def ejecutor(msg1):
    p = subprocess.Popen(msg1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True, bufsize=10000)
    salida, error = p.communicate()
    return {"salida":salida, "error":error}


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="port")
    parser.add_argument("-c", type=str, required=True, help="concurrencia", choices=["p", "t"])
    return parser.parse_args()


def main():
    args = argumentos()
    host = "0.0.0.0"
    port = args.p
    if args.c == "p":
        print("++++++++++++++ Procesos +++++++++++++++")
        excecutor = concurrent.futures.ProcessPoolExecutor(max_workers=9)       # Cuando se conecta un cliene, se crean todos los procesos (max_workers)
    elif args.c == "t":
        print("++++++++++++++++ Hilos ++++++++++++++++")
        excecutor = concurrent.futures.ThreadPoolExecutor(max_workers=9)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #Para utilizar el puerto cuando queda colgado. Esto se debe a que se intenta evitar un paquete viejo de una conexion pasada.
        s.bind((host, port))
        s.listen(5)
        while True:
            s2_cliente, addr = s.accept()
            excecutor.submit(handle, s2_cliente, addr)
  

if __name__ == "__main__":    
    main()