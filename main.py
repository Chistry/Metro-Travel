from data_loader import cargar_visas, cargar_tarifas
from pathfinder import construir_grafo, encontrar_ruta_mas_barata
from bfs_pathfinder import encontrar_ruta_menos_escalas_bfs
from graph_visualizer import GraphVisualizer
from complete_graph_visualizer import CompleteGraphVisualizer
import tkinter as tk
from tkinter import messagebox


#Orquesta la aplicación: saluda, pide datos, procesa y muestra resultados.
def iniciar_consulta(origen, destino, tiene_visa, resultado_label, root):
    
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
        vuelos_totales = len(ruta) - 1
        escalas = max(0, len(ruta) - 2)
        resultado = (
            f"🎉 ¡Ruta más económica encontrada! 🎉\n"
            f"Ruta: {' -> '.join(ruta)}\n"
            f"Costo Total: ${costo:,.2f}\n"
            f"Vuelos totales: {vuelos_totales}\n"
            f"Escalas: {escalas}"
        )
        
        # Habilitar botón para ver grafo con ruta
        visualizar_ruta_btn.config(
            state="normal",
            command=lambda: GraphVisualizer(root, grafo, ruta)
        )
    else:
        resultado = f"No se encontró una ruta posible desde {origen} hacia {destino_final}."
        visualizar_ruta_btn.config(state="disabled")
        
    resultado_label.config(text=resultado)
    
    # Guardar el grafo actual para poder visualizarlo
    root.grafo_actual = grafo

def buscar_menos_escalas(origen, destino, tiene_visa, resultado_label, root):
    """
    Busca la ruta con menos escalas usando BFS (Breadth-First Search).
    
    BFS garantiza encontrar la ruta con el mínimo número de escalas,
    ya que explora el grafo nivel por nivel.
    """
    # 1. Cargar datos
    visas = cargar_visas()
    tarifas = cargar_tarifas()
    todos_aeropuertos = set(visas.keys())

    # 2. Validar entrada
    origen_str = origen.get().upper()
    if origen_str not in todos_aeropuertos:
        messagebox.showerror("Error", f"El aeropuerto de origen '{origen_str}' no es válido.")
        return

    destino_str = destino.get().upper()
    if destino_str not in todos_aeropuertos:
        messagebox.showerror("Error", f"El aeropuerto de destino '{destino_str}' no es válido.")
        return

    tiene_visa_bool = tiene_visa.get()

    # 3. Determinar aeropuertos permitidos
    if tiene_visa_bool:
        aeropuertos_permitidos = todos_aeropuertos
    else:
        aeropuertos_permitidos = {a for a, req in visas.items() if not req}

    # Verificar restricciones de visa
    if origen_str not in aeropuertos_permitidos:
        resultado_label.config(text=f"El aeropuerto de origen '{origen_str}' requiere visa y el pasajero no la posee.")
        return
    if destino_str not in aeropuertos_permitidos:
        resultado_label.config(text=f"El aeropuerto de destino '{destino_str}' requiere visa y el pasajero no la posee.")
        return

    # 4. Construir grafo y buscar ruta con BFS
    grafo = construir_grafo(tarifas, aeropuertos_permitidos)
    costo, escalas, ruta = encontrar_ruta_menos_escalas_bfs(grafo, origen_str, destino_str)

    # 5. Presentar resultados
    if costo != float('inf'):
        vuelos_totales = len(ruta) - 1
        resultado = (
            f"✈️ ¡Ruta con menos escalas encontrada! ✈️\n"
            f"Ruta: {' -> '.join(ruta)}\n"
            f"Costo Total: ${costo:,.2f}\n"
            f"Vuelos totales: {vuelos_totales}\n"
            f"Escalas: {escalas}\n"
            f"(Optimizado para menos escalas usando BFS)"
        )
        
        # Habilitar botón para ver grafo con ruta
        visualizar_ruta_btn.config(
            state="normal",
            command=lambda: GraphVisualizer(root, grafo, ruta)
        )
    else:
        resultado = f"No se encontró una ruta posible desde {origen_str} hacia {destino_str}."
        visualizar_ruta_btn.config(state="disabled")
        
    resultado_label.config(text=resultado)
    root.grafo_actual = grafo

def visualizar_todas_las_rutas(root):
    """Muestra TODAS las rutas del archivo tarifas.json sin filtros"""
    CompleteGraphVisualizer(root)

def iniciar_gui():
    root = tk.Tk()
    root.title("Metro Travel - Consulta de Vuelos")
    
    # Frame principal
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack()
    
    # Sección de entrada de datos
    tk.Label(main_frame, text="Aeropuerto ORIGEN:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    origen_entry = tk.Entry(main_frame, font=("Arial", 10), width=20)
    origen_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(main_frame, text="Aeropuerto DESTINO:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    destino_entry = tk.Entry(main_frame, font=("Arial", 10), width=20)
    destino_entry.grid(row=1, column=1, padx=5, pady=5)

    tiene_visa = tk.BooleanVar()
    root.tiene_visa_var = tiene_visa  # Guardar referencia para uso posterior
    tk.Checkbutton(main_frame, text="¿Tiene visa?", variable=tiene_visa, font=("Arial", 10)).grid(row=2, columnspan=2, pady=5)

    # Frame para botones
    button_frame = tk.Frame(main_frame)
    button_frame.grid(row=3, columnspan=2, pady=10)
    
    # Botones en dos filas
    # Primera fila
    consultar_btn = tk.Button(
        button_frame, text="Ruta Más Económica",
        command=lambda: iniciar_consulta(origen_entry, destino_entry, tiene_visa, resultado_label, root),
        bg="lightblue", font=("Arial", 10, "bold"), width=18
    )
    consultar_btn.grid(row=0, column=0, padx=5, pady=3)
    
    menos_escalas_btn = tk.Button(
        button_frame, text="Ruta Menos Escalas",
        command=lambda: buscar_menos_escalas(origen_entry, destino_entry, tiene_visa, resultado_label, root),
        bg="lightgreen", font=("Arial", 10, "bold"), width=18
    )
    menos_escalas_btn.grid(row=0, column=1, padx=5, pady=3)
    
    # Segunda fila
    global visualizar_ruta_btn
    visualizar_ruta_btn = tk.Button(
        button_frame, text="Ver Grafo con Ruta",
        state="disabled",
        bg="orange", font=("Arial", 10), width=18
    )
    visualizar_ruta_btn.grid(row=1, column=0, padx=5, pady=3)
    
    visualizar_todas_btn = tk.Button(
        button_frame, text="Ver TODAS las Rutas",
        command=lambda: visualizar_todas_las_rutas(root),
        bg="purple", fg="white", font=("Arial", 10, "bold"), width=18
    )
    visualizar_todas_btn.grid(row=1, column=1, padx=5, pady=3)

    # Área de resultados
    resultado_frame = tk.LabelFrame(main_frame, text="Resultado", font=("Arial", 10, "bold"))
    resultado_frame.grid(row=4, columnspan=2, padx=5, pady=10, sticky="ew")
    
    resultado_label = tk.Label(resultado_frame, text="", fg="blue", wraplength=400, justify="left", font=("Arial", 10))
    resultado_label.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    iniciar_gui()