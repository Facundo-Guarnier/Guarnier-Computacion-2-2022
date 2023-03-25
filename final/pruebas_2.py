continuar = True

while continuar:
    print("++++++++ Inicio bucle ++++++++")
    for i in [1,2]:
        a = input("{} Input: ".format(i))
        if a == "1":    #! Salir
            print("Entaste en el True", i)
            continuar = False
            break
        
        elif a == "2":  #! Continuar
            print("Entraste en el False", i)
            continuar = True
            break
    
    print("++++++++ Fin bucle ++++++++")