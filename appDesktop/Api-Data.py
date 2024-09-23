import tkinter as tk
from tkinter import ttk
import requests
from threading import Thread
import time

# URL de la API MockAPI
API_URL = "https://66eb848d55ad32cda47cc96b.mockapi.io/IoTCarStatus"

class RegistroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualización de Registros")
        self.root.geometry("750x450")
        self.root.configure(bg="#e6e6e6")

        # Crear estructura de la interfaz
        self.crear_interfaz()

        # Iniciar actualización automática
        self.iniciar_actualizacion()

    def crear_interfaz(self):
        # Encabezado
        self.crear_encabezado()

        # Cuerpo (listado de registros)
        self.crear_listado()

        # Botones
        self.crear_botones()

    def crear_encabezado(self):
        frame_encabezado = tk.Frame(self.root, bg="#de1263", padx=10, pady=10)
        frame_encabezado.pack(fill="x")

        label_titulo = tk.Label(frame_encabezado, text="10 Registros", font=("Arial", 20), bg="#de1263", fg="Black")
        label_titulo.pack()

    def crear_listado(self):
        frame_central = tk.Frame(self.root, bg="#6e6767")
        frame_central.pack(padx=20, pady=10, fill="both", expand=True)

        label_lista = tk.Label(frame_central, text="Registros recientes", font=("Arial", 14), bg="#6e6767")
        label_lista.pack(anchor="w")

        self.listbox_registros = tk.Listbox(frame_central, font=("Arial", 12), width=80, height=12)
        self.listbox_registros.pack(pady=10)

    def crear_botones(self):
        frame_botones = tk.Frame(self.root, bg="#e6e6e6")
        frame_botones.pack(pady=10)

        self.boton_actualizar = ttk.Button(frame_botones, text="Actualizar", command=self.refrescar_registros)
        self.boton_actualizar.pack(pady=10)

    def refrescar_registros(self):
        self.obtener_registros()

    def obtener_registros(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                registros = response.json()[-10:]  # 10 Registros
                self.mostrar_registros(registros)
            else:
                print(response.text)  # Imprime el cuerpo de la respuesta de error
                self.listbox_registros.insert(tk.END, f"Error al obtener registros: {response.status_code}")
        except Exception as e:
            self.listbox_registros.insert(tk.END, f"Error al obtener registros: {e}")

    def mostrar_registros(self, registros):
        self.listbox_registros.delete(0, tk.END)  # Limpiar el contenido anterior
        encabezado = f"{'ID':<5} {'Nombre':<20} {'Status':<10} {'Fecha':<20} {'IP':<15}"
        self.listbox_registros.insert(tk.END, encabezado)
        self.listbox_registros.insert(tk.END, "-" * 65)

        for registro in registros:
            fecha_formateada = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(registro['date']))
            registro_formateado = f"{registro['id']:<5} {registro['name']:<20} {registro['status']:<10} {fecha_formateada:<15} {registro['ipClient']:<15}"
            self.listbox_registros.insert(tk.END, registro_formateado)

    def iniciar_actualizacion(self):
        self.actualizar_registros()

    def actualizar_registros(self):
        self.obtener_registros()
        self.root.after(5000, self.actualizar_registros)  # Llama cada 5 segundos


# Crear la aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroApp(root)
    root.mainloop()
