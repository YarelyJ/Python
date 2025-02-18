import socket
import os

def start_server(host="0.0.0.0", port=5000):
    print("Iniciando servidor...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Servidor escuchando en {host}:{port}")

    while True:
        print("Esperando conexión...")
        client_socket, address = server_socket.accept()
        print(f"Conexión establecida con {address}")

        # Recibir información del archivo
        file_info = client_socket.recv(1024).decode()
        print(f"Información recibida del cliente: {file_info}")
        file_name, file_size = file_info.split("|")
        file_size = int(file_size)

        # Solicitar al usuario si desea cambiar el nombre del archivo
        print(f"Recibiendo archivo: {file_name} ({file_size} bytes)")
        new_file_name = input("¿Deseas cambiar el nombre del archivo? Si no, presiona Enter: ")
        if not new_file_name.strip():
            new_file_name = file_name

        # Guardar el archivo recibido
        with open(new_file_name, "wb") as file:
            received_size = 0
            print("Recibiendo datos...")
            while received_size < file_size:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                file.write(chunk)
                received_size += len(chunk)

        print(f"Archivo {new_file_name} recibido y guardado correctamente.")
        client_socket.close()