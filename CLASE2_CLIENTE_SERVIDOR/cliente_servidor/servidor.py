import socket

"""socket.AF_INET es el dominio del conector. En este caso un conector IPv4"""
"""socket.SOCK_STREAM envia los paquetes en orden"""
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Ip_Servidor = '127.0.0.1'
Puerto = 1234

"""La funcion bind crea un oyente que espera la conexion al servidor """
socket_server.bind((Ip_Servidor,Puerto))

"""La funcion listen acepta el numero de clientes posibles que puede aceptar el servidor"""
Clientes = 2

socket_server.listen(Clientes)

"""La funcion .accept() crea dos objetos. En este caso la variable ID_SOCKET_CLIENTE almacena la informacion
   que llega y direccion es una lista de los clientes conectados"""

ID_SOCKET_CLIENTE, direccion = socket_server.accept()

while True:

    """La funccion .recv() espera hasta que llegue un mensaje"""
    bytes_a_recibir = 1024
    mensaje_recibido = ID_SOCKET_CLIENTE.recv(bytes_a_recibir)
    """La funcion .decode permite realizar un cambio de formato (bytes-str)"""
    texto = mensaje_recibido.decode("utf-8")

    if texto == "Cerrar":
        break
    else:
        print(str(direccion) + "envió", texto)

    """Enviar mensaje al cliente """

    Mensaje_envio = "Enviado"
    ID_SOCKET_CLIENTE.send(Mensaje_envio.encode())

print("TERMINO LA APLICACION")

"""Cerrar instancias de socket"""
ID_SOCKET_CLIENTE.close()
socket_server.close()