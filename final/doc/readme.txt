Juego de Batalla Naval: 

El servidor es el encargado de:
	> Un nuevo proceso (multiprocessing) encargado de las conexiones y de las partidas.
	> Un hilo es encargado de establecer múltiples conexiones, cada una utilizando un hilo.
	> Cada 2 jugadores/conexiones se crea un nuevo hilo para realizar una partida.
	> Los 3 hilos (2 clientes y 1 partida) relacionados para la partida se comunican via queue, event y punto de encuentro (Barrier).
	> Al momento de establecer partida, se establecen los tableros con los barcos de cada jugador. La distribución de los mismos es de forma aleatoria. 
	> Un nuevo proceso (multiprocessing) para utilizar una BD (almacenar resultado de los jugadores) mediante la utilización de AsyncIO.
	> La comunicación entre los 2 procesos (de partida y de BD) es a través de multiprocessing.Pipe().

El servidor recibe por parámetro: 
	> Cantidad máxima de jugadores simultáneos.
	> Ubicación de la BD
	> IP
	> Puerto

El cliente recibe por parámetro:
	> Nickname
	> IP del server
	> Puerto del server


Una ves iniciado el cliente, este espera a que el servidor lo empareje con otro jugador, luego recibe la posición de 
sus barcos de forma aleatoria de parte del servidor para empezar a jugar a "Batalla Naval". El cliente visualiza la partida 
mediante una interfaz grafica utilizando 'tkinter'.


Cada vez que se establece conexión con un nuevo cliente, el hilo encargado de las conexiones guarda en un diccionario 
de diccionarios los siguientes parámetros:
	{
	    "Jugador1": {
	        "s2": socket
	        "espera": True/False
	        "queue": queue.Queue(maxsize=1)
			"e1": threading.Event()
			"pe": threading.Barrier(2) 
	    },
	    "Jugador2": {...},
	}

donde indica los estados de los jugadores y las herramientas necesarias para la comunicación y sincronización con el servidor: 