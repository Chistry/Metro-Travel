from data_loader import cargar_visas, cargar_tarifas
from pathfinder import construir_grafo, encontrar_ruta_mas_barata

def iniciar_consulta():
    """
    Orquesta la aplicación: saluda, pide datos, procesa y muestra resultados.
    """
    print("✈️  Bienvenido al sistema de consulta de vuelos de Metro Travel ✈️")
    print("-" * 60)

    # 1. Cargar datos usando nuestro módulo
    visas = cargar_visas()
    tarifas = cargar_tarifas()
    todos_aeropuertos = set(visas.keys())

    # 2. Interactuar con el usuario (esto después lo cambian apra agregarle el UI de usuario)
    # ORIGEN
    origen = input("Ingrese el código del aeropuerto de ORIGEN: ").upper()
    if origen not in todos_aeropuertos:
        print(f"Error: El aeropuerto de origen '{origen}' no es válido.")
        return

    # DESTINO
    destino_final = input("Ingrese el código del aeropuerto de DESTINO: ").upper()
    if destino_final not in todos_aeropuertos:
        print(f"Error: El aeropuerto de destino '{destino_final}' no es válido.")
        return

    respuesta_visa = input("¿El pasajero tiene visa? (si/no): ").lower()
    tiene_visa = (respuesta_visa == 'si')

    print("-" * 60)

    # 3. Aplicar la lógica de negocio y obtener resultados

    # Lógica para determinar aeropuertos permitidos
    if tiene_visa:
        aeropuertos_permitidos = todos_aeropuertos
    else:
        aeropuertos_permitidos = {a for a, req in visas.items() if not req}

    # Verificar si el origen o el destino requieren visa y el pasajero no la tiene
    if origen not in aeropuertos_permitidos:
        print(f"Lo sentimos, no se puede calcular la ruta.")
        print(f"El aeropuerto de origen '{origen}' requiere visa y el pasajero no la posee.")
        return

    if destino_final not in aeropuertos_permitidos:
        print(f"Lo sentimos, no se puede calcular la ruta.")
        print(f"El aeropuerto de destino '{destino_final}' requiere visa y el pasajero no la posee.")
        return


    # Usamos las funciones de nuestro módulo pathfinder
    grafo = construir_grafo(tarifas, aeropuertos_permitidos)
    costo, escalas, ruta = encontrar_ruta_mas_barata(grafo, origen, destino_final)

    # 4. Presentar resultados
    if costo != float('inf'):
        print("🎉 ¡Ruta más económica encontrada! 🎉")
        print(f"Ruta: {' -> '.join(ruta)}")
        print(f"Costo Total: ${costo:,.2f}")
        print(f"Número de vuelos/escalas: {len(ruta) - 1}")
    else:
        print(f"Lo sentimos, no se encontró una ruta posible desde {origen} hacia {destino_final} con los criterios dados.")

if __name__ == "__main__":
    iniciar_consulta()