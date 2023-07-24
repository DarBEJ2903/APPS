from scapy.all import *

"""DEFINE LA INTERFACE A TRAVES DE LA CUAL SE REALIZA UN ESCANEO"""

interface1 = "Ethernet"
interface2 = "Wi-Fi"

def Imprimir_Informacion(paquete):

    """Ip es una parametro heredado de la red"""
    ip_layer = paquete.getlayer(IP)
    print("Nuevo paquete detectado en: {src} >> {dst}".format(src = ip_layer.src, dst = ip_layer.dst))
    ip_layer.show(dump = True)

if __name__ == '__main__':

    print("Presione Ctrl+C para terminar")

    """Llamar hilo del sniffer"""
    sniff(iface = interface2,filter="ip",prn = Imprimir_Informacion)
    print("Término el Sniff")
