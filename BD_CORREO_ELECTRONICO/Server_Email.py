"""IMPORTE LA LIBRERIA SMTP"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class Conexion_Server_Email:
    def __init__(self):
        pass


if __name__ == '__main__':

    """CREE UN OBJETO PARA ALMACENAR EL CORREO ELECTRONICO A ENVIAR"""
    MSG = MIMEMultipart()

    """ESCRIBA EL CUERPO DEL CORREO ELECTRONICO"""
    Mensaje = "Estamos envando un correo desde python utilizando SMTP"

    """ESTABLEZCA LOS PARAMETROS DEL CORREO ELECTRONICO"""
    Contrasena = "ihxiwpwtsqduyxeo"
    MSG['From'] = "daniel032998@gmail.com"
    MSG['To'] = "daniel0327@outlook.es"
    MSG['Subject'] = "PRUEBA CORREO"

    """AGREGUE EL CUERPO DEL CORREO AL OBJETO"""
    MSG.attach(MIMEText(Mensaje,'plain'))

    try:
        """ESTABLEZCA LA CONEXION CON EL SERVIDOR DE GMAIL"""

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()

        """INGRESE AL SERVICIO"""

        server.login(MSG['From'],Contrasena)

        """ENVIE EL MENSAJE"""
        server.sendmail(MSG['From'],MSG['To'],MSG.as_string())
        server.quit()
        print("Mensaje enviado a: %s"% (MSG['To']))

    except:

        print("Error al enviar el correo")
