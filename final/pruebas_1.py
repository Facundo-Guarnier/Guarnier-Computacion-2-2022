import socket, threading, time
from app.server.cliente import C_Cliente

host = "0.0.0.0"
port = 5000



def f_cliente(cli):
    cli.espera = "tu vieja"
    


def aceptar2_cliente(server):
    
    i = 0
    while i < 2:
        # s2,addr = server.accept()  

        s2 = "el socket"
        addr = ["la ip", "el puerto"]
        
        global clientes_objeto
        nickname = "Jugador" + str(i+1)
        clientes_objeto.append(C_Cliente(s2, addr, nickname))
        
        
        threading.Thread(target=f_cliente, args=(clientes_objeto[i],)).start()
        #! Estoy probando si el objeto de la lista al modificarlo en el hilo, en la lista tambien se modifica.
    
        i += 1
    
    global cliente_en_espera
    cliente_en_espera =[]
    cliente_en_espera.append(clientes_objeto[1])
    
    
    

def main():    

    s = "el server"

    global clientes_objeto
    clientes_objeto = []
    
    
    global cliente_en_espera
    cliente_en_espera =[]
    
    threading.Thread(target=aceptar2_cliente, args=(s,)).start()
    
    time.sleep(2)
    print("Objeto: ", clientes_objeto)
    print("++++++++++++++++++++++++++++++++++")
        
        
    for cliente in clientes_objeto:
        if cliente.nickname == "Jugador1":
            clientes_objeto.remove(cliente)
    print("Objeto: ", clientes_objeto)
    
    
    
if __name__ == '__main__':
    main()