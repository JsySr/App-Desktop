def inyectar_datos():
    # Obtener los datos del formulario
    car_id = entry_car_id.get()
    status = entry_status.get()
    location = entry_location.get()

    # Crear el payload (datos a enviar)
    data = {
        "car_id": car_id,
        "status": status,
        "location": location
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
