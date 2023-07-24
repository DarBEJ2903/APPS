import socket

socket_Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Ip_Servidor = "127.0.0.1"
Puerto = 1234
socket_Server.bind((Ip_Servidor,Puerto))

"""Esta estructura de codigo permite conectar más de un cliente"""
Clientes = 2
socket_Server.listen(Clientes)
conexiones = 2

Lista_Id_socket_Clientes = []
Lista_Direcciones = []

"""Este for anida la cantidad de clientes que se conecten"""

for conexiones in range (Clientes):

    paquete,direccion = socket_Server.accept()
    Lista_Id_socket_Clientes.append(paquete)
    Lista_Direcciones.append(direccion)

while True:

    bytes_a_recibir = 1024
    conexiones = 2
    texto = ' '

    """Este for escanea de manera secuencial el socket"""
    for conexiones in  range(Clientes):

        Mensaje_recibido = Lista_Id_socket_Clientes[conexiones]
        Mensaje_recibido = Mensaje_recibido.recv(bytes_a_recibir)
        texto =  Mensaje_recibido.decode('utf-8')
        print(str(Lista_Direcciones[conexiones])+ "envio" , texto)

    if texto == "Cerrar" :
        break

print("termino la plicacion")

"""Cerrar instancias de socket (En este caso se realiza con un for dada la cantidad de clientes)"""

conexiones = 2

for conexiones in range(Clientes):
    Lista_Id_socket_Clientes[conexiones].close()

socket_Server.close()
