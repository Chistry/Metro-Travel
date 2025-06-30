import heapq # Importamos heapq para implementar una cola de prioridad, clave para el algoritmo de Dijkstra.
import csv   # Importamos csv para leer los archivos de datos de forma sencilla y robusta.

def cargar_visas(archivo_visas):
    """
    Carga los requisitos de visa desde un archivo de texto.
    
    Args:
        archivo_visas (str): La ruta al archivo 'visas.txt'.
    
    Returns:
        dict: Un diccionario donde las llaves son los códigos de aeropuerto 
              y los valores son booleanos (True si requiere visa, False si no).
    """
    visas = {}
    try:
        with open(archivo_visas, mode='r', encoding='utf-8') as f:
            lector = csv.reader(f)
            for fila in lector:
                if len(fila) == 2:
                    aeropuerto, requiere = fila
                    visas[aeropuerto.strip()] = (requiere.strip().lower() == 'si')
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_visas}' no fue encontrado.")
        exit() # Termina el programa si no se encuentra el archivo
    return visas

def cargar_tarifas(archivo_tarifas):
    """
    Carga las tarifas de vuelos desde un archivo de texto.
    
    Args:
        archivo_tarifas (str): La ruta al archivo 'tarifas.txt'.
        
    Returns:
        list: Una lista de tuplas, donde cada tupla representa un vuelo
              en el formato (origen, destino, precio).
    """
    tarifas = []
    try:
        with open(archivo_tarifas, mode='r', encoding='utf-8') as f:
            lector = csv.reader(f)
            for fila in lector:
                if len(fila) == 3:
                    origen, destino, precio_str = fila
                    try:
                        precio = float(precio_str)
                        tarifas.append((origen.strip(), destino.strip(), precio))
                    except ValueError:
                        print(f"Advertencia: Ignorando tarifa inválida en fila: {fila}")
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_tarifas}' no fue encontrado.")
        exit() # Termina el programa si no se encuentra el archivo
    return tarifas

def construir_grafo(tarifas, aeropuertos_permitidos):
    """
    Construye una representación de grafo a partir de las tarifas.
    El grafo es un diccionario donde cada llave es un aeropuerto y su valor
    es una lista de tuplas (destino, precio).
    
    Args:
        tarifas (list): La lista de vuelos (origen, destino, precio).
        aeropuertos_permitidos (set): Un conjunto de códigos de aeropuertos que
                                      se pueden usar en la ruta.
    
    Returns:
        dict: El grafo como una lista de adyacencia.
    """
    grafo = {aeropuerto: [] for aeropuerto in aeropuertos_permitidos}
    for origen, destino, precio in tarifas:
        # Solo añadimos la ruta si ambos aeropuertos están permitidos
        if origen in aeropuertos_permitidos and destino in aeropuertos_permitidos:
            # Añadimos el vuelo en ambas direcciones ya que los costos son iguales
            grafo[origen].append((destino, precio))
            grafo[destino].append((origen, precio))
    return grafo

def encontrar_ruta_mas_barata(grafo, origen, destino):
    """
    Encuentra la ruta más barata usando el algoritmo de Dijkstra.
    Si hay empate en costo, elige la ruta con menos escalas.
    
    Args:
        grafo (dict): El grafo de vuelos.
        origen (str): El código del aeropuerto de origen.
        destino (str): El código del aeropuerto de destino.
        
    Returns:
        tuple: Una tupla con (costo_total, numero_escalas, ruta_completa)
               o (inf, 0, []) si no se encuentra una ruta.
    """
    # La cola de prioridad almacenará tuplas de: (costo, escalas, nodo_actual, ruta_hasta_ahora)
    cola_prioridad = [(0, 0, origen, [origen])]
    
    # Un diccionario para llevar registro del costo mínimo y escalas para llegar a cada nodo
    distancias = {nodo: (float('inf'), float('inf')) for nodo in grafo}
    distancias[origen] = (0, 0)
    
    while cola_prioridad:
        # Extraemos el camino con el menor costo (y luego por escalas)
        costo_actual, escalas_actuales, nodo_actual, ruta_actual = heapq.heappop(cola_prioridad)
        
        # Si encontramos una ruta mejor a este nodo después de haberlo añadido a la cola, la ignoramos
        if (costo_actual, escalas_actuales) > distancias[nodo_actual]:
            continue
        
        # Si hemos llegado al destino, retornamos el resultado
        if nodo_actual == destino:
            return costo_actual, escalas_actuales, ruta_actual
            
        # Exploramos los vecinos (destinos directos desde el nodo actual)
        for vecino, precio_vuelo in grafo.get(nodo_actual, []):
            nuevo_costo = costo_actual + precio_vuelo
            nuevas_escalas = escalas_actuales + 1
            
            # Si encontramos una ruta más barata, o una con el mismo costo pero menos escalas...
            if (nuevo_costo, nuevas_escalas) < distancias[vecino]:
                # ...actualizamos la distancia y añadimos el nuevo camino a la cola
                distancias[vecino] = (nuevo_costo, nuevas_escalas)
                nueva_ruta = ruta_actual + [vecino]
                heapq.heappush(cola_prioridad, (nuevo_costo, nuevas_escalas, vecino, nueva_ruta))
                
    return float('inf'), 0, [] # Si el bucle termina, no se encontró ruta

def main():
    """
    Función principal que orquesta el programa.
    """
    print("✈️  Bienvenido al sistema de consulta de vuelos de Metro Travel ✈️")
    print("-" * 60)
    
    # Cargar datos
    visas = cargar_visas('visas.txt')
    tarifas = cargar_tarifas('tarifas.txt')
    
    todos_aeropuertos = set(visas.keys())
    
    # Solicitar información al usuario
    destino_final = input("Ingrese el código del aeropuerto de destino: ").upper()
    
    if destino_final not in todos_aeropuertos:
        print(f"Error: El aeropuerto de destino '{destino_final}' no es válido.")
        return
        
    respuesta_visa = input("¿El pasajero tiene visa? (si/no): ").lower()
    tiene_visa = (respuesta_visa == 'si')
    
    print("-" * 60)

    # Validar si el destino es accesible
    if visas.get(destino_final, False) and not tiene_visa:
        print("Lo sentimos, no se puede calcular la ruta.")
        print(f"El destino '{destino_final}' requiere visa y el pasajero no la posee.")
        return

    # Determinar aeropuertos permitidos para las escalas
    if tiene_visa:
        aeropuertos_permitidos = todos_aeropuertos
    else:
        # Si no tiene visa, solo puede pasar por aeropuertos que NO la requieran.
        aeropuertos_permitidos = {a for a, req in visas.items() if not req}
        # Aseguramos que el origen (CCS) y el destino final estén incluidos si son válidos.
        aeropuertos_permitidos.add('CCS')
        aeropuertos_permitidos.add(destino_final)

    # Construir grafo y encontrar la ruta
    origen = 'CCS'
    grafo = construir_grafo(tarifas, aeropuertos_permitidos)
    
    costo, escalas, ruta = encontrar_ruta_mas_barata(grafo, origen, destino_final)
    
    # Presentar resultados
    if costo != float('inf'):
        print("🎉 ¡Ruta más económica encontrada! 🎉")
        print(f"Ruta: {' -> '.join(ruta)}")
        print(f"Costo Total: ${costo:,.2f}")
        print(f"Número de escalas: {escalas}")
    else:
        print("Lo sentimos, no se encontró una ruta posible hacia el destino con los criterios dados.")
        
if __name__ == "__main__":
    main()