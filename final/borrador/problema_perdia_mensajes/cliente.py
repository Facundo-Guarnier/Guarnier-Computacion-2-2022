import socket, pickle, time, json, marshal, pandas, pickle5

host = "0.0.0.0"
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server:", host + ":" + str(port))
s.connect((host, port))

while True:
    time.sleep(2) # Simulando procesamiento
    mensaje = s.recv(1000000)        

    # print("[ Server ]", mensaje)
    # print("[ Server ]", pickle.loads(mensaje))            #! Con perdida de mensajes
    # print("[ Server ]", marshal.loads(mensaje))           #! No soporta DataFrame
    # print("[ Server ]", mensaje.decode())                 #! Sin perdidas de mensajes pero no soporta listas ni diccionarios.
    # print("[ Server ]", json.loads(mensaje.decode()))     #! Sin perdida de mensajes, si soporta listas y diccionarios pero no soporta pandas.DataFrame()
    print("[ Server ]", pickle5.loads(mensaje))            #! Con perdida de mensajes pero soporta todo