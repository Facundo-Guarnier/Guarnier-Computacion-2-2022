import socket, sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# host = sys.argv[1]
# port = int(sys.argv[2])

host = "0.0.0.0"
port = 5000

print(host + ":" + str(port))
s.connect((host, port))

while(1):
    msg = input("Cliente: ")
    s.send(msg.encode("ascii"))
    
    msg2 = s.recv(1024)
    print("Servidor:", msg2.decode("ascii"))
    
    if msg.lower() == "exit":
        s.close()
        exit()
