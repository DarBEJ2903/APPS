import psutil

disk_usage = psutil.disk_usage("C:\\")
disk_usage2 = psutil.disk_usage("D:\\")

def convert_bytes_to_gigas(bytes):
    "Convirtiendo a gigaBytes"
    return bytes/1024**3

if __name__ == '__main__':

    print("Espacio Total: {:.2f} GB.".format(convert_bytes_to_gigas(disk_usage.total)))
    print("Espacio Disponible: {:.2f} GB.".format(convert_bytes_to_gigas(disk_usage.free)))
    print("Espacio Usado: {:.2f} GB.".format(convert_bytes_to_gigas(disk_usage.used)))
    print("Porcentaje de espacio usado: {}% GB.".format(disk_usage.percent))
    print("\n\r")
    print("DISCO D")
    print("Espacio Total: {:.2f} GB.".format(convert_bytes_to_gigas(disk_usage2.total)))
    print("Espacio Disponible: {:.2f} GB.".format(convert_bytes_to_gigas(disk_usage2.free)))
    print("Espacio Usado: {:.2f} GB.".format(convert_bytes_to_gigas(disk_usage2.used)))
    print("Porcentaje de espacio usado: {}% GB.".format(disk_usage2.percent))