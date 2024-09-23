import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime  # Para obtener la fecha y hora


# Función para inyectar datos en MockAPI
def inyectar_datos(location_value):
    # Obtener los datos del formulario
    car_id = entry_car_id.get()
    status = entry_status.get()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtener fecha y hora actuales

    # Crear el payload (datos a enviar)
    data = {
        "car_id": car_id,
        "status": status,
        "location": location_value,
        "timestamp": current_time  # Añadir la fecha y hora
    }

    # URL de MockAPI
    url = "https://66eb848d55ad32cda47cc96b.mockapi.io/IoTCarStatus"

    try:
        # Realizar la solicitud POST para inyectar los datos
        response = requests.post(url, json=data)

        if response.status_code == 201:  # 201 Created
            messagebox.showinfo("Éxito", "Registro inyectado correctamente.")
            verificar_inyeccion(response.json()["id"])  # Verificar la inyección
        else:
            messagebox.showerror("Error", f"Error al inyectar el registro: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión: {e}")


# Función para verificar el registro inyectado
def verificar_inyeccion(record_id):
    url = f"https://66eb848d55ad32cda47cc96b.mockapi.io/IoTCarStatus/{record_id}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            messagebox.showinfo("Verificación", f"Registro verificado: {data}")
        else:
            messagebox.showerror("Error", "No se pudo verificar el registro.")
    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión: {e}")


# Función para manejar los botones de dirección
def enviar_direccion(direccion):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtener fecha y hora actuales
    text_output.config(state=tk.NORMAL)  # Habilitar escritura en el cuadro de texto
    text_output.insert(tk.END, f"{direccion} - {current_time}\n")  # Insertar la dirección y el tiempo
    text_output.config(state=tk.DISABLED)  # Deshabilitar escritura de nuevo
    inyectar_datos(direccion)  # Llamar a la función de inyección de datos


# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Inyección de Datos IoTCarStatus")
root.geometry("400x400")

# Etiquetas y campos de entrada
tk.Label(root, text="Car ID").pack(pady=10)
entry_car_id = tk.Entry(root)
entry_car_id.pack()

tk.Label(root, text="Status").pack(pady=10)
entry_status = tk.Entry(root)
entry_status.pack()

tk.Label(root, text="Location (Dirección)").pack(pady=10)

# Botones para direcciones
button_arriba = tk.Button(root, text="Arriba", command=lambda: enviar_direccion("Arriba"))
button_arriba.pack(pady=5)

button_abajo = tk.Button(root, text="Abajo", command=lambda: enviar_direccion("Abajo"))
button_abajo.pack(pady=5)

button_izquierda = tk.Button(root, text="Izquierda", command=lambda: enviar_direccion("Izquierda"))
button_izquierda.pack(pady=5)

button_derecha = tk.Button(root, text="Derecha", command=lambda: enviar_direccion("Derecha"))
button_derecha.pack(pady=5)

# Cuadro de texto para mostrar las direcciones y tiempos seleccionados
text_output = tk.Text(root, height=10, state=tk.DISABLED)
text_output.pack(pady=10)

# Iniciar la aplicación
root.mainloop()
