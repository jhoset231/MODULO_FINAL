import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd


def generar_reporte_ventas(nombre_archivo):
    print(" Generando reporte de ventas...")
    datos = {
        "País": ["Perú", "México", "Argentina"],
        "Producto_ID": [101, 102, 103],
        "Total_Vendido": [500, 300, 400]
    }
    df = pd.DataFrame(datos)
    df.to_csv(nombre_archivo, index=False)
    print(f"✅ Reporte de ventas '{nombre_archivo}' generado correctamente.")
    return nombre_archivo

def generar_reporte_ventas_descuento(nombre_archivo):
    print("ℹ️ Generando reporte de ventas con descuento...")
    datos = {
        "País": ["Perú", "México", "Argentina"],
        "Producto_ID": [101, 102, 103],
        "Total_Vendido": [500, 300, 400],
        "Descuento_Aplicado": [50, 30, 40]
    }
    df = pd.DataFrame(datos)
    df.to_csv(nombre_archivo, index=False)
    print(f"✅ Reporte de ventas con descuento '{nombre_archivo}' generado correctamente.")
    return nombre_archivo

def enviar_correo(servidor_smtp, puerto_smtp, correo_remitente, clave_remitente, correo_destinatario, asunto, cuerpo, ruta_archivo=None):
    try:
        print("SMTP (Simple Mail Transfer Protocol) es el protocolo usado para enviar correos electrónicos.")
        print("Debes ingresar los datos correctos del servidor SMTP y la autenticación.")

        mensaje = MIMEMultipart()
        mensaje['From'] = correo_remitente
        mensaje['To'] = correo_destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        if ruta_archivo:
            with open(ruta_archivo, 'rb') as archivo:
                adjunto = MIMEApplication(archivo.read(), _subtype="csv")
                adjunto.add_header('Content-Disposition', 'attachment', filename=ruta_archivo.split("/")[-1])
                mensaje.attach(adjunto)

        with smtplib.SMTP(servidor_smtp, puerto_smtp) as servidor:
            servidor.starttls()
            servidor.login(correo_remitente, clave_remitente)
            servidor.sendmail(correo_remitente, correo_destinatario, mensaje.as_string())

        print("✅ Correo enviado exitosamente a", correo_destinatario)

    except Exception as e:
        print("❌ Error al enviar correo:", e)

def menu():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Generar reporte de ventas")
        print("2. Generar reporte de ventas con descuento")
        print("3. Enviar correo con reporte adjunto")
        print("4. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == '1':
            nombre_archivo = "reporte_ventas.csv"
            generar_reporte_ventas(nombre_archivo)
        elif opcion == '2':
            nombre_archivo = "reporte_ventas_descuento.csv"
            generar_reporte_ventas_descuento(nombre_archivo)
        elif opcion == '3':
            print(" Asegúrate de usar los datos correctos del servidor SMTP y autenticación.")
            servidor_smtp = input("Servidor SMTP: ")
            puerto_smtp = int(input("Puerto SMTP: "))
            correo_remitente = input("Correo del remitente: ")
            clave_remitente = input("Contraseña: ")
            correo_destinatario = input("Correo del destinatario: ")
            asunto = input("Asunto del correo: ")
            cuerpo = input("Cuerpo del correo: ")
            ruta_archivo = input("Ruta del archivo adjunto (ejemplo: reporte_ventas.csv o reporte_ventas_descuento.csv): ")
            
            if not ruta_archivo:
                print("❌ No se ha seleccionado un archivo para adjuntar.")
            else:
                enviar_correo(servidor_smtp, puerto_smtp, correo_remitente, clave_remitente, correo_destinatario, asunto, cuerpo, ruta_archivo)
        elif opcion == '4':
            print("Saliendo del programa...")
            break
        else:
            print("❌ Opción no válida. Inténtalo de nuevo.")


menu()
