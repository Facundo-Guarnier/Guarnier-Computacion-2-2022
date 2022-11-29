"""
    Escriba un programa cliente/servidor en python que permita ejecutar comandos GNU/Linux 
    en una computadora remota.

    Técnicamente, se deberá ejecutar un código servidor en un equipo “administrado”, y 
    programar un cliente (administrador) que permita conectarse al servidor mediante 
    sockets STREAM.

    El cliente deberá darle al usuario un prompt en el que pueda ejecutar comandos 
    de la shell.

    Esos comandos serán enviados al servidor, el servidor los ejecutará, y retornará 
    al cliente:

        > La salida estándar resultante de la ejecución del comando
        > La salida de error resultante de la ejecución del comando.
        
    El cliente mostrará en su consola local el resultado de ejecución del comando 
    remoto, ya sea que se haya realizado correctamente o no, anteponiendo un OK o 
    un ERROR según corresponda.

    El servidor debe atender solicitudes utilizando sockets de alto nivel con 
    serversocket.

    El servidor debe poder recibir las siguientes opciones:
        
        -p <port>: puerto donde va a atender el servidor.
        
        -c p | t : modo de concurrencia. Si la opción es "-c p" el servidor generará 
        un nuevo proceso al recibir conexiones nuevas. Si la opción es "-c t" 
        generará hilos nuevos.
    
    El cliente debe poder recibir las siguientes opciones:

        -h <host> : dirección IP o nombre del servidor al que conectarse.
        -p <port> : número de puerto del servidor.
        
    Para leer estos argumentos se recomienda usar módulos como argparse o click.
"""

import socketserver, pickle, subprocess, argparse

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("+-------------------------------------+")
        print("| Nuevo cliente {}  |".format(self.client_address))
        print("+-------------------------------------+")

        while True:
            msg1 = self.request.recv(1024)
            msg1 = pickle.loads(msg1)
            if msg1 == "exit":
                print("  Cliente {} saliendo...".format(self.client_address))
                self.request.sendall(pickle.dumps("Saliendo..."))
                # sock.close()    #Como cierro el socket??
                break

            else:
                msg2_diccionario = ejecutor(msg1)
                msg2_diccionario = pickle.dumps(msg2_diccionario)   #De normal a bits 
                self.request.sendall(msg2_diccionario)


class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def ejecutor(msg1):
    p = subprocess.Popen(msg1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True, bufsize=10000)
    salida, error = p.communicate()
    return {"salida":salida, "error":error}


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="port")
    parser.add_argument("-c", type=str, required=True, help="concurrencia", choices=["p", "t"])
    return parser.parse_args()

# def server_close(server):
#     while True: 
#         print("'server_close' para finalizar el server.")
#         texto = sys.stdin.readline()
#         # print(texto)
#         if texto == "server_close\n":
#             print("Server cerrado")
#             server.shutdown()
#             break


def abrir_socket_procesos(args):
    host = "0.0.0.0"
    port = args.p
    socketserver.TCPServer.allow_reuse_address = True
    server = ForkedTCPServer((host, port), MyTCPHandler)
    # threading.Thread(target=server_close, args=(server,)).start()
    server.serve_forever()


def abrir_socket_hilos(args):
    host = "0.0.0.0"
    port = args.p

    socketserver.TCPServer.allow_reuse_address = True
    with ThreadedTCPServer((host, port), MyTCPHandler) as server:
        server.serve_forever()


def main():
    args = argumentos()
    if args.c == "p":
        print("++++++++++++++ Procesos +++++++++++++++")
        abrir_socket_procesos(args)
    elif args.c == "t":
        print("++++++++++++++++ Hilos ++++++++++++++++")
        abrir_socket_hilos(args)
  

if __name__ == "__main__":    
    main()
