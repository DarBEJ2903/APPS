# IMPORTANDO LIBRERIA SOCKET
import socket

#INSTANCIANDO LA CLASE SOCKET
socket_1 = socket.socket()

"""LLamar al metodo connect para establecer una conexión con el servidor. Teniendo en cuenta que tiene 
dos parametros, la direccion IP y el puerto """

Ip_Servidor = '127.0.0.1'
Puerto = 1234

"""Se Intenta establecer una conexión"""

try:
    Bandera = True
    socket_1.connect((Ip_Servidor,Puerto))

except ConnectionRefusedError:

    Bandera = False
    print("Intenta conectarse al servidor nuevamente")

while Bandera:

    """Solicitud del mensaje a enviar"""
    texto = input("Mesaje a enviar: ")
    """Cambio de formato del paquete a enviar (str-Bye)"""
    paquete = texto.encode()
    """Intente enviar un mensaje o si no termine la conexión"""
    try:
        socket_1.send(paquete)
        if texto == 'Cerrar':
            break
    except ConnectionResetError:
        break

    """Recibir mensaje del Servidor"""

    bytes_a_recibir = 1024
    mensaje_Recibido = socket_1.recv(bytes_a_recibir)
    texto = mensaje_Recibido.decode("utf-8")
    print(texto)

print("TERMINO LA COMUNICACION")
socket_1.close()


