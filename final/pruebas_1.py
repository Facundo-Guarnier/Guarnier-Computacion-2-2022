import socket, threading, time
from app.server.cliente import C_Cliente

host = "0.0.0.0"
port = 5000



def f_cliente(cli):
    cli.espera = "tu vieja"
    time.sleep(3)
    cli.espera = "tu vieja2"
    time.sleep(3)
    cli.espera = "tu vieja3"
    time.sleep(3)
    cli.espera = "tu vieja4"
    


def aceptar2_cliente(server):
    
    i = 0
    while i < 2:
        # s2,addr = server.accept()  

        s2 = "el socket"
        addr = ["la ip", "el puerto"]
        
        global cliente_objeto
        nickname = "Jugador" + str(i+1)
        cliente_objeto.append(C_Cliente(s2, addr, nickname))
        
        
        threading.Thread(target=f_cliente, args=(cliente_objeto[i],)).start()
        #! Estoy probando si el objeto de la lista al modificarlo en el hilo, en la lista tambien se modifica.
    
        i += 1
    
    global cliente_en_espera
    cliente_en_espera =[]
    cliente_en_espera.append(cliente_objeto[1])
    
    
    

def main():    

    s = "el server"

    global cliente_objeto
    cliente_objeto = []
    
    
    global cliente_en_espera
    cliente_en_espera =[]
    
    threading.Thread(target=aceptar2_cliente, args=(s,)).start()
    
    while True:
        time.sleep(2)
        print("Objeto: ", cliente_objeto[0], cliente_objeto[1])
        print("En espera: ", cliente_en_espera[0])
        print("++++++++++++++++++++++++++++++++++")
        
    
    
if __name__ == '__main__':
    main()