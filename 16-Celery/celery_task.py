from celery_confg import app
import math

@app.task
def raiz(filas_o):
    print("Trabajando raiz con:", filas_o)
    filas_r = []
    for fila_o in filas_o:
        fila_r = []
        for x in fila_o:
            a = math.sqrt(int(x))
            fila_r.append(a) 
        filas_r.append(fila_r)
        
    return filas_r

@app.task
def pot(filas_o):
    print("Trabajando potencia con:", filas_o)
    filas_r = []
    for fila_o in filas_o:
        fila_r = []
        for x in fila_o:
            a = int(x) * int(x) 
            fila_r.append(a) 
        filas_r.append(fila_r)
        
    return filas_r

@app.task
def log(filas_o):
    print("Trabajando logaritmo con:", filas_o)
    filas_r = []
    for fila_o in filas_o:
        fila_r = []
        for x in fila_o:
            a = math.log(int(x))
            fila_r.append(a) 
        filas_r.append(fila_r)
        
    return filas_r

def funcion_calculo(c,filas):   
    if c == "raiz":
        print("Raiz:")
        return raiz.delay(filas)
        
    elif c == "pot":
        print("Potencia:")
        return pot.delay(filas)
        
    elif c == "log":
        print("Logaritmo:")
        return log.delay(filas)
