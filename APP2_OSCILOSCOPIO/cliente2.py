import threading
import socket
from tkinter import Tk, Frame,Button,Label, ttk
import sys
import time

estado_Senal = "Stop"


class Servidor_Connect:

    def __init__(self):


        self.Ip_Servidor = socket.gethostname()
        self.Puerto = 1234
        self.flag = False

    def conectar(self):

        global estado_Senal

        while True:

            self.datos_envio = estado_Senal
            self.trama = self.datos_envio.encode("utf-8")

            try:

                if not self.flag:
                 socket_1.connect((self.Ip_Servidor,self.Puerto))

                self.flag = True

            except ConnectionRefusedError:

                print("NO CONECTADO A SERVER")
                continue

            try:

                socket_1.send(self.trama)
                print(self.trama)
                bytes_a_recibir = 1024
                mensaje_Recibido = socket_1.recv(bytes_a_recibir)
                texto = mensaje_Recibido.decode("utf-8")
                print(texto)

            except ConnectionResetError:

                print("No hay conexion")
                break


if __name__ == '__main__':

    socket_1 = socket.socket()

    ventana = Tk()
    ventana.geometry('500x100')
    ventana.wm_title('Osciloscopio')
    ventana.minsize(width=200, height=200)

    frame = Frame(ventana, bg='white', bd=3)
    frame.pack(fill='both')

    def begin():
        global estado_Senal
        estado_Senal = "Run"

    def pausar():
        global  estado_Senal
        estado_Senal = "Stop"


    def reanudar():
        global  estado_Senal
        estado_Senal = "Play"

    Button(frame, text='INICIO',width=15, bg='#FF5F00',fg='black',command=begin).pack(pady=5, side='left',expand=1)
    Button(frame, text= 'PAUSAR',width=15, bg='#0DFFF5',fg='black',command=pausar).pack(pady=5, side='left', expand=1)
    Button(frame, text='REANUDAR',width=15, bg='#FF0545',fg='black', command=reanudar).pack(pady=5, side='left', expand=1)

    conexion = Servidor_Connect()
    hilo1 = threading.Thread(target = conexion.conectar)
    hilo1.start()


    ventana.mainloop()