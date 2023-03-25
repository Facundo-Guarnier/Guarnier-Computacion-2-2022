# def partida(jugadores):
#     print("  Hilo 'Partida' ID:", threading.get_native_id())

#     j1, j2 = jugadores 

#     q_j1 = j1.q1
#     q_j2 = j2.q1
    
#     e_j1 = j1.e1
#     e_j2 = j2.e1
    
#     pe_j1 = j1.pe
#     pe_j2 = j2.pe

#     tablero1 = {"disparos_enemigos": matriz_inicial(), "mis_barcos": matriz_barco_random(), "cant_hundidos": 0}     
#     tablero2 = {"disparos_enemigos": matriz_inicial(), "mis_barcos": matriz_barco_random(), "cant_hundidos": 0}
    
#     #! Avisar a los jugadores que se encontró partida y quien es el jugador 1 y el 2.
#     q_j1.put(["Ningun mensaje", tablero1, tablero2,  [True, "1"]])
#     q_j2.put(["Ningun mensaje", tablero2, tablero1, [True, "2"]])
    
#     #! Bucle para todas las jugadas.
#     while True:

        #! Desde acá empieza el jugador1.
        #! Se tiene que quedar en el bucle hasta que en el estado no exitstan errores (error-s1).
        while True:
    
            # msg2, tablero1, tablero2, estado = turno(q_j1, e_j1, pe_j1, tablero1, tablero2)
        
            if estado[0]:           #! Sale del bucle porque no hay error en el estado.
                q_j2.put([msg2, tablero2, tablero1, estado])      #! Envia el resultado ya correcto, no envia al otro jugador todos los erores.
                break

            elif not(estado[0]):    #! Existe error, por lo tanto se queda en el bucle del jugador.    
                pass    #! Solo para representar cuando hay error, no tiene ninguna funcion real.

        
        if estado[1] == "FIN":      #! Fin de la partida.
            break   #! Sale del bucle de turnos para iniciar el fin de la partida.
        
        
        #! Desde acá empieza el jugador2.
        #! Se tiene que quedar en el bucle hasta que en el estado no exitstan errores (error-s1).
        while True:
            
            # msg2, tablero2, tablero1, estado = turno(q_j2, e_j2, pe_j2, tablero2, tablero1)

            if estado[0]:           #! Sale del bucle porque no hay error en el estado.
                q_j1.put([msg2, tablero1, tablero2, estado])  
                break
            
            elif not(estado[0]):    #! Existe error, por lo tanto se queda en el bucle del jugador.    
                pass    #! Solo para representar cuando hay error, no tiene ninguna funcion real.


        if estado[1] == "FIN":      #! Fin de la partida.
            break   #! Sale del bucle de turnos para iniciar el fin de la partida.
    
    
    threading.Thread(target=fin_partida, args=(j1,), name="Fin de partida 1").start()
    threading.Thread(target=fin_partida, args=(j2,), name="Fin de partida 2").start()
        