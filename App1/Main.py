import PySimpleGUI as sg
from tkinter import messagebox
from Opcion_1 import grafica_barras as op1
from  Opcion2 import GFG as op2
from Opcion3 import opcion3 as op3
from PIL import ImageTk, Image
from tkinter import *


import tkinter
import time
from tkinter import *
from PIL import ImageTk, Image


Usuarios = {'ANDRES RAMIREZ' : '123' }

class mainInterfaz:
    stateVal = False

    def __init__(self):

        self.interfazreg = interfazReg()
        self.validacion = Validacion()
        self.secondwidow = secondWindow()
        sg.theme('DarkTanBlue')
        self.layout = [[sg.Text('LOGIN')],
                    [sg.Image('imagen1.png',expand_x=True)],
                    [sg.Text('Nombre Usuario', size=(15, 1)),
                     sg.InputText(key='-NAME-',do_not_clear=False)],
                    [sg.Text('Contraseña ', size=(15, 1)), sg.InputText(key='-PSW-',password_char='*',do_not_clear=False)],
                    [sg.Btn(button_text="Ingresar",expand_x=True),sg.Button(button_text="Registrarse",expand_x=True),sg.Cancel()]]
        self.run()

    def run(self):
        self.window = sg.Window('Login', self.layout,size=(400,300),finalize=True)
        while True:

            self.event ,self.values = self.window.read()
            if self.event == sg.WIN_CLOSED or self.event == 'Cancel': # if user closes window or clicks cancel
                break
            elif "Registrarse" in self.event:

                self.window.minimize()
                self.interfazreg.run()
                self.window.Normal()
                #self.window['-NAME-'].update("")
                #self.window['-PSW-'].update("")

            elif "Ingresar" in self.event:

                self.stateVal = self.validacion.validar(self.values)
                if not self.stateVal:
                    sg.popup_ok("USUARIO NO EXISTE")
                else:
                    self.window.minimize()
                    self.secondwidow.run(self.values['-NAME-'])
                    self.window.Normal()

            print(self.stateVal)


class interfazReg:

    nameNewUser = ""
    passNewUsr = ""
    values = {}
    global Usuarios

    def run(self):

        self.layout = [[sg.Text('REGISTRO')],
                    [sg.Text('NOMBRE', size=(15, 1)),sg.InputText(do_not_clear=False)],
                    [sg.Text('APELLIDO', size=(15, 1)),sg.InputText(do_not_clear=False)],
                    [sg.Text('CONTRASEÑA ', size=(15, 1)), sg.InputText(password_char='*',do_not_clear=False)],
                    [sg.Text('CONFIRMAR', size=(15, 1)), sg.InputText(password_char='*',do_not_clear=False)],
                    [sg.Button(button_text="CREAR",expand_x=True),sg.Cancel()]]

        self.window = sg.Window('REGISTRARSE', self.layout)
        self.event, self.values = self.window.read()
        self.window.close()  if self.event == sg.WIN_CLOSED or self.event else 0
        self.crearUsuario(self.values) if "CREAR" in self.event else 0


    def crearUsuario(self,values):

        if values[2] == values[3]:
            self.nameNewUser = values[0]+" "+values[1]
        else:
            return
        self.passNewUsr = values[2]
        Usuarios[self.nameNewUser] = self.passNewUsr
        messagebox.showinfo(message="USUARIO CREADO CON ÉXITO",title="REGISTRO")
        return

class secondWindow:

    def run(self,nameUser):

        self.layout = [[sg.Text('USER: ',auto_size_text=True,background_color="green"),sg.Text(nameUser,auto_size_text=True,background_color="green")],
                       [sg.Btn(button_text="OPCION 1",expand_x=True,expand_y=True)],
                       [sg.Btn(button_text="OPCION 2",expand_x=True,expand_y=True)],
                       [sg.Btn(button_text="OPCION 3",expand_y=True,expand_x=True)],
                       [sg.Cancel()]]

        self.window = sg.Window('USUARIO' , self.layout,size=(300,300),finalize=True)
        self.event, self.values = self.window.read()
        self.window.close()  if self.event == sg.WIN_CLOSED or self.event else 0

        if self.event == "OPCION 1":

            self.bar_plot = op1()
            self.bar_plot.graficar()
            return

        elif self.event == "OPCION 2":

            self.gif = op2()
            self.window.finalize()
            self.gif.graficar()
            return

        elif self.event == "OPCION 3":

            self.animation3 = op3()
            self.window.finalize()
            self.animation3.master.mainloop()
            return

class Validacion:

    nombre = ""
    password  = 0
    global Usuarios

    def validar(self,values):

        self.nombre = values['-NAME-']
        self.password = values['-PSW-']
        if self.nombre in Usuarios:
           return True if Usuarios.get(self.nombre) == self.password else 0

if __name__ == '__main__':
    main = mainInterfaz()
