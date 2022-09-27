import socket

direcciones = []
direcciones.append(socket.getaddrinfo("localhost", 5000, socket.AF_INET6, 1)[0])
direcciones.append(socket.getaddrinfo("localhost", 5000, socket.AF_INET, 1)[0])

print("\n")
print(direcciones)
print("\n")