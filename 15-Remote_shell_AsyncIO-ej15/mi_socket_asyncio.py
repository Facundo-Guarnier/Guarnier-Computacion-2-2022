"""
    Escriba un programa cliente/servidor en python que permita ejecutar comandos GNU/Linux en una computadora remota.

    Técnicamente, se deberá ejecutar un código servidor en un equipo “administrado”, y programar un cliente (administrador) 
    que permita conectarse al servidor mediante sockets STREAM.

    El cliente deberá darle al usuario un prompt en el que pueda ejecutar comandos de la shell.

    Esos comandos serán enviados al servidor, el servidor los ejecutará, y retornará al cliente:
        > La salida estándar resultante de la ejecución del comando.
        > La salida de error resultante de la ejecución del comando.

    El cliente mostrará en su consola local el resultado de ejecución del comando remoto, ya sea que se haya realizado 
    correctamente o no, anteponiendo un OK o un ERROR según corresponda.

    El servidor debe poder recibir las siguientes opciones:
        > -p <port>: puerto donde va a atender el servidor.
    
    El servidor deberá poder atender varios clientes simultáneamente utilizando AsyncIO.

    El cliente debe poder recibir las siguientes opciones:
        > -h <host> : dirección IP o nombre del servidor al que conectarse.
        > -p <port> : número de puerto del servidor.
    
    Para leer estos argumentos se recomienda usar módulos como argparse o click.
"""

import subprocess, argparse, asyncio, pickle

#! decode = loads -> de bits a normal
#! encode = dumps -> de normal a bits

def ejecutor(msg1):
    p = subprocess.Popen(msg1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True, bufsize=10000)
    salida, error = p.communicate()
    return {"salida":salida, "error":error}


def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="port")
    return parser.parse_args()


async def handle_echo(reader, writer):
    
    print("+---------------------------------------+")
    print("|  Nuevo cliente {}   |".format(writer.get_extra_info('peername')))
    print("+---------------------------------------+")
    while True:
        msg1 = await reader.read(100)
        msg1 = pickle.loads(msg1)

        if msg1 == "exit":
            print("+---------------------------------------+")
            print("| Cliente saliendo {} |".format(writer.get_extra_info('peername')))
            print("+---------------------------------------+")
            writer.write(pickle.dumps("Saliendo..."))
            await writer.drain()
            break

        else:
            msg2_diccionario = ejecutor(msg1) 
            msg2_diccionario = pickle.dumps(msg2_diccionario)

            writer.write(msg2_diccionario)
            await writer.drain()
    writer.close()


async def main():
    args = argumentos()
    host = "127.0.0.1"
    server = await asyncio.start_server(handle_echo, host, args.p)

    async with server:
        print("Tarea: {}".format(asyncio.current_task().get_name()))
        print("+---------------------------------------+")
        print("|  Server creado ('{}', {})    |".format(host, args.p))
        print("+---------------------------------------+")
        await server.serve_forever()
        

if __name__ == '__main__':
    asyncio.run(main())