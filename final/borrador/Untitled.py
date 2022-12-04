
import multiprocessing, time, os

def proceso():
    while True:
        print("  Proceso 'Proceso' ID:", os.getpid())
        time.sleep(5)



print("ID proceso padre:", os.getpid())
pro =  multiprocessing.Process(target=proceso)
pro.start()
print("Esta es la ID de 'pro':", pro.pid)
print("Esta es la Ident de 'pro'", pro.ident)

time.sleep(16)
print("Matando al proceso")
# pro.kill()
# pro.terminate()
print("Padre esperando...")
time.sleep(10)
print("FIN")
