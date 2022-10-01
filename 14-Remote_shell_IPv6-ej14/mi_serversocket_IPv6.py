
"""
    Modificar el código de shell remota realizado con anterioridad (socketserver) para que atienda en 
    todas las IP's del sistema operativo, independientemente de que se trate de IPv4 o IPv6.

    Lance un thread para cada socket.

    El servidor de shell debe mantener la concurrencia para atender a varios clientes, ya sea por 
    procesos o hilos, dependiendo del parámetro pasado por argumento "-c".
"""

import socketserver, threading, pickle, subprocess, argparse, socket


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
                break

            else:
                msg2_diccionario = ejecutor(msg1)
                msg2_diccionario = pickle.dumps(msg2_diccionario)
                self.request.sendall(msg2_diccionario)


class ForkedTCPServer4(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET
    pass

class ForkedTCPServer6(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass


class ThreadedTCPServer4(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET
    pass

class ThreadedTCPServer6(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
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


def abrir_socket_procesos(d):
    socketserver.TCPServer.allow_reuse_address = True
    if d[0] == socket.AF_INET:
        with ForkedTCPServer4(d[4], MyTCPHandler) as server:
            server.serve_forever()
    
    elif d[0] == socket.AF_INET6:
        with ForkedTCPServer6(d[4], MyTCPHandler) as server:
                server.serve_forever()


def abrir_socket_hilos(d):
    socketserver.TCPServer.allow_reuse_address = True
    if d[0] == socket.AF_INET:
        with ThreadedTCPServer4(d[4], MyTCPHandler) as server:
            server.serve_forever()
    
    elif d[0] == socket.AF_INET6:
        with ThreadedTCPServer6(d[4], MyTCPHandler) as server:
                server.serve_forever()


def main():
    args = argumentos()
    direcciones = []
    direcciones.append(socket.getaddrinfo("localhost", args.p, socket.AF_INET, 1)[0])
    direcciones.append(socket.getaddrinfo("localhost", args.p, socket.AF_INET6, 1)[0])

    if args.c == "p":
        print("++++++++++++++ Procesos +++++++++++++++")
        for d in direcciones:
            print("Server: ", d[4])
            threading.Thread(target=abrir_socket_procesos, args=(d,)).start()
            print("---------------------------------------")

    elif args.c == "t":
        print("++++++++++++++++ Hilos ++++++++++++++++")
        for d in direcciones:
            print("Server: ", d[4])
            threading.Thread(target=abrir_socket_hilos, args=(d,)).start()
            print("---------------------------------------")



if __name__ == "__main__":    
    main()
