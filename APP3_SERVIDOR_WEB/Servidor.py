"""
 ANDRES DANIEL RAMIREZ BEJARANO
 ING EN CONTROL Y AUTOMATIZACION
"""


from tkinter import messagebox
import tkinter as tk
import json
from tkinter import *
from PIL import Image, ImageTk
from random import randint
import hashlib
import PySimpleGUI as sg
import socket , pickle
import threading
import time
import mysql.connector as mysql
import sys

class conexion_BD:

    def __init__(self):

        self.ORIGEN = "localhost"
        self.USUARIO = "root"
        self.Contrasena = "12345"
        self.BASEDATOS = "BD_GAME"

    def connectBD(self):

        global userBD

        self.BD = mysql.connect(host=self.ORIGEN,user = self.USUARIO,password = self.Contrasena,db = self.BASEDATOS,auth_plugin='mysql_native_password')
        self.Cursor = self.BD.cursor()
        self.Cursor.execute("SELECT * FROM JUGADORES")

        for row in self.Cursor:
            userBD.append(''.join(row[1])+''.join(row[2])+''.join(row[4]))

        self.BD.close()

    def editRegistros(self,**kwargs):

        self.BD = mysql.connect(host=self.ORIGEN,user = self.USUARIO,password = self.Contrasena,db = self.BASEDATOS,auth_plugin='mysql_native_password')
        self.Cursor = self.BD.cursor()

        Npartidas = kwargs['nPartidas']
        idP1 = kwargs['idP1']
        idP2 = kwargs['idP2']
        puntos = kwargs['score']
        partidas_perdidas = kwargs['loseScore']

        scoreP1 = puntos[0]
        scoreP2 = puntos[1]

        pp_player1 = partidas_perdidas[0]
        pp_player2 = partidas_perdidas[1]

        consulta = """
                    UPDATE JUGADORES
                    SET PJUGADAS = PJUGADAS + %s
                    WHERE id = %s or id = %s
                    """

        self.Cursor.execute(consulta,(Npartidas,idP1,idP2))
        self.BD.commit()

        for i in range(2):

            consulta = """
                        UPDATE JUGADORES
                        SET PGANADAS = PGANADAS + %s,PPERDIDAS = PPERDIDAS + %s
                        WHERE id = %s
                        """
            if i == 0:
                self.Cursor.execute(consulta,(scoreP1,pp_player1,idP1))
            elif i == 1:
                self.Cursor.execute(consulta,(scoreP2,pp_player2,idP2))

        self.BD.commit()



class Wait_Connect:

    def __init__(self):
        pass

    def wait(self):

        global Lista_ID_Socket_Clientes,Lista_Direcciones,Puerto,socket_Server1,Ip_Servidor

        while True:

            global stateWindowLog

            try:

                paquete,direccion =socket_Server1.accept()
                Lista_ID_Socket_Clientes.append(paquete)
                Lista_Direcciones.append(direccion)

            except:
                break



class Client1_Connect:

    def __init__(self):

        global Ip_Servidor,Puerto
        self.IP_SERVIDOR = Ip_Servidor
        self.PUERTO = Puerto

    def reciveData(self):

        global  socket_Server1,Lista_ID_Socket_Clientes,Lista_Direcciones,data,statePlayer1,trama_envio,json_recive,name_players
        global indiceP1,stateWindowLog

        while True:

            if stateWindowLog:
                break

            if len(Lista_ID_Socket_Clientes) != 0:

                self.ID_SOCKET_CLIENT = Lista_ID_Socket_Clientes[0]
                self.Direcciones = Lista_Direcciones[0]
                break

        while True:

            bytes_recive = 1024

            if stateWindowLog:
                break

            try:

                trama_recive = self.ID_SOCKET_CLIENT.recv(bytes_recive)
                data = trama_recive.decode("utf-8")
                json_recive = json.loads(data)

                json_to_send = json.dumps(trama_envio)
                self.ID_SOCKET_CLIENT.send(json_to_send.encode("utf-8"))

                if json_recive['dataUser'] in userBD:

                    indiceP1 = userBD.index(json_recive['dataUser'])
                    name_players['player1'] = json_recive['name_player1']
                    statePlayer1 = True
                    trama_envio.update(statePlayer1=statePlayer1)

                else:
                    pass

            except ConnectionError:

                print("CLIENTE DESCONECTADO")

class RefreshInterfaz:
    def refresh(self,**kwargs):

        global name_players,conexionBD,indiceP1,indiceP2

        lab1  = kwargs['label_player1']
        lab2 = kwargs['label_player2']
        lab4 = kwargs['label_pointP1']
        lab5 = kwargs['label_pointP2']
        lab7 = kwargs['label_countP']
        vector_images = kwargs['vector_imagenes']
        interfaz = kwargs['interfaz']

        while True:

            global trama_envio,json_recive,nPartida,contPartida,puntajeP1,puntajeP2,puntosP1,puntosP2,stateInterface

            boton_principal = kwargs['botonPrincipal']

            num_loseP1 = 0
            num_loseP2 = 0

            num_winP1 = 0
            num_winP2 = 0

            num_games = 0

            if stateInterface==True:
                break

            if trama_envio['turno'] == "player1":

                boton_principal.configure(state=DISABLED,background="gray")
                lab1.configure(bg='white')
                lab2.configure(bg='black')

            else:

                boton_principal.configure(state=NORMAL,background="green")
                lab1.configure(bg='black')
                lab2.configure(bg='white')

            if (trama_envio['turno'] == "player1") and (json_recive['stateBtnPC'] == True):

                a = int(json_recive['value_dice'])
                img = Image.open(vector_images[a])
                new_img= img.resize((300,256))
                render= ImageTk.PhotoImage(new_img)
                img1= Label(interfaz,image=render)
                img1.image=render
                img1.place(x=50, y=30)
                img.close()
                trama_envio.update(ackS = True)
                num_games +=1
                contPartida+=1
                nPartida.set(str(contPartida))
                lab7.configure(textvariable = nPartida)
                valueP1 = int(json_recive['value_dice'])
                valueP2 = int(trama_envio['value_dice'])

                if (valueP1>valueP2):

                    num_winP1 += 1
                    num_loseP2 +=1
                    puntosP1 += 1
                    puntajeP1.set(str(puntosP1))
                    lab4.configure(textvariable = puntajeP1)

                elif (valueP2>valueP1):

                    num_winP2 += 1
                    num_loseP1 += 1
                    puntosP2 = puntosP2 + 1
                    puntajeP2.set(str(puntosP2))
                    lab5.configure(textvariable = puntajeP2)

                conexionBD.editRegistros(nPartidas = num_games , idP1 = int(indiceP1) + 1, idP2 = int(indiceP2)+1,
                                         score = (num_winP1,num_winP2),loseScore = (num_loseP1,num_loseP2))

                trama_envio.update(turno = "player2")

            interfaz.update()
class GameInterfaz:
    def runInterfaz(self):

        global  trama_envio,refrescar,name_players,nPartida,puntajeP1,puntajeP2,window

        trama_envio.update(name_jugadores =(name_players['player1'],name_players['player2']))
        interfaz= tk.Toplevel()
        interfaz.title("JUGADOR 2")
        interfaz.geometry('600x600+650+50')
        vector_images = ["imagen1.png","imagen2.png","imagen3.png","imagen4.png","imagen5.png","imagen6.png"]

        def cerrar():

            global stateInterface
            stateInterface = True
            interfaz.destroy()

        def imagen():

            global clickBtnPrincipal,nPartida,puntajeP1,puntajeP2

            clickBtnPrincipal = True
            a= randint(0,5)
            trama_envio.update(value_dice = a, stateBtnP = clickBtnPrincipal,ackS = False)
            img = Image.open(vector_images[a])
            new_img= img.resize((300,256))
            render= ImageTk.PhotoImage(new_img)
            img1= Label(interfaz,image=render)
            img1.image=render
            img1.place(x=50, y=30)
            img.close()

            while True:

                global  json_recive
                if json_recive['ack']:
                    break

            clickBtnPrincipal =False
            trama_envio.update(stateBtnP = clickBtnPrincipal,turno = "player1")

        name_player2 = StringVar()
        name_player2.set(name_players['player2'])

        name_player1 = StringVar()
        name_player1.set(name_players['player1'])

        puntajeP1.set(str(0))
        puntajeP2.set(str(0))
        nPartida.set(str(0))

        lab1 = Label(interfaz,textvariable=name_player1, fg ='green',bg= 'black',font=('Arial',20))
        lab1.place(x = 50,y = 360)

        lab2 = Label(interfaz,textvariable=name_player2, fg ='green',bg= 'black',font=('Arial',20))
        lab2.place(x = 50,y = 400)

        lab3 = Label(interfaz,text="SCORE", fg ='white',bg= 'black',font=('Arial',20))
        lab3.place(x = 350,y = 320)

        lab4 = Label(interfaz,textvariable=puntajeP1, fg ='white',bg= 'black',font=('Arial',20))
        lab4.place(x = 390,y = 360)

        lab5 = Label(interfaz,textvariable=puntajeP2, fg ='white',bg= 'black',font=('Arial',20))
        lab5.place(x = 390,y = 400)

        lab6 = Label(interfaz,text="No. PARTIDA", fg ='blue',bg= 'black',font=('Arial',20))
        lab6.place(x = 400,y = 150)

        lab7 = Label(interfaz,textvariable=nPartida, fg ='white',bg= 'black',font=('Arial',20))
        lab7.place(x = 470,y = 180)

        # botones interfaz
        botonprincipal=tk.Button(interfaz,text='Selección número',height=2, width=20,command=imagen)
        botonprincipal.place(x=50, y=470)

        botoncerrar=tk.Button(interfaz,text='Cerrar',height=2, width=20, command= cerrar)
        botoncerrar.place(x=230, y=470)
        interfaz.config(bg='black')

        hilo_refresh = threading.Thread(target = refrescar.refresh,kwargs={'vector_imagenes':vector_images,'interfaz':interfaz,
                                                                            'botonPrincipal' : botonprincipal,
                                                                            'label_player1':lab1,
                                                                            'label_player2':lab2,
                                                                            'label_countP':lab7,
                                                                           'label_pointP1':lab4,
                                                                           'label_pointP2':lab5})
        hilo_refresh.start()

        interfaz.mainloop()


if __name__ == '__main__':

    sg.theme('DarkTanBlue')
    print("HOLAAAAAAAA")
    layout= [[sg.Text('LOGIN JUGADOR 2')],
              [sg.Image('user_icon.png',expand_x=True)],
              [sg.Text('Nombre Usuario', size=(15, 1)),
               sg.InputText(key='-NAME-',do_not_clear=False)],
              [sg.Text('Contraseña ', size=(15, 1)), sg.InputText(key='-PSW-',password_char='*',do_not_clear=False)],
              [sg.Btn(button_text="Ingresar",expand_x=True),sg.Button(button_text="Registrarse",expand_x=True),sg.Cancel()]]

    window = sg.Window('Login',layout,size=(400,300),finalize=True,location=(600,150))

    socket_Server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Ip_Servidor = socket.gethostname()
    Puerto = 1234

    userBD = []
    data = ""
    conexionBD = conexion_BD()
    conexionBD.connectBD()

    socket_Server1.bind(("",Puerto))
    socket_Server1.listen()

    Lista_ID_Socket_Clientes = []
    Lista_Direcciones = []

    clickBtnPrincipal = False
    statePlayer1 = False
    statePlayer2 = False

    stateInterface = False
    stateWindowLog = False

    contPartida = 0
    puntosP1 = 0
    puntosP2 = 0
    nPartida = StringVar()
    puntajeP1 = StringVar()
    puntajeP2 = StringVar()

    name_players = {'player1':"",'player2':""}
    json_recive = ""
    trama_envio = {"statePlayer1":statePlayer1,"statePlayer2":statePlayer2,
                   "value_dice":-1,"turno":"","stateBtnP":clickBtnPrincipal,"ackS":False}

    wait_connection =Wait_Connect()
    conexionCliente1 = Client1_Connect()
    refrescar = RefreshInterfaz()

    hilo_conexiones = threading.Thread(target = wait_connection.wait)
    hilo_conexiones.start()

    hilo_player1 = threading.Thread(target = conexionCliente1.reciveData)
    hilo_player1.start()

    login_name = str
    login_passwd = str

    indiceP2 = int
    indiceP1 = int


    while True:

        event ,values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel

            socket_Server1.close()
            stateWindowLog =True
            window.close()
            break

        if "Ingresar" in event:

            login_name =values['-NAME-']
            login_passwd = values['-PSW-']

            "Encriptando la contraseña de la ventana de login"
            h = hashlib.new("sha1",login_passwd.encode())
            listValidacion = []
            listValidacion.append(login_name)
            listValidacion.append(h.hexdigest())

            strValidacion = "".join(listValidacion)
            strValidacion = strValidacion.replace(" ","")

            if strValidacion in userBD:

                indiceP2 = userBD.index(strValidacion)
                name_players['player2'] = login_name
                trama_envio.update(statePlayer2 = True)
                trama_envio.update(turno = "player2")
                wait_window = tk.Toplevel()
                wait_window.title("...")
                wait_window.geometry("300x100+660+180")
                #wait_window.config(width=300,height=100)

                Minute=StringVar()
                Second=StringVar()

                Minute.set("00")
                Second.set("59")

                Minute_entry= Entry(wait_window, width=3, font=("Arial",18,""),
                                    textvariable=Minute,state='readonly')
                Minute_entry.place(x=90,y=20)

                Second_entry= Entry(wait_window, width=3, font=("Arial",18,""),
                                    textvariable=Second,state='readonly')
                Second_entry.place(x=140,y=20)

                var = StringVar()
                label = Label(wait_window, textvariable = var,justify=CENTER)

                var.set("WAIT PLAYER...")
                label.place(x=100 , y = 60)

                temp = int(Minute.get())*60 + int(Second.get())
                estadoWindow2 = False

                while temp >-1:

                    if estadoWindow2:
                        window.close()
                        break
                    def cerrar():

                        global estadoWindow2
                        wait_window.destroy()
                        estadoWindow2 = True

                    wait_window.protocol("WM_DELETE_WINDOW",cerrar)

                    if statePlayer1 == True:

                        wait_window.destroy()
                        window.close()
                        interfazJuego = GameInterfaz()
                        interfazJuego.runInterfaz()
                        break;

                    Mins,Secs = divmod(temp,60)
                    Minute.set("{0:2d}".format(Mins))
                    Second.set("{0:2d}".format(Secs))

                    wait_window.update()
                    time.sleep(1)

                    if (temp == 0):

                        messagebox.showinfo("Time Countdown", "NO HAY JUGADORES CONECTADOS")
                        time.sleep(3)
                        wait_window.destroy()

                    temp -= 1

                print("ACCESO CONCEDIDO")

            else:
                print("ACCESO DENEGADO")



