from scapy.layers.inet import IP, ICMP
from time import time
from scapy.all import sr1
import sys
import os

Direccion_IP = "192.168.0.1"

tiempo_inicio = time()
informacion_recibida = sr1(IP(dst = Direccion_IP)/ICMP(),timeout = 2)

try:
    informacion_recibida.show()
    tiempo_transcurrido = time() - tiempo_inicio
    print(tiempo_transcurrido)
except:
    print("No se detecto dispositivo")
