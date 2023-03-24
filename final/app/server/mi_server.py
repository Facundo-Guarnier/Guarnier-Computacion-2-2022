import socket, threading, os, multiprocessing, argparse, queue, time, signal, random, pickle, re
import pandas as pd
from cliente import C_Cliente

# https://stackoverflow.com/questions/3991104/very-large-input-and-piping-using-subprocess-popen

#! [msg, tablero1, tablero2, estado]
def enviar_mensaje(s, m):
    # print("Mensaje enviado:",m)
    s.send(pickle.dumps(m))


def recibir_mensaje(s):
    mensaje = s.recv(10000) 
    # print("Mensaje recibido:", mensaje)
    return pickle.loads(mensaje)


#* Un hilo para cada uno de los clientes.
def f_cliente(cli):   
    print("  Hilo 'Conexion' ID:", threading.get_native_id())

    mensaje = cli.q1.get()
        
    if "1" == mensaje[3][1]: 
        enviar_mensaje(cli.s1, mensaje)
        jugador1(cli.s1, cli.q1, cli.e1, cli.pe)
        
    elif "2" == mensaje[3][1]:
        enviar_mensaje(cli.s1, mensaje)
        jugador2(cli.s1, cli.q1, cli.e1, cli.pe)
    
    else:
        print("error-s8")


def jugador1(sock, q1, e1, pe):
    while True:
        #! Empieza el jugador1
        while True:     #! Bucle si es que existe un error en el estado.
            msg1 = recibir_mensaje(sock)
                    
            q1.put(msg1)     #* Pone el mensaje en la cola
            
            pe.wait()       #* Espera al hilo partida a que llegue al punto de encuentro (que ya pueda leer q1).
            
            e1.wait()       #* Espera a que suceda el evento (procesar el disparo y poner los resultados en q1).
            e1.clear()
            
            msg2 = q1.get() #* Mensaje del resultado del disparo.
            
            enviar_mensaje(sock, msg2)
            
            if msg2[3][0]:          
                if msg2[3][1] == "FIN":
                    print("Entraste en el pass del jugador1")
                    pass
                else:
                    break   #! Sale del bucle porque no hay error en el estado.
            
            elif not(msg2[3][0]):   #! Existe error. 
                print("hilo jugador1, existe error, me quedo en el bucle")    
                pass
        
        #! Desde acá deberia empezar el jugador2
        msg2 = q1.get()     #! Se queda esperando a que pueda conumir la respuesta al ataque del jugador 2 de la cola.
        enviar_mensaje(sock, msg2)


def jugador2(sock, q1, e1, pe):
    while True:
        #! Desde acá deberia empezar el jugador1
        msg2 = q1.get()     #! Mensaje desde el hilo 'Partida'. Ataque jugador 1.
        
        enviar_mensaje(sock, msg2)
        
        #! Desde acá deberia empezar el jugador2
        while True:     #! Bucle si es que existe un error en el estado.

            msg1 = recibir_mensaje(sock)
            
            q1.put(msg1)
            
            pe.wait()
            
            e1.wait()
            e1.clear()
            
            msg2 = q1.get() #Mensaje desde el hilo 'Partida'
            
            enviar_mensaje(sock, msg2)
            
            
            if msg2[3][0]:          #! Sale del bucle porque no hay error en el estado.
                if msg2[3][1] == "FIN":
                    pass
                else:
                    break
            
            elif not(msg2[3][0]):   #! Existe error. 
                print("hilo jugador2, existe error, me quedo en el bucle")    
                pass


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=False, help="port", default=5000)
    return parser.parse_args()


def abrir_socket(args):
    host = "0.0.0.0"
    port = args.p

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    print("Padre ID:", os.getpid())
    print("Server 'ON' <" + host + ": " + str(port) + ">")
    s.listen()
    return s


#TODO Conexion con la BD
def base_datos():
    pass


#* Hilo de para aceptar.
def aceptar_cliente(server):
    print("  Hilo 'Aceptar_cliente' ID:", threading.get_native_id())
    
    i = 0
    while True:
        s2,addr = server.accept()
        print("-------------------------------------")
        print("  Nuevo cliente {}". format(addr))
        print("  Proceso padre ID:", os.getpid())
        
        global clientes_objeto
        nickname = "Jugador" + str(i+1)
        clientes_objeto.append(C_Cliente(s2, addr, nickname))
        
        threading.Thread(target=f_cliente, args=(clientes_objeto[i],)).start()
        
        i += 1


def matriz_inicial():
    matriz = []
    for y in range(10):         #! Filas
        matriz.append([])
        for x in range(10):     #! Columnas
            matriz[y].append(" ")
    return pd.DataFrame(matriz, index = ["A","B","C","D","E","F","G","H","I","J"])


def matriz_barco_random():
    matriz = matriz_inicial()
    contador_error = 0
    tipos = ["L", "F", "D", "S", "P"]  
    tamaño = 4
    # print("\n+++++++++++++++++++++ Nueva matriz +++++++++++++++++++++++++\nMatriz barco:\n", matriz)
    while len(tipos) > 0:
        barco = tipos.pop()
        n1 = random.randint(1, 2)
        barco = barco+str(n1)
        
        #! Horizontal
        if n1 == 1:
            estado = False
            while not(estado):
                x_inicio = random.randint(0, 9)
                y = random.randint(0, 9)
                x_final = x_inicio + tamaño     #Hacia la derecha
                derecha = True

                if x_final > 9 or x_final < 0:
                    x_final = x_inicio - tamaño #Hacia la izquerda
                    derecha = False
                
                # print("\n--------------------------------------------------------\nX incio {}, x fin {}, barco {}".format(x_inicio,x_final, barco))
                estado = True
                for i in range(tamaño+1):
                    if derecha:
                        if matriz.iloc[y, x_inicio+i] != " ":
                            estado = False
                            # print("Intento fallido de establecer el barco {} (error-s4)".format(barco))
                            contador_error += 1
                            
                    else:
                        if matriz.iloc[y, x_inicio-i] != " ":
                            estado = False
                            # print("Intento fallido de establecer el barco {} (error-s5)".format(barco))
                            contador_error += 1
                        
                # print("Estado {} del barco {}".format(estado, barco))
                if estado and derecha:
                    for i in range(tamaño+1):
                        matriz.iloc[y, x_inicio+i] = barco
                elif estado and not(derecha):
                    for i in range(tamaño+1):
                        matriz.iloc[y, x_inicio-i] = barco
                    
                    
                #! Para evitar que quede en un bucle de intentos fallidos
                if contador_error > 100:
                    matriz = matriz_inicial()
                    contador_error = 0
                    tipos = ["L", "F", "D", "S", "P"]  
                    tamaño = -1
                    estado = True
                    
            tamaño -= 1
            
        #! Vertical
        else:
            estado = False
            while not(estado):
                y_inicio = random.randint(0, 9)
                x = random.randint(0, 9)
                y_final = y_inicio + tamaño     #Hacia abajo
                abajo = True
                if y_final > 9 or y_final < 0:
                    y_final = y_inicio - tamaño #Hacia arriba
                    abajo = False
                    
                # print("\n--------------------------------------------------------\nY incio {}, Y fin {}, barco {}".format(y_inicio,y_final, barco))
                estado = True
                for i in range(tamaño+1):
                    if abajo:
                        if matriz.iloc[y_inicio+i, x] != " ":
                            estado = False
                            # print("Intento fallido de establecer el barco {} (error-s6)".format(barco))
                            contador_error += 1
                        else:
                            if matriz.iloc[y_inicio-i, x] != " ":
                                estado = False
                                # print("Intento fallido de establecer el barco {} (error-s7)".format(barco))
                                contador_error += 1
                        
                # print("Estado {} del barco {}".format(estado, barco))
                if estado and abajo:
                    for i in range(tamaño+1):
                        matriz.iloc[y_inicio+i, x] = barco
                elif estado and not(abajo):
                    for i in range(tamaño+1):
                        matriz.iloc[y_inicio-i, x] = barco
                
                
                #! Para evitar que quede en un bucle de intentos fallidos
                if contador_error > 100:
                    matriz = matriz_inicial()
                    contador_error = 0
                    tipos = ["L", "F", "D", "S", "P"]  
                    tamaño = -1
                    estado = True
                    
            tamaño -= 1
            
    return matriz


#* Un hilo para cada partida (cada 2 jugadores).
def partida(jugadores):
    print("  Hilo 'Partida' ID:", threading.get_native_id())

    q_jugador1 = jugadores[0].q1
    q_jugador2 = jugadores[1].q1
    
    e_jugador1 = jugadores[0].e1
    e_jugador2 = jugadores[1].e1
    
    pe_jugador1 = jugadores[0].pe
    pe_jugador2 = jugadores[1].pe

    
    #! tablero = {disparos_enemigos:DataFrame , mis_barcos:DataFrame, cant_hundidos:Int}
    tablero1 = {"disparos_enemigos": matriz_inicial(), "mis_barcos": matriz_barco_random(), "cant_hundidos": 0}     
    tablero2 = {"disparos_enemigos": matriz_inicial(), "mis_barcos": matriz_barco_random(), "cant_hundidos": 0}
    

    #! Avisar a los jugadores que se encontró partida y quien es el jugador 1 y el 2.
    q_jugador1.put(["Ningun mensaje", tablero1, tablero2,  [True, "1"]])
    q_jugador2.put(["Ningun mensaje", tablero2, tablero1, [True, "2"]])
    
    #! Siempre empieza el jugador 1. 
    while True:

        #! Desde acá empieza el jugador1.
        #! Se tiene que quedar en el bucle hasta que en el estado no exitstan errores (error-s1).
        while True:
            pe_jugador1.wait()          #! Espera a que el hilo jugador ponga el texto introducido por el usuario.
            
            msg1 = q_jugador1.get()     #! Lee el texto de el usuario.
            
            msg1, tablero1, tablero2, estado = jugada(msg1, tablero1, tablero2)     #! Procesar el texto del primer jugador.
            
            q_jugador1.put([msg1, tablero1, tablero2, estado])      #! Enviar los resultados a los hilos jugadores.
            
            e_jugador1.set()        #! Establece que ya terminó de procesar y de poner los elementos en la cola. 
        
            if estado[0]:           #! Sale del bucle porque no hay error en el estado.
                q_jugador2.put([msg1, tablero2, tablero1, estado])      #! Envia el resultado ya correcto, no envia al otro jugador todos los erores.
                break

            elif not(estado[0]):    #! Existe error, por lo tanto se queda en el bucle del jugador.    
                pass    #! Solo para representar cuando hay error, no tiene ninguna funcion real.

        
        if estado[1] == "FIN":      #! Fin de la partida.
            break   #! Sale del bucle de turnos para iniciar el fin de la partida.
        
        
        #! Desde acá empieza el jugador2.
        #! Se tiene que quedar en el bucle hasta que en el estado no exitstan errores (error-s1).
        while True:
            pe_jugador2.wait()          #! Espera a que el hilo jugador ponga el texto introducido por el usuario.
            
            msg1 = q_jugador2.get()     #! Lee el texto de el usuario.

            msg1, tablero2, tablero1, estado = jugada(msg1, tablero2, tablero1)     #! Procesar el texto del primer jugador.
            
            q_jugador2.put([msg1, tablero2, tablero1, estado])      #! Enviar los resultados a los hilos jugadores.
                
            e_jugador2.set()        #! Establece que ya terminóde procesar y poner los elementos en la cola. 
        
            if estado[0]:           #! Sale del bucle porque no hay error en el estado.
                q_jugador1.put([msg1, tablero1, tablero2, estado])  
                break
            
            elif not(estado[0]):    #! Existe error, por lo tanto se queda en el bucle del jugador.    
                pass    #! Solo para representar cuando hay error, no tiene ninguna funcion real.


        if estado[1] == "FIN":      #! Fin de la partida.
            break   #! Sale del bucle de turnos para iniciar el fin de la partida.
    
    
    threading.Thread(target=fin_partida, args=(jugadores[0],)).start()
    threading.Thread(target=fin_partida, args=(jugadores[1],)).start()
        

#! Fin de la partida por cada jugador.
#! Anuncia al ganador y pregutar al cliente si desean finalizar la conexion o jugar otra vez.
#! Al cliente le llegará un mensaje por el metedo recv() con longitud cero. Cuando esto  
#! suceda, el cliente deberia cerrar su conexion con el .close() para liberar recursos.
def fin_partida(jugador):
    
    global clientes_objeto
    
    print("Entraste en fin_partida", jugador.nickname)
    
    #! Jugador1
    
    print("Antes del pe", jugador.nickname)
    jugador.pe.wait()       #! Espera a que el hilo jugador ponga el texto introducido por el usuario.
    print("Despues del pe", jugador.nickname)
    
    msg1 = jugador.q1.get()     #! Lee el texto de el usuario. 
    
    print("MENSAJE: ", msg1)
    
    if msg1=="continuar": 
        print("Entraste en continuar", jugador.nickname)
        jugador.q1.put(["Buscando proxima partida...", "", "", [True, "Continuar"]])      #! Enviar los resultados al hilo jugador.
        jugador.e1.set()        #! Establece que ya terminó de procesar y de poner los elementos en la cola. 
        
        jugador.espera = True
        #TODO Resetiar todo los atributos.
    
    elif msg1=="salir":
        print("Entraste en salir", jugador.nickname)
        jugador.q1.put(["finalizando y desconectando...", "", "", [False, "Desconexion"]])      #! Enviar los resultados al hilo jugador.
        jugador.e1.set()        #! Establece que ya terminó de procesar y de poner los elementos en la cola. 
        jugador.s2.close()
        
        #! Busca y elimina al jugador de la lista de jugadores.
        for cliente in clientes_objeto:
            if cliente.nickname == jugador.nickname:
                clientes_objeto.remove(cliente)



#! Procesamiento del disparo
#! Tiene que devolver [mensaje, tabelro1, tablero2, estado]     (Estado = [True/False, descripcion])
#! Errores: s1=Valores no validos, s2=Valores fuera de rango, s3=Disparo ya realizado, 
#! tablero = {disparos_enemigos:DataFrame , mis_barcos:DataFrame, cant_hundidos:Int}
def jugada(msg, tablero1, tablero2):
    
    codificacion = str.maketrans(
        'ABCDEFGHIJ',
        "0123456789",
        )
    
    #* 1 - Revisar que el disparo (A1) sea coherente (menor a 10 y a J).
    try:
        fila = int(msg[0].translate(codificacion))
        columna = int(msg[1])
    except:
        return "Valores no validos", tablero1, tablero2, [False, "error-s1"]
    
    if (fila > 9 or fila < 0 or columna > 9 or columna < 0):
        return "Valores fuera de rango", tablero1, tablero2, [False, "error-s2"]
    


    #* 2 - Revisar si ya se disparó en ese lugar (comprobar en disparos_enemigos en tablero 2).
    if tablero2["disparos_enemigos"].iloc[fila, columna] != " ":
        return "Disparo realizado con aterioridad", tablero1, tablero2, [False, "error-s3"]
    
    
    #* 3 - Comprobar si le dió a un barco y Guardar Tocado o Agua respectivamente.
    if tablero2["mis_barcos"].iloc[fila, columna] == " ":
        tablero2["disparos_enemigos"].iloc[fila, columna] = "A"
        return "AGUA!! El disparo fue errado.", tablero1, tablero2, [True, "Agua"]
    
    else:
        tablero2["disparos_enemigos"].iloc[fila, columna] = "T"     #! Tocado
        
        #* 3.1 - Revisar si el barco está undido. 
        #! Barco hundido
        #! Contar sobre el eje 'X' o sobre el eje 'Y' si hay x cantidad de tocados partiendo desde msg
        if (es_hundido(fila, columna, tablero2)):
            tablero2["cant_hundidos"] = tablero2["cant_hundidos"] + 1
        
            #* 3.2 - Comprobar si se hundieron todos los barcos.
            # if tablero2["cant_hundidos"] >= 5:
            if tablero2["cant_hundidos"] >= 1:
                return "Todos los barcos han sido hundidos!!!", tablero1, tablero2, [True, "FIN"]
        
            else:
                return "HUNDIDO!! El disparo fue certero, {} fuen hundido.".format(tipo_barco(tablero2["mis_barcos"].iloc[fila, columna])), tablero1, tablero2, [True, "Hundido"]

        #! Barco no hundido
        else:
            return "TOCADO!! El disparo fue certero, {} afectado.".format(tipo_barco(tablero2["mis_barcos"].iloc[fila, columna])), tablero1, tablero2, [True, "Tocado"]


def es_hundido(fila, columna, tablero2):
    tipo_barco = tablero2["mis_barcos"].iloc[fila, columna]
    tamaño_barco = 0
    tamaño_tocado = 0
    #! Barcos verticales
    if "2" in tipo_barco:
        for x in range(10):
            if tablero2["mis_barcos"].iloc[x, columna] == tipo_barco:
                tamaño_barco += 1
                if tablero2["disparos_enemigos"].iloc[x, columna] == "T":
                    tamaño_tocado += 1
        return tamaño_barco == tamaño_tocado

    #! Barcos horizontales
    else :
        for y in range(10):
            if tablero2["mis_barcos"].iloc[fila, y] == tipo_barco:
                tamaño_barco += 1
                if tablero2["disparos_enemigos"].iloc[fila, y] == "T":
                    tamaño_tocado += 1
        return tamaño_barco == tamaño_tocado


def tipo_barco(letra):
    #! 1 = horizontal
    #! 2 = vertical
    if letra == "P1" or letra == "P2":
        return "un Portaaviones"
    elif letra == "S1" or letra == "S2":
        return "un Submarino"
    elif letra == "D1" or letra == "D2":
        return "un Destructor"
    elif letra == "L1" or letra == "L2":
        return "una Lancha torpedera"
    elif letra == "F1" or letra == "F2":
        return "una Fragata"


#* Proceso juego.  
#! Acá tiene que agregar al diccionario las conexiones
def juego(server):
    print("  Proceso 'Juego' ID:", os.getpid())
    
    global clientes_objeto
    clientes_objeto = []
    
    threading.Thread(target=aceptar_cliente, args=(server,)).start()

    #! Acá tiene que leer el diccionario y cada 2 en estado de espera crear una partida 
    while True:
        jugadores_espera = []
        
        #TODO Seccion critica?? Deberia ser accedido por un hilo a la vez (juego o aceptar_cliente).
        for cliente in clientes_objeto:
            if cliente.espera:
                jugadores_espera.append(cliente)
                
                #TODO Esta medio raro que hayan dos "if len() > 2:". Tener en cuenta que la variable jugadores_espera es pasada al hilo partida.
                if len(jugadores_espera) >= 2:
                    break
        
        
        if len(jugadores_espera) >= 2:
            print("++++++++++++++++++++ Se establecio una partida ++++++++++++++++++++")
            threading.Thread(target=partida, args=(jugadores_espera,)).start()

            for cliente in jugadores_espera:
                cliente.espera = False
        
            jugadores_espera = []
            

        else:
            print("++++++++++++++++++++ Esperando jugador nuevo ++++++++++++++++++++")
            print("  Total de jugadores:", len(clientes_objeto))
            print("  Jugadores en espera:", len(jugadores_espera))
            time.sleep(6)


def señal(nro_senial, marco):
    print("Finalizando el proceso ID:", os.getpid())
    os._exit(0)


def main():
    ar = argumentos()
    server = abrir_socket(ar)
    
    pid_padre = os.getpid()
    print("  Proceso main ID:", pid_padre)

    signal.signal(signal.SIGINT, señal)

    #! Proceso de todas las partidas y clienets
    p_juego = multiprocessing.Process(target=juego, args=(server,)).start()

    #! Proceso BD
    # p_bd = multiprocessing.Process(target=base_datos, args=())
    
    # ...
    #! Proceso main del servidor 
    # ...
    
    
if __name__ == '__main__':
    main()


#TODO: En orden de prioridades.
# Al momento de finalizar una partida y volver a empezar otra (escribir continuar) los roles de los jugadores se mezclan (los 2 son jugador 1 o algo asi)

#// Condicion de fin de la partida cuando se hunden todos los barcos, los clientes 
#// deberian terminan pero no lo hacen, el server detecta bien la condicion.

#// Que vuelva a jugar el mismo jugador cuando el disparo es en un lugar que ya disparó. 

#// Volver a dar el turno al jugador que se equivocó de coordenas (mal escritas). Esto deberia ser 
#// por lado del server y no del cliente. Hay una solucion propuesta desde el lado del cliente.

# El click del GUI quedó a medio camino.

# Como cerramos las conexiones.

#// Cambiar el diccionario cliente por una clase cliente.

# Cambiar la variable global clientes por una variable compratida entre hilos del mismo proceso.

# Separar los barcos un lugar a los costados, no se pueden estar tocando.

# Ver si se puede con IPv4 y v6.

# Usar MongoBD  .

# Cada usuario pueda poner su nickname personalizado.

# ¿Como borrar un cliente que se desconectó con "ctrl + c"?

# Poner una seccion critica a las variables globales
# Seccion critica??? En todo los lugares en que esté un q1 y e1.

# Investigar threading.RLock(), threading.BoundedSemaphore(), threading.Condition().

#//  Ver como matar al proceso "online" cuando muere el main. Señal de ctrl + c para que tambien se la envíe al hijo. 