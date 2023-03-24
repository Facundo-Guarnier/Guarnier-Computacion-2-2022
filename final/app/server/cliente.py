"""
    Clase cliente con los siguientes atributos:
        > Nickname
        > Socket
        > Address
        > Event
        > Queue
        > Barrier
        > Espera (para saber si está en partida o buscando una)
"""        

import threading, queue


class C_Cliente:
    def __init__(self, socket, address, nickname):
        self.nickname = nickname
        self.s1 = socket
        self.ad = address                       #! [Ip, puerto]
        self.q1 = queue.Queue(maxsize=1)        #! Cola de elementos, es de tipo FIFO. Se está limitando a 1 elemento. 
        self.e1 = threading.Event()             #! Predeterminado es falso. Señala cuando se a producido un evento (un cambio de estado en el programa).
        self.pe = threading.Barrier(2)          #! Punto de encuentro de hilos, se detienen hasta que lleguen los necesarios (2 en este caso) a la barrera.
        # self.s1 = threading.Semaphore(3)      #! Contador de un numero limitado de recursos (seccion critica). Es este caso, hay 3 recursos disponibles.
        # self.l1 = threading.Lock()            #! Protege una seccion critica, inicia en abierto. Es un caso particular de Semaphore inicializado en 1.
        self.espera = True
        
    def __str__(self) -> str:
        return "< {} ({}:{}), {} >".format(self.nickname, self.ad[0], self.ad[1], self.espera)