import socket

HOST = '127.0.0.1'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hola, mundo')
    data = s.recv(1024)
    
    while len(data) > 0:
        # procesar datos recibidos
        print(data)
        data = s.recv(1024)
        
    # cerrar la conexión
    s.close()