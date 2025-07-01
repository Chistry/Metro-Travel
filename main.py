from data_loader import cargar_visas, cargar_tarifas
from pathfinder import construir_grafo, encontrar_ruta_mas_barata
import tkinter as tk
from tkinter import messagebox


#Orquesta la aplicación: saluda, pide datos, procesa y muestra resultados.
def iniciar_consulta(origen, destino, tiene_visa, resultado_label):
    
    #print("✈️  Bienvenido al sistema de consulta de vuelos de Metro Travel ✈️")
    #print("-" * 60)

    # 1. Cargar datos usando nuestro módulo
    visas = cargar_visas()
    tarifas = cargar_tarifas()
    todos_aeropuertos = set(visas.keys())

    # 2. Interactuar con el usuario (esto después lo cambian apra agregarle el UI de usuario)
    # ORIGEN
    origen = origen.get().upper()
    if origen not in todos_aeropuertos:
        messagebox.showerror("Error", f"El aeropuerto de origen '{origen}' no es válido.")
        return

    # DESTINO
    destino_final = destino.get().upper()
    if destino_final not in todos_aeropuertos:
        messagebox.showerror("Error", f"El aeropuerto de destino '{destino_final}' no es válido.")
        return

    tiene_visa = tiene_visa.get()

    #print("-" * 60)

    # 3. Aplicar la lógica de negocio y obtener resultados

    # Lógica para determinar aeropuertos permitidos
    if tiene_visa:
        aeropuertos_permitidos = todos_aeropuertos
    else:
        aeropuertos_permitidos = {a for a, req in visas.items() if not req}

    # Verificar si el origen o el destino requieren visa y el pasajero no la tiene
    if origen not in aeropuertos_permitidos:
        resultado_label.config(text=f"El aeropuerto de origen '{origen}' requiere visa y el pasajero no la posee.")
        return
    if destino_final not in aeropuertos_permitidos:
        resultado_label.config(text=f"El aeropuerto de destino '{destino_final}' requiere visa y el pasajero no la posee.")
        return


    # Usamos las funciones de nuestro módulo pathfinder
    grafo = construir_grafo(tarifas, aeropuertos_permitidos)
    costo, escalas, ruta = encontrar_ruta_mas_barata(grafo, origen, destino_final)

    # 4. Presentar resultados
    if costo != float('inf'):
        resultado = f"🎉 ¡Ruta más económica encontrada! 🎉\nRuta: {' -> '.join(ruta)}\nCosto Total: ${costo:,.2f}\nNúmero de vuelos/escalas: {len(ruta) - 1}"
    else:
        resultado = f"No se encontró una ruta posible desde {origen} hacia {destino_final}."
    resultado_label.config(text=resultado)

def iniciar_gui():
    root = tk.Tk()
    root.title("Metro Travel - Consulta de Vuelos")
    
    tk.Label(root, text="Aeropuerto ORIGEN:").grid(row=0, column=0, padx=5, pady=5)
    origen_entry = tk.Entry(root)
    origen_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Aeropuerto DESTINO:").grid(row=1, column=0, padx=5, pady=5)
    destino_entry = tk.Entry(root)
    destino_entry.grid(row=1, column=1, padx=5, pady=5)

    tiene_visa = tk.BooleanVar()
    tk.Checkbutton(root, text="¿Tiene visa?", variable=tiene_visa).grid(row=2, columnspan=2, pady=5)

    resultado_label = tk.Label(root, text="", fg="blue", wraplength=400, justify="left")
    resultado_label.grid(row=4, columnspan=2, padx=5, pady=10)

    consultar_btn = tk.Button(
        root, text="Consultar Ruta",
        command=lambda: iniciar_consulta(origen_entry, destino_entry, tiene_visa, resultado_label)
    )
    consultar_btn.grid(row=3, columnspan=2, pady=5)

    root.mainloop()

if __name__ == "__main__":
    iniciar_gui()