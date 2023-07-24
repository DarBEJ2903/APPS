from scapy.all import *

def sniff_packets(packet):

    #Muestra informacion sobre cada paquete capturado
    packet.show()
    #carga util del packete
    print(packet.payload)

#filtro para capturar solo paquetes ARP (Adress resolution protocol)
arp_filter = "http" #tcp,http

#filtro para capturar solo paquetes que provengan de la direccion IP 192.168.1.6
ip_filter = "src host 192.168.1.6"

#Captura paquetes ARP
sniff(filter = arp_filter, prn = sniff_packets)
