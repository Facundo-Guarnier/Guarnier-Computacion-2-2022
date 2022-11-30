Juego de Batalla Naval: 

El servidor es el encargado de:
	> Un nuevo proceso (multiprocessing) encargado de las conexiones y de las partidas.
	> Establecer múltiples conexiones utilizando hilos del proceso anteriormente mencionado.
	> Cada 2 jugadores/conexiones se crea un nuevo hilo para realizar una partida.
	> Los 3 hilos relacionados para la partida se comunican via queue.
	> Un nuevo proceso (multiprocessing) para utilizar una BD (almacenar resultado de los jugadores) mediante AsyncIO.
	> La comunicacion entre los 2 procesos (de partida y de BD) es a travez de multiprocessing.Pipe() 

El servidor recibe por parámetro: 
	> Cantidad máxima de jugadores simultáneos.
	> Ubicación de la BD
	> IP
	> Puerto

El cliente recibe por parámetro:
	> Nickname
	> IP del server
	> Puerto del server

El cliente define la posición de sus barcos, luego queda en espera a que el servidor lo empareje con otro jugador y finalmente jugar a "Batalla Naval".

Cada hilo de conexion se guarda en un diccionario, que contiene diccionarios donde indica los estados de los 
jugadores (jugando/en espera) y su queue para comunicarse con otro jugador: 
	{
	    "Jugador1": {
	        "Hilo": ...
	        "Estado": jugando
	        "queue": ...
	    },
	    "Jugador2": {...},
	}