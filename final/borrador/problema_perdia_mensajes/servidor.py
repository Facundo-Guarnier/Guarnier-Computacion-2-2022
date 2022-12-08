import socket, pickle, time, json, marshal, pandas, pickle5

host = "0.0.0.0"
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print("Server 'ON' <" + host + ": " + str(port) + ">")
s.listen()

s2,addr = s.accept()

dataframe = pandas.DataFrame(columns=["1"], index = ["A","B","C","D","E","F","G","H","I","J"])


while True:
    lista = []
    
    msg2 = input("=> ")
    
    lista.append(msg2)
    lista.append(dataframe)
    
    
    
    # s2.send(pickle.dumps(msg2))           #! Con perdida de mensajes
    # s2.send(marshal.dumps(lista))         #! No soporta DataFrame
    # s2.send(lista.encode())               #! Sin perdida de mensajes pero no soporta listas ni diccionarios.
    # s2.send(json.dumps(lista).encode())   #! Sin perdida de mensajes, si soporta listas y diccionarios pero no soporta pandas.DataFrame()
    s2.send(pickle5.dumps(msg2))           #! Con perdida de mensajes