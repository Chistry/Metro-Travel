from custom_priority_queue import CustomPriorityQueue # Importamos nuestra cola de prioridad personalizada

# Construye una representación de grafo a partir de las tarifas
def construir_grafo(tarifas, aeropuertos_permitidos):
    grafo = {aeropuerto: [] for aeropuerto in aeropuertos_permitidos}
    for origen, destino, precio in tarifas:
        if origen in aeropuertos_permitidos and destino in aeropuertos_permitidos:
            grafo[origen].append((destino, precio))
            grafo[destino].append((origen, precio))
    return grafo

def encontrar_ruta_mas_barata(grafo, origen, destino):
    cola_prioridad = CustomPriorityQueue() 
    
    distancias = {nodo: (float('inf'), float('inf')) for nodo in grafo}
    distancias[origen] = (0, 0)
    predecesores = {nodo: None for nodo in grafo}

    # Añadimos el nodo de origen a la cola de prioridad
    cola_prioridad.push((0, 0, origen, [origen])) 

    while not cola_prioridad.is_empty(): 
        costo_actual, escalas_actuales, nodo_actual, ruta_actual = cola_prioridad.pop() 

        # si ya hemos encontrado una ruta mejor a este nodo, lo ignoramos
        if (costo_actual, escalas_actuales) > distancias[nodo_actual]: 
            continue 
        
        # Si hemos llegado al destino, construimos la ruta y la devolvemos
        if nodo_actual == destino: 
            return costo_actual, escalas_actuales, ruta_actual 
            
        # Explorar vecinos del nodo_actual
        for vecino, precio_vuelo in grafo.get(nodo_actual, []): 
            nuevo_costo = costo_actual + precio_vuelo 
            nuevas_escalas = escalas_actuales + 1 
            
            # Si encontramos una ruta más corta o una ruta con menos escalas al mismo costo, actualizamos
            if (nuevo_costo, nuevas_escalas) < distancias[vecino]: 
                distancias[vecino] = (nuevo_costo, nuevas_escalas) 
                predecesores[vecino] = nodo_actual 
                nueva_ruta = ruta_actual + [vecino] 
                cola_prioridad.push((nuevo_costo, nuevas_escalas, vecino, nueva_ruta)) 
                
    # si no se enccuetrra una ruta al destino
    return float('inf'), 0, [] 
