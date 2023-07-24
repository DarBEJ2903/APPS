"""
 ANDRES DANIEL RAMIREZ BEJARANO
 ING EN CONTROL Y AUTOMATIZACION
"""

from typing import io
import hashlib
from flask import Flask,render_template,request
import time
import mysql.connector as mysql

app = Flask(__name__)

class CONEXION_BD:

    def __init__(self):

        self.ORIGEN = "localhost"
        self.USUARIO = "root"
        self.Contrasena = "12345"
        self.BASEDATOS = "BD_GAME"

    def connectBD(self):

        global userBD,p

        self.BD = mysql.connect(host=self.ORIGEN,user = self.USUARIO,password = self.Contrasena,db = self.BASEDATOS,auth_plugin='mysql_native_password')
        self.Cursor = self.BD.cursor()
        self.Cursor.execute("SELECT ID,FIRST_NAME,LAST_NAME,EMAIL,PJUGADAS,PGANADAS,PPERDIDAS FROM JUGADORES".format(io))
        users = self.Cursor.fetchall()
        nUsers = len(users)
        self.BD.close()

        return users,nUsers

    def registroBD(self,dataNewUser):

        self.BD = mysql.connect(host=self.ORIGEN,user = self.USUARIO,password = self.Contrasena,db = self.BASEDATOS,auth_plugin='mysql_native_password')
        self.Cursor = self.BD.cursor()
        Comando="INSERT INTO JUGADORES (FIRST_NAME,LAST_NAME,EMAIL,CONTRASENA,PJUGADAS,PGANADAS,PPERDIDAS) VALUES(%s,%s,%s, %s, %s, %s, %s);"
        h = hashlib.new("sha1",dataNewUser['CAJA4'].encode())
        Valores=(dataNewUser['CAJA2'],dataNewUser['CAJA3'],dataNewUser['CAJA1'],h.hexdigest(),
                 0,0,0)
        self.Cursor.execute(Comando,Valores)
        self.BD.commit()
        self.BD.close()
        print(dataNewUser)


@app.route('/Registro',methods = ['GET', 'POST'])
def paginaRegistro():

    return render_template('registro.html')

@app.route('/',methods = ['GET', 'POST'])
def paginaWB():

    global connectBD

    if request.method == 'POST':
        Valores_Registro = request.form

        if Valores_Registro:
            connectBD.registroBD(Valores_Registro)

    users,nUsers = connectBD.connectBD()
    return render_template('interfaceWEB.html',Datos = users, nRegistros = nUsers)

if __name__ == '__main__':

    connectBD = CONEXION_BD()
    app.run(debug=True)
