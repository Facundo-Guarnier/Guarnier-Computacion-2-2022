import socket, pickle, argparse

def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="port")
    parser.add_argument("-d", required=True, help="direccion")
    return parser.parse_args()


def abrir_socket(args):
    host = args.d
    port = args.p

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(host + ":" + str(port))
    s.connect((host, port))
    return s


def main():
    args = argumentos()

    s = abrir_socket(args)

    while True:
        msg1 = input("Cliente: ")
        msg1 = pickle.dumps(msg1)     #De normal a bits
        s.send(msg1)

        msg2 = s.recv(10000)
        msg2 = pickle.loads(msg2)   #De bits a normal

        if pickle.loads(msg1).lower() == "exit":
            print("Servidor:", msg2)
            s.close()
            exit()
            

        if msg2["error"] == "":
            print("Servidor OK:\n", msg2["salida"])
        else:
            print("Servidor ERROR:\n", msg2["error"])


if __name__ == '__main__':
    main()
    
