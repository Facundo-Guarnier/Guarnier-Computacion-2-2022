import threading, os

def caca():
    print(threading.get_native_id())

threading.Thread(target=caca).start()
print("padre",os.getpid())
