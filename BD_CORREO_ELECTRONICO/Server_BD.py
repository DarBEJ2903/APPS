# _*_ coding: utf-8 _*_
"""Importar libreria del conector mysql"""
import mysql.connector as mysql

"CREAR VARIABLES CON LOS PARAMETROS DE ACCESO A LA BD"
ORIGEN = "localhost"
USUARIO = "root"
Contrasena = "AmericaCali-98"
BASEDATOS = "EJEMPLO1"

"""ESTABLECER CONEXION CON LA BASE DE DATOS"""

BD = mysql.connect(host=ORIGEN,user=USUARIO,password=Contrasena,db=BASEDATOS,auth_plugin='mysql_native_password')
Cursor = BD.cursor()

"""CODIGO PARA CONSULTAR EN LA BASE DE DATOS"""
Cursor.execute("SELECT * FROM SENSOR_1")

for row in Cursor:
    print(row)

"""CODIGO PARA INSERTAR UN REGISTRO"""

"""Comando = "INSERT INTO SENSOR_1 (HORA,TEMPERATURA) VALUES (%s,%s);"
valores = (str(14),str(15.86))
Cursor.execute(Comando,valores)
BD.commit()"""
BD.close()


