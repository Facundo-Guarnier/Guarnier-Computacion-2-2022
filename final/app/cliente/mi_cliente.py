import ipaddress
import socket, argparse, os, datetime, pickle, re
from mi_gui import gui

def hora_actual():
    return datetime.datetime.now().strftime("%H:%M:%S")


def detectar_tipo_ip(ip):
    try:
        ip = ipaddress.ip_address(ip)   #! Convierte la ip en un objeto de ipaddress.
        if isinstance(ip, ipaddress.IPv4Address):   #! Verifica si el objeto ip es una instancia de la clase ipv4address 
            return "IPv4"
        elif isinstance(ip, ipaddress.IPv6Address):     #! Verifica si el objeto ip es una instancia de la clase ipv6address
            return "IPv6"
        else:
            return False
    except ValueError:
        return False


#! Solo la casilla (Ej: B1, J9)
def enviar_mensaje(s, m):
    s.send(pickle.dumps(m))


def recibir_mensaje(s):
    mensaje = s.recv(100000) 
    return pickle.loads(mensaje)


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=False, help="Puerto", default= 5000)
    parser.add_argument("-d", required=False, help="Dirección IPv4 o  IPv6", default= "0.0.0.0")
    parser.add_argument("-n", type=str, required=False, help="Nickname", default= "Jugador")

    return parser.parse_args()


def abrir_socket(args):
    
    host = args.d
    port = args.p
    
    try:
        print("Server:", host + ":" + str(port))
        if detectar_tipo_ip(host) == "IPv4":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            enviar_mensaje(s, args.n)
            return s

        
        elif detectar_tipo_ip(host) == "IPv6":
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            s.connect((host, port))
            enviar_mensaje(s, args.n)
            return s

        else:
            print("Dirección ingresada no valida como IPv4 o IPv6")
            os._exit(0)

    except:
        print("No se puede establecer conexión, finalizando...")
        os._exit(0)


def enviar(s):
    er = r'[A-J][0-9]$'   #! Expresion regular para las coordenadas.

    while True:
        msg1 = input(f"[ C {hora_actual()} ] Coordenadas: ").upper()
        
        if re.match(er, msg1):        #! Coordenada correcta
            break
        
        else:
            print(f"[ C {hora_actual()} ] Coordenada inválida.")
    

    enviar_mensaje(s, msg1)


def print_mensaje(mensaje):
#! [msg1, tablero1, tablero2, estado]
    print("\n++++++++++++++++++++++++++++++++++++++++++++ PRINT ++++++++++++++++++++++++++++++++++++++++++++\n")
    print(f"[ S {hora_actual()} ]\n   Mensaje: {mensaje[0]}\n   Estado: {mensaje[3]}")       #!Mensaje al jugador
    print("\n-----Mis barcos: \n", mensaje[1]["mis_barcos"])
    print("\n-----Disparos enemigos: \n", mensaje[1]["disparos_enemigos"])
    print("\n-----Mis disparos: \n", mensaje[2]["disparos_enemigos"])
    print("\n++++++++++++++++++++++++++++++++++++++++++++ PRINT ++++++++++++++++++++++++++++++++++++++++++++\n")

#! Si el usuario quiere buscar otra partida o terminar y cerrar el juego.
def seguir_jugando(s):
    
    while True:
        msg1 = input(f"[ C {hora_actual()} ] Continuar o salir: ").lower()
        
        if msg1 == "continuar":
            print(f"[ C  {hora_actual()} ] Entraste en continuar")
            enviar_mensaje(s, msg1)
            mensaje = recibir_mensaje(s)        
            print(f"[ S {hora_actual()} ] {mensaje}")
            return True
        
        elif msg1 == "salir":
            print(f"[ C  {hora_actual()} ] Entraste en salir")
            enviar_mensaje(s, msg1)
            return False
        
        else: 
            print(f"[ C  {hora_actual()} ] Escribí bien bro...", msg1)


def juego(s):
    nueva_partida = True
    
    while nueva_partida: 
        
        mensaje = recibir_mensaje(s)        
        print_mensaje(mensaje)
        
        if mensaje[3][0] == False:  #! Error en el server.
            print(f"[ C {hora_actual()} ] ERROR EN EL SERVER ANTES DE SABER QUE JUGADOR SOS. {mensaje[3]}")
            break
        
        elif mensaje[3][1] == "1":    
            
            nueva_partida = jugador(s, [1,2])

        elif mensaje[3][1] == "2":  
            nueva_partida = jugador(s, [2,1])
            
        else:
            print(f"[ C {hora_actual()} ] ERROR INESPERADO EN EL SERVER.")
            break
    
    print("Finalizando ...")
    os._exit(0)


def jugador(s, orden):
    
    continuar_partida = True
    nueva_partida = False
    
    while continuar_partida:
        
        for turno in orden:     #! Turno del Jugador 1 y luego del Jugador 2.
            if turno == 1:
                respuesta = hacer_ataque(s)
            
            elif turno == 2:
                respuesta = recibir_ataque(s)
            
            if respuesta[3][1] == "FIN":
                print(f"[ C  {hora_actual()} ] FIN DE LA PARTIDA.")

                nueva_partida = seguir_jugando(s)       #! Buscar una nueva partida o no.
                continuar_partida = False               #! Terminar partida actual.
                break                                   #! Terminar turno actual. Sale del "for", por lo tanto, se reinicia el bucle. 
                
    return nueva_partida


def hacer_ataque(s):
    while True:     #! Bucle por si existe un error del server.
        enviar(s)   #! Envía las coordenadas ingresadas por el usuario.
        
        print("++ ESPERANDO RESPUESTA DEL SERVIDOR de mi ataque")
        respuesta = recibir_mensaje(s)      #! Estado de mi actaque al enemigo
        
        if respuesta[3][0]:     #! No existe error
            print("+++++++++++++++++++++ No hay error +++++++++++++++++++++")
            print_mensaje(respuesta)
            return respuesta
        
        else:       #! Existe error.
            print("+++++++++++++++++++++ Si hay error +++++++++++++++++++++")
            print_mensaje(respuesta)


def recibir_ataque(s):
    while True:     #! Bucle si es que existe un error del server.
        print("++ ESPERANDO RESPUESTA DEL SERVIDOR del ataque enemigo")
        respuesta = recibir_mensaje(s)
        
        if respuesta[3][0]:     #! No existe error
            print("+++++++++++++++++++++ No hay error +++++++++++++++++++++")
            print_mensaje(respuesta)
            return respuesta
        
        else:           #! Existe error.
            print("+++++++++++++++++++++ Si hay error +++++++++++++++++++++")
            print_mensaje(respuesta)


def main():
    args = argumentos()

    s = abrir_socket(args)
    
    juego(s)

    print(f"[ C Main {hora_actual()} ] Finalizando...")
    s.close()
    os._exit(0)


if __name__ == '__main__':
    main()
