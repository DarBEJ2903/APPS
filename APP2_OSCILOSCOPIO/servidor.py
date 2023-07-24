import tkinter
import socket
import threading
import time
import math
import matplotlib.pyplot as plt
from tkinter import Tk, Frame,Button,Label, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import matplotlib.animation as animation
import numpy as np


class Wait_Connect:

    def __init__(self):
        pass

    def wait(self):

        global Lista_ID_Socket_Clientes

        while True:

            paquete,direccion =socket_Server1.accept()
            Lista_ID_Socket_Clientes.append(paquete)
            time.sleep(0.3)


class Client2_connect:

    def __init__(self):

        global Ip_Servidor,Puerto
        self.IP_SERVIDOR = Ip_Servidor
        self.PUERTO = Puerto

    def reciveData(self):

        global socket_Server1,Lista_ID_Socket_Clientes,estado_senal

        while True:

            if len(Lista_ID_Socket_Clientes) == 2:
                self.ID_SOCKET_CLIENT =  Lista_ID_Socket_Clientes[1]
                break

        while True:

            bytes_recive = 1024
            trama = self.ID_SOCKET_CLIENT.recv(bytes_recive)
            data = trama.decode("utf-8")
            Mensaje_envio = "Enviado"
            self.ID_SOCKET_CLIENT.send(Mensaje_envio.encode())
            print("conectado a cliente 2")
            estado_senal = data
            time.sleep(1)

class Client1_Connect:

    def __init__(self):

        global Ip_Servidor,Puerto
        self.IP_SERVIDOR = Ip_Servidor
        self.PUERTO = Puerto

    def reciveData(self):

        global  amplitud,frecuencia,gData,socket_Server1,Lista_ID_Socket_Clientes

        while True:
            if len(Lista_ID_Socket_Clientes) != 0 :
                self.ID_SOCKET_CLIENT = Lista_ID_Socket_Clientes[0]
                break

        while True:

                bytes_recive = 1024
                trama = self.ID_SOCKET_CLIENT.recv(bytes_recive)
                data = trama.decode("utf-8")
                Mensaje_envio = "Enviado"
                self.ID_SOCKET_CLIENT.send(Mensaje_envio.encode())
                print("conectado a cliente 1")

                index = data.find("$")
                amplitud = int(data[0:index])
                frecuencia = int(data[index+1::])


if __name__ == '__main__':


    amplitud = 0
    frecuencia = 0
    estado_senal = " "

    socket_Server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Ip_Servidor = socket.gethostname()
    Puerto = 1234

    fig, ax= plt.subplots(dpi=100)
    ax.set_facecolor('black')
    ax.grid(True)
    plt.title("Senosoidal", color="red", size=30)
    plt.xlim([0, 1000])
    plt.ylim([-10, 10])

    x = np.linspace(0, 400*np.pi, 100)
    line, = ax.plot(x, amplitud*np.sin(x), color='yellow', marker='o', linestyle='dotted', linewidth=6, markersize=1, markeredgecolor='violet')

    ventana = Tk()
    ventana.geometry('1042x835')
    ventana.wm_title('Osciloscopio')
    ventana.minsize(width=742, height=635)

    frame = Frame(ventana, bg='white', bd=3)
    frame.pack(fill='both')

    canvas = FigureCanvasTkAgg(fig, master = frame)
    canvas.get_tk_widget().pack(padx=5, pady=5, expand=1, fill='both')

    def ani(i):

        if estado_senal == "Run":

            line.set_ydata(np.sin((x+i)*frecuencia)*amplitud)

        elif estado_senal == "Stop":
            pass
        return line,


    ani = animation.FuncAnimation(fig, ani, interval=15, blit=True, save_count=10)

    canvas.draw()

    wait_connection =Wait_Connect()
    conexionCliente1 = Client1_Connect()
    conexionCliente2 =  Client2_connect()


    socket_Server1.bind((Ip_Servidor,Puerto))
    socket_Server1.listen()
    Lista_ID_Socket_Clientes = []
    Lista_Direcciones = []

    print(len(Lista_ID_Socket_Clientes))

    hilo_conexiones = threading.Thread(target = wait_connection.wait)
    hilo_conexiones.start()

    hilo1 = threading.Thread(target = conexionCliente1.reciveData)
    hilo1.start()

    hilo2 = threading.Thread(target = conexionCliente2.reciveData)
    hilo2.start()

    ventana.mainloop()




