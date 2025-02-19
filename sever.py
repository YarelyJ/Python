import socket
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

def select_files():
    """Abrir una ventana para seleccionar múltiples archivos."""
    Tk().withdraw()  # Oculta la ventana principal de Tkinter
    file_paths = askopenfilenames()  # Abrir cuadro de diálogo para seleccionar múltiples archivos
    if not file_paths:
        print("No seleccionaste ningún archivo.")
        return None
    return file_paths

def send_files(server_host, server_port):
    file_paths = select_files()
    if not file_paths:
        return

    try:
        # Conexión con el servidor
        print(f"Conectando con el servidor {server_host}:{server_port}...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        print("Conexión establecida.")

        for file_path in file_paths:
            # Obtener nombre y tamaño del archivo
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            # Enviar información del archivo (nombre y tamaño)
            print(f"Enviando información del archivo: {file_name}, tamaño: {file_size} bytes")
            client_socket.send(f"{file_name}|{file_size}".encode())

            # Enviar el archivo en bloques
            with open(file_path, "rb") as file:
                while True:
                    chunk = file.read(1024)  # Leer en bloques de 1024 bytes
                    if not chunk:
                        break
                    client_socket.send(chunk)

            print(f"Archivo '{file_name}' enviado correctamente.")

        # Enviar señal de finalización
        client_socket.send("FIN".encode())
        print("Todos los archivos se han enviado correctamente.")
        client_socket.close()

    except ConnectionRefusedError:
        print("Error: No se pudo conectar al servidor. Verifica que esté activo y que la dirección IP/puerto sean correctos.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "_main_":
    # Solicitar datos al usuario
    server_host = input("Introduce la dirección IP del servidor: ").strip()
    server_port = int(input("Introduce el puerto del servidor: ").strip())

    # Llamar a la función para enviar los archivos
    send_files(server_host, server_port)