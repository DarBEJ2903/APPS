import threading
import socket
from PyQt5.QtWidgets import *
import sys
import time

socket_1 = socket.socket()
amplitud_senal = "0"
freq_senal = "0"

class Conexion_Server:

    datos_envio = ""

    def __init__(self):

        self.Ip_Servidor = socket.gethostname()
        self.Puerto = 1234
        self.flag = False

    def etablecer_Comunicacion(self):

        global amplitud_senal
        global freq_senal
        global  socket_1


        while True:

            self.datos_envio = amplitud_senal + "$" + freq_senal
            self.trama = self.datos_envio.encode("utf-8")

            try:

                if not self.flag:
                    socket_1.connect((self.Ip_Servidor,self.Puerto))

                self.flag = True

            except ConnectionRefusedError:

                self.flag = False
                print("NO HAY CONEXIÓN CON SERVIDOR")
                continue


            try:

                socket_1.send(self.trama)
                print("CONECTADO AL SERVIDOR")
                bytes_a_recibir = 1024
                mensaje_Recibido = socket_1.recv(bytes_a_recibir)
                texto = mensaje_Recibido.decode("utf-8")
                print(texto)

            except ConnectionResetError:

                print("No hay conexion")
                break

            time.sleep(1)

        print("Termino la Comunicacion")
        socket_1.close()


class Window(QMainWindow):

    def __init__(self):

        super().__init__()

        # setting title
        self.setWindowTitle("CONTROL AMPLITUD Y FRECUENCIA ")

        # setting geometry
        self.setGeometry(100, 100, 700, 400)

        # calling method
        self.UiComponents()

    def changeAmplitud(self):

        global amplitud_senal

        self.label.setText("Amplitud = " + str(self.dial.value()))
        amplitud_senal = str(self.dial.value())

    def changeFreq(self):

        global freq_senal

        self.label2.setText("Frecuencia = " + str(self.dial_freq.value()))
        freq_senal = str(self.dial_freq.value())


    # method for components
    def UiComponents(self):

        # creating QDial object
        self.dial = QDial(self)
        self.dial_freq = QDial(self)

        # setting geometry to the dial
        self.dial.setGeometry(100, 100, 200, 200)
        self.dial_freq.setGeometry(300, 100, 400, 200)

        # setting minimum value to the dial
        self.dial.setMinimum(-10)
        self.dial.setMaximum(10)

        self.dial_freq.setMinimum(0)
        self.dial_freq.setMaximum(1000)


        # making notch visible
        self.dial.setNotchesVisible(True)
        self.dial_freq.setNotchesVisible(True)


        # creating a label
        self.label = QLabel("AMPLITUD", self)
        self.label2 = QLabel("FRECUENCIA", self)

        # setting geometry to the label
        self.label.setGeometry(180, 30, 230, 50)
        self.label2.setGeometry(450, 30, 500, 50)

        # making label multiline
        self.label.setWordWrap(True)
        self.label2.setWordWrap(True)


        # adding action to the dial
        self.dial.valueChanged.connect(self.changeAmplitud)
        self.dial_freq.valueChanged.connect(self.changeFreq)


    def mostrar_Interfaz(self):

        self.show()


if __name__ == '__main__':

    # create pyqt5 app
    App = QApplication(sys.argv)

    #create the instance of our Window
    window = Window()

    #Instanciando la clase comunicacion
    comu = Conexion_Server()

    hilo1 = threading.Thread(target = comu.etablecer_Comunicacion)
    hilo1.start()

    window.mostrar_Interfaz()

    # start the app
    sys.exit(App.exec())

