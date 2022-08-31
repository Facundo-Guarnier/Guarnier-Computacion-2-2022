import socket, threading, os

def hilo(sock):
    print("  Hijo ID:", threading.get_native_id())
    while True:
        msg1 = sock.recv(1024)
        if msg1.decode() == "exit":
            print("Cliente saliendo...")
            sock.send("pepe".encode("ascii"))
            sock.close()
            break
        else:
            sock.send((msg1.decode().upper()).encode("ascii"))
            # sock.send((b"HTTP 200 OK \n"))
            # sock.close()
            # break

host = "0.0.0.0"
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))


print("Padre ID:", os.getpid())
print("Server 'ON' <" + host + ": " + str(port) + ">")

s.listen(1)

while True:
    s2,addr = s.accept()
    print("+++++++++++++++++++")
    print("  Nuevo cliente {}". format(addr))
    threading.Thread(target=hilo, args=(s2,)).start()