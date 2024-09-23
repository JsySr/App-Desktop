import tkinter as tk
import requests
import socket
import time
from threading import Thread

# URL de la API MockAPI
API_URL = "https://66eb848d55ad32cda47cc96b.mockapi.io/IoTCarStatus"


class ControlCarritoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Carrito")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        # Crear la interfaz gráfica
        self.crear_interfaz()

    def crear_interfaz(self):
        # Mostrar nombre predeterminado en la ventana
        label_nombre = tk.Label(self.root, text="Nombre: Usuario", font=("Helvetica", 14), bg="#827e7e")
        label_nombre.pack(pady=10)

        # Etiqueta para el estado
        self.label_status = tk.Label(self.root, text="A donde se mueve el carrito", font=("Helvetica", 15),
                                     bg="#827e7e")
        self.label_status.pack(pady=10)

        # Frame para los botones
        frame_botones = tk.Frame(self.root, bg="#f0f0f0")
        frame_botones.pack(expand=True)

        # Crear botones de control
        self.crear_botones(frame_botones)

        # Asignar eventos de teclado
        self.root.bind('<Key>', self.controlar_teclado)

    def crear_botones(self, frame):
        # Estilo de botones
        btn_style = {
            "width": 12,
            "height": 3,
            "font": ("Arial", 12)
        }

        # Botón Adelante (Rojo)
        btn_adelante = tk.Button(frame, text="Adelante", **btn_style, bg="#F44336",
                                 command=lambda: self.enviar_datos("adelante"))
        btn_adelante.grid(row=0, column=1, padx=5, pady=5)

        # Botón Atrás (Azul)
        btn_atras = tk.Button(frame, text="Atrás", **btn_style, bg="#2196F3",
                              command=lambda: self.enviar_datos("atras"))
        btn_atras.grid(row=2, column=1, padx=5, pady=5)

        # Botón Izquierda (Amarillo)
        btn_izquierda = tk.Button(frame, text="Izquierda", **btn_style, bg="#FFEB3B",
                                   command=lambda: self.enviar_datos("izquierda"))
        btn_izquierda.grid(row=1, column=0, padx=5, pady=5)

        # Botón Derecha (Amarillo)
        btn_derecha = tk.Button(frame, text="Derecha", **btn_style, bg="#FFEB3B",
                                 command=lambda: self.enviar_datos("derecha"))
        btn_derecha.grid(row=1, column=2, padx=5, pady=5)

        # Cambiar el diseño del cuadro
        for button in [btn_adelante, btn_atras, btn_izquierda, btn_derecha]:
            button.config(relief="raised", borderwidth=3)

    def enviar_datos(self, status):
        nombre = "Usuario"  # Nombre estático
        data = {
            "status": status,
            "date": int(time.time()),  # Fecha en formato Unix
            "ipClient": self.obtener_ip_cliente(),
            "name": nombre,
            "id": "5"  # ID estático como ejemplo
        }

        def enviar_peticion():
            try:
                response = requests.post(API_URL, json=data)
                if response.status_code == 201:
                    self.label_status.config(text=f"Datos enviados: {status}")
                else:
                    self.label_status.config(text=f"Error: {response.status_code}")
            except Exception as e:
                self.label_status.config(text=f"Error al enviar datos: {e}")

        # Enviar la petición en segundo plano para no bloquear la interfaz
        Thread(target=enviar_peticion).start()

    def controlar_teclado(self, event):
        tecla = event.char.lower()
        if tecla == "w":
            self.enviar_datos("adelante")
        elif tecla == "s":
            self.enviar_datos("atras")
        elif tecla == "a":
            self.enviar_datos("izquierda")
        elif tecla == "d":
            self.enviar_datos("derecha")

    @staticmethod
    def obtener_ip_cliente():
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)


# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ControlCarritoApp(root)
    root.mainloop()
