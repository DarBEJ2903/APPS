"""
 ANDRES DANIEL RAMIREZ BEJARANO
 ING EN CONTROL Y AUTOMATIZACION
"""

import hashlib
from functools import partial
from tkinter import messagebox
import json
from tkinter import *
from PIL import Image, ImageTk
from random import randint
import tkinter as tk
import PySimpleGUI as sg
import threading
import  sys
import  socket,pickle
import time
from tkinter import messagebox


class RefreshInterfaz:
    def refresh(self,**kwargs):

        lab1 = kwargs['label_Jugador1']
        lab2 = kwargs['label_Jugador2']
        vector_images = kwargs['vector_imagenes']
        interfaz = kwargs['interfaz']

        while True:

            global isclose,json_recive,json_envio

            boton_principal = kwargs['botonPrincipal']

            if isclose:
                interfaz.destroy()
                break

            if json_recive['turno'] == "player2":

                boton_principal.configure(state=DISABLED,background="gray")
                lab1.configure(bg="black")
                lab2.configure(bg="white")

            else:

                lab1.configure(bg="white")
                lab2.configure(bg="black")
                boton_principal.configure(state=NORMAL,background="green")

            if (json_recive['turno'] == "player2") and (json_recive['stateBtnP'] == True):

                a = int(json_recive['value_dice'])
                img = Image.open(vector_images[a])
                new_img= img.resize((300,256))
                render= ImageTk.PhotoImage(new_img)
                img1= Label(interfaz,image=render)
                img1.image=render
                img1.place(x=50, y=30)
                img.close()
                json_envio.update(ack = True)


            interfaz.update()


class ServerConnect:

    def __init__(self):
        self.flag = False

    def connect(self):

        global socket_1,Ip_Servidor,Puerto,json_recive,json_envio

        while True:

            if event == sg.WIN_CLOSED or event == 'Cancel':
                print("TERMINO COMUNICACION")
                socket_1.close()
                break

            try:

                if not self.flag:
                    socket_1.connect((Ip_Servidor,Puerto))

                self.flag = True

            except ConnectionRefusedError:

                self.flag = False
                print("NO HAY CONEXIÓN CON SERVIDOR")
                continue

            try:

                trama_send = json.dumps(json_envio)
                socket_1.send(trama_send.encode())
                bytes_a_recibir = 4096
                mensaje_Recibido = socket_1.recv(bytes_a_recibir).decode()
                json_recive = json.loads(mensaje_Recibido)

            except ConnectionResetError:
                pass

            time.sleep(1)

class GameInterfaz:
    def runInterfaz(self):

        global json_recive,nPartida,puntajeP1,puntajeP2

        interfaz= tk.Toplevel()
        interfaz.title("JUGADOR 1")
        interfaz.geometry('600x600+50+50')

        vector_images = ["imagen1.png","imagen2.png","imagen3.png","imagen4.png","imagen5.png","imagen6.png"]
        def closeWindow():

            global isclose

            isclose =True
            interfaz.destroy()

        def imagen():

            global json_envio,contPartida,puntosP1,puntosP2

            a= randint(0,5)
            img = Image.open(vector_images[a])
            new_img= img.resize((300,256))
            render= ImageTk.PhotoImage(new_img)
            img1= Label(interfaz,image=render)
            img1.image=render
            img1.place(x=50, y=30)
            clickBtnPrincipal = True
            json_envio.update(value_dice = a,stateBtnPC = clickBtnPrincipal,ack = False)

            while True:

                json_recive.update()
                if json_recive['ackS']:
                    break

            contPartida += 1
            nPartida.set(str(contPartida))

            valueDiceP1 = int(json_envio['value_dice'])
            valueDiceP2 = int(json_recive['value_dice'])

            if valueDiceP1 > valueDiceP2:

                puntosP1 += 1
                puntajeP1.set(str(puntosP1))

            elif valueDiceP2 >valueDiceP1:

                puntosP2 += 1
                puntajeP2.set(str(puntosP2))

            clickBtnPrincipal =False
            json_envio.update(stateBtnPC = clickBtnPrincipal)

        name_player2 = StringVar()
        name_player2.set(json_recive['name_jugadores'][1])

        name_player1 = StringVar()
        name_player1.set(json_recive['name_jugadores'][0])

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

        botonprincipal=tk.Button(interfaz,text='Selección número',height=2, width=20,command=imagen)
        botonprincipal.place(x=50, y=470)

        botoncerrar=tk.Button(interfaz,text='Cerrar',height=2, width=20, command= closeWindow)
        botoncerrar.place(x=230, y=470)
        interfaz.config(bg='black')

        hilo2 = threading.Thread(target = refrescar.refresh,kwargs={'vector_imagenes':vector_images,'interfaz':interfaz,
                                                                    'botonPrincipal' : botonprincipal,
                                                                    'label_Jugador1':lab1,
                                                                    'label_Jugador2':lab2,
                                                                    'label_countP':lab7,
                                                                    'label_pointP1':lab4,
                                                                    'label_pointP2':lab5
                                                                    })
        hilo2.start()

        interfaz.mainloop()


if __name__ == '__main__':

    """Ejecución HILO 1"""
    socket_1 = socket.socket()
    Ip_Servidor = socket.gethostname()
    Puerto = 1234

    conexionServer = ServerConnect()
    refrescar = RefreshInterfaz()

    sg.theme('DarkTanBlue')
    layout = [[sg.Text('LOGIN JUGADOR 1')],
                   [sg.Image('user_icon.png',expand_x=True)],
                   [sg.Text('Nombre Usuario', size=(15, 1)),
                    sg.InputText(key='-NAME-',do_not_clear=False)],
                   [sg.Text('Contraseña ', size=(15, 1)), sg.InputText(key='-PSW-',password_char='*',do_not_clear=False)],
                   [sg.Btn(button_text="Ingresar",expand_x=True),sg.Button(button_text="Registrarse",expand_x=True),sg.Cancel()]]

    window = sg.Window('Login',layout,size=(400,300),finalize=True,location=(90,150))

    contPartida = 0
    puntosP1 = 0
    puntosP2 = 0
    nPartida = StringVar()
    puntajeP1 = StringVar()
    puntajeP2 = StringVar()

    isclose = False
    clickBtnPrincipal = False
    name_player1 = ""
    strValidacion = ""
    login_nombre = ""
    login_psw = ""
    event = []
    json_recive = {}
    json_envio = {"dataUser" : strValidacion,'ack':False,'value_dice':-1, 'stateBtnPC': clickBtnPrincipal,
                  "name_player1":name_player1}

    hilo1 = threading.Thread(target = conexionServer.connect)
    hilo1.start()

    while True:

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel

            window.close()
            break

        if "Ingresar" in event:

            login_nombre = values['-NAME-']
            login_psw = values['-PSW-']

            "Encriptando la contraseña de la ventana de login"
            h = hashlib.new("sha1",login_psw.encode())
            listValidacion = []
            listValidacion.append(login_nombre)
            listValidacion.append(h.hexdigest())

            strValidacion = "".join(listValidacion)
            strValidacion = strValidacion.replace(" ","")
            json_envio.update(dataUser = strValidacion)
            time.sleep(2)

            if json_recive['statePlayer1'] == False:

                sg.popup_ok("ACCESO DENEGADO")

            elif json_recive['statePlayer1'] == True:

                json_envio.update(name_player1 = login_nombre)
                wait_window = tk.Toplevel()
                wait_window.title("...")
                wait_window.geometry("300x100+100+170")
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
                        break
                    def cerrar():

                        global estadoWindow2
                        wait_window.destroy()
                        estadoWindow2 = True

                    wait_window.protocol("WM_DELETE_WINDOW",cerrar)

                    if json_recive['statePlayer2'] == True:

                        wait_window.destroy()
                        window.close()
                        interfazJuego = GameInterfaz()
                        interfazJuego.runInterfaz()
                        break

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

        event ,values = window.read()
