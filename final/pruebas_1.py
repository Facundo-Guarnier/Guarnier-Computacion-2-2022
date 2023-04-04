import multiprocessing
import time


def proceso1(p):
    print("p1")
    p.send(["read","AAAAAAAAA"])
    p.send(["read","bBBBBBBBB"])
    a = p.recv()
    print(a)
    
    

def proceso2(p):
    print("p2")
    time.sleep(2)
    while p.poll():
        a = p.recv()
        print(a)
    time.sleep(2)
    p.send(["read","CCCCCCCCCCCCCC"])
    
    
def main():
    
    p1, p2 = multiprocessing.Pipe()

    h1 = multiprocessing.Process(target=proceso1, args=(p1,))
    h2 = multiprocessing.Process(target=proceso2, args=(p2,))
    
    h1.start()
    h2.start()
    h1.join()
    h2.join()
    print("FIN PADRE")

if __name__ == '__main__':
    main()